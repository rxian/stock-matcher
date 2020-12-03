CREATE PROCEDURE GetDefaultTrackedListings ()
BEGIN
    CREATE TEMPORARY TABLE IF NOT EXISTS TrackedListings
    SELECT listingID FROM Listings WHERE active = 1 AND tracked = 1;
END;

CREATE PROCEDURE GetTradingDates (IN startDate DATE, IN endDate DATE)
BEGIN
    CALL GetDefaultTrackedListings();
    DROP TEMPORARY TABLE IF EXISTS TradingDates;
    CREATE TEMPORARY TABLE TradingDates 
    SELECT DISTINCT date FROM Prices
    WHERE startDate <= date AND date <= endDate AND listingID IN (SELECT * FROM TrackedListings);
END;

CREATE PROCEDURE AlignPrices (IN startDate DATE, IN endDate DATE)
BEGIN
    CALL GetDefaultTrackedListings();
    CALL GetTradingDates(startDate, endDate);

    DROP TEMPORARY TABLE IF EXISTS AlignedPrices;
    CREATE TEMPORARY TABLE AlignedPrices
    SELECT d.listingID, d.date, COALESCE(p.close, (SELECT q.close FROM Prices q WHERE q.listingID = d.listingID AND q.date < d.date ORDER BY q.date DESC LIMIT 1)) AS close 
    FROM (SELECT listingID, date, close FROM Prices WHERE startDate <= date AND date <= endDate) p RIGHT OUTER JOIN (SELECT * FROM TrackedListings, TradingDates) d ON d.date = p.date AND d.listingID = p.listingID;
END;

CREATE PROCEDURE ComputeStats ()
BEGIN
    DROP TEMPORARY TABLE IF EXISTS PriceStats;
    CREATE TEMPORARY TABLE PriceStats (listingID INT PRIMARY KEY, mean REAL, stddev REAL, INDEX (listingID))
    SELECT listingID, AVG(close) AS `mean`, STD(close) AS `stddev`
    FROM AlignedPrices
    GROUP BY listingID;
END;

CREATE PROCEDURE NormalizePrices (IN startDate DATE, IN endDate DATE)
BEGIN
    CALL GetDefaultTrackedListings();
    CALL AlignPrices(startDate, endDate);
    CALL ComputeStats();

    DROP TEMPORARY TABLE IF EXISTS NormalizedPrices;
    CREATE TEMPORARY TABLE NormalizedPrices
    SELECT p.listingID, p.date, (p.close-s.mean)/IF(s.stddev=0,1,s.stddev) AS close
    FROM AlignedPrices p JOIN PriceStats s ON p.listingID = s.listingID;
END;

CREATE PROCEDURE ComputeDistances (IN targetListingID INT, IN startDate DATE, IN endDate DATE)
BEGIN
    CALL GetDefaultTrackedListings();
    CALL NormalizePrices(startDate, endDate);

    DROP TEMPORARY TABLE IF EXISTS NormalizedPrices2;
    CREATE TEMPORARY TABLE NormalizedPrices2
    SELECT * FROM NormalizedPrices
    WHERE listingID = targetListingID;

    DROP TEMPORARY TABLE IF EXISTS Distances;
    CREATE TEMPORARY TABLE  Distances (listingID INT PRIMARY KEY, distance REAL)
    SELECT p2.listingID AS listingID, AVG(POW(p1.close - p2.close, 2)) AS distance
    FROM NormalizedPrices2 p1 JOIN NormalizedPrices p2 ON p1.date = p2.date AND p1.listingID <> p2.listingID
    GROUP BY p1.listingID, p2.listingID;
END;

CREATE PROCEDURE ComputeAllPairsDistances (IN startDate DATE, IN endDate DATE)
BEGIN
    CALL GetDefaultTrackedListings();
    CALL NormalizePrices(startDate, endDate);
    
    DROP TEMPORARY TABLE IF EXISTS NormalizedPrices2;
    CREATE TEMPORARY TABLE NormalizedPrices2
    SELECT * FROM NormalizedPrices;
    
    DROP TEMPORARY TABLE IF EXISTS AllPairsDistances;
    CREATE TEMPORARY TABLE AllPairsDistances (listingID1 INT, listingID2 INT, distance REAL,
    PRIMARY KEY (listingID1, listingID2))
    SELECT p1.listingID AS listingID1, p2.listingID AS listingID2, AVG(POW(p1.close - p2.close, 2)) AS distance
    FROM NormalizedPrices p1 JOIN NormalizedPrices2 p2 ON p1.date = p2.date AND p1.listingID < p2.listingID
    GROUP BY p1.listingID, p2.listingID;
END;

CREATE PROCEDURE ComputeDTWDistances (IN targetListingID INT, IN startDate DATE, IN endDate DATE, IN frame INT)
BEGIN
    DECLARE i1 INT;
    DECLARE i2 INT;
    DECLARE n INT;
    DECLARE p REAL;

    CALL GetDefaultTrackedListings();
    CALL NormalizePrices(startDate, endDate);

    DROP TEMPORARY TABLE IF EXISTS TradingDates1;
    CREATE TEMPORARY TABLE TradingDates1 
    SELECT date, CAST(ROW_NUMBER() OVER (ORDER BY date) AS SIGNED) AS idx
    FROM TradingDates;

    DROP TEMPORARY TABLE IF EXISTS NormalizedPrices1;
    CREATE TEMPORARY TABLE NormalizedPrices1 (
        listingID INT,
        date DATE,
        idx INT,
        close REAL,
        INDEX (idx)
    )
    SELECT listingID, date, idx, close 
    FROM NormalizedPrices NATURAL JOIN TradingDates1;

    DROP TEMPORARY TABLE IF EXISTS DistancesDP;
    CREATE TEMPORARY TABLE DistancesDP (
        idx1 INT,
        idx2 INT,
        listingID INT,
        cost REAL,
        INDEX (idx1, idx2)
    );

    SET n = (SELECT MAX(idx) FROM TradingDates1);
    SET i1 = 1;
    WHILE i1 <= n DO
        SET i2 = GREATEST(1, i1-frame);

        SET p = (SELECT close FROM NormalizedPrices1 WHERE idx = i1 AND listingID = targetListingID);

        WHILE i2 <= LEAST(i1+frame, n) DO

            DROP TEMPORARY TABLE IF EXISTS NewCost;
            CREATE TEMPORARY TABLE NewCost (
                listingID INT, 
                thisCost REAL,
                pastCost1 REAL,
                pastCost2 REAL,
                pastCost3 REAL,
                INDEX (listingID)
            );

            INSERT INTO NewCost (listingID, thisCost)
            SELECT listingID, POW(close - p, 2) AS thisCost FROM NormalizedPrices1 WHERE idx = i2 AND listingID <> targetListingID;

            UPDATE NewCost c JOIN (SELECT listingID, cost FROM DistancesDP WHERE idx1 = i1-1 AND idx2 = i2) t ON c.listingID = t.listingID
            SET c.pastCost1 = t.cost;

            UPDATE NewCost c JOIN (SELECT listingID, cost FROM DistancesDP WHERE idx1 = i1 AND idx2 = i2-1) t ON c.listingID = t.listingID
            SET c.pastCost2 = t.cost;

            UPDATE NewCost c JOIN (SELECT listingID, cost FROM DistancesDP WHERE idx1 = i1-1 AND idx2 = i2-1) t ON c.listingID = t.listingID
            SET c.pastCost3 = t.cost;

            INSERT INTO DistancesDP
            SELECT i1, i2, listingID, COALESCE(thisCost + LEAST(COALESCE(pastCost1,pastCost2,pastCost3), COALESCE(pastCost2,pastCost1,pastCost3), COALESCE(pastCost3,pastCost2,pastCost1)), thisCost) FROM NewCost;

            SET i2 = i2 + 1;
        END WHILE;

        SET i1 = i1 + 1;
    END WHILE;

    DROP TEMPORARY TABLE IF EXISTS Distances;
    CREATE TEMPORARY TABLE Distances (listingID INT PRIMARY KEY, distance REAL)
    SELECT listingID, cost AS distance
    FROM DistancesDP
    WHERE idx1 = n AND idx2 = n;

    DROP TEMPORARY TABLE IF EXISTS Lengths;
    CREATE TEMPORARY TABLE Lengths
    SELECT listingID, COUNT(date) AS l
    FROM NormalizedPrices
    GROUP BY listingID;

    SET p = (SELECT COUNT(date) FROM NormalizedPrices WHERE listingID = targetListingID);

    UPDATE Distances d JOIN (SELECT listingID, COUNT(date) AS l FROM NormalizedPrices GROUP BY listingID) t ON d.listingID = t.listingID
    SET distance = distance / LEAST(p, t.l);

END;


-- CALL GetTradingDates('2020-05-30','2020-11-25');

-- DROP TEMPORARY TABLE IF EXISTS TradingDates1;
-- CREATE TEMPORARY TABLE TradingDates1 
-- SELECT date, CAST(ROW_NUMBER() OVER (ORDER BY date DESC) AS SIGNED) AS idx
-- FROM TradingDates;

-- SELECT * FROM TradingDates1;

-- CALL ComputeAllPairsDistances('2020-09-02','2020-11-25')

-- INSERT INTO Distances60
-- SELECT * FROM AllPairsDistances;