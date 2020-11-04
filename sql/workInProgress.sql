CREATE PROCEDURE ImportPricesFromCsv (IN csvPath VARCHAR(65535))
BEGIN

    DROP TEMPORARY TABLE IF EXISTS ImportPrices;
    
    CREATE TEMPORARY TABLE ImportPrices(
        listingID   INT,
        symbol      VARCHAR(50),
        date        DATE,
        open        REAL,
        close       REAL,
        high        REAL,
        low         REAL,
        volume      REAL,
        cap         REAL
    );

    LOAD DATA INFILE csvPath
    INTO TABLE ImportPrices
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS
    (symbol,date,open,close,high,low,volume,cap);

    INSERT INTO Listings (symbol, active)
    SELECT s.symbol, 1
    FROM (SELECT DISTINCT symbol FROM ImportPrices) s LEFT OUTER JOIN Listings l ON s.symbol = l.symbol AND l.active = 1
    WHERE l.listingID IS NULL;

    UPDATE ImportPrices i, Listings l 
    SET i.listingID = l.listingID
    WHERE i.symbol = l.symbol AND l.active = 1;

    INSERT INTO Prices
    SELECT listingID,date,open,close,high,low,volume,cap
    FROM ImportPrices;

END



CREATE TRIGGER TriggerInsertPriceMatchSymbol BEFORE INSERT ON account
       FOR EACH ROW SET @sum = @sum + NEW.amount;




DROP TEMPORARY TABLE IF EXISTS CloseStatistics, CloseStatistics2;

CREATE TEMPORARY TABLE CloseStatistics (listingID INT PRIMARY KEY, mean REAL, stddev REAL, INDEX (listingID))
SELECT listingID, AVG(close) AS mean, IF(STD(close)=0, 1,STD(close)) AS stddev
FROM Prices
WHERE "2020-01-01" <= date AND date <= "2020-01-02"
GROUP BY listingID
HAVING COUNT(date) >= DATEDIFF("2020-01-02","2020-01-01")+1;

CREATE TEMPORARY TABLE CloseStatistics2 (listingID INT PRIMARY KEY, mean REAL, stddev REAL, INDEX (listingID))
SELECT * FROM CloseStatistics;

SELECT p1.listingID AS listingID1, p2.listingID AS listingID2, SUM(POW(p1.close - p2.close, 2)) AS distance
FROM (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN CloseStatistics WHERE "2020-01-01" <= date AND date <= "2020-01-02") p1 JOIN (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN CloseStatistics2 WHERE "2020-01-01" <= date AND date <= "2020-01-02") p2 ON p1.date = p2.date AND p1.listingID < p2.listingID
GROUP BY p1.listingID, p2.listingID;



CREATE PROCEDURE computeDistances (IN startDate DATE, IN endDate DATE)
BEGIN
    
    SELECT p1.listingID AS listingID1, p2.listingID AS listingID2, SUM(POW(p1.close - p2.close, 2)) AS distance
    FROM Prices p1 JOIN Prices p2 ON p1.date = p2.date AND startDate <= p1.date <= endDate
    WHERE p1.listingID < p2.listingID
    GROUP BY p1.listingID, p2.listingID
    HAVING COUNT(p1.listingID) >= DATEDIFF(endDate,startDate);
END

CREATE VIEW asdasd AS 


SELECT COALESCE(close, (SELECT 1) 



SELECT l.listingID, COALESCE(close, prevClose, nextClose)
FROM (select TrackedListings.listingID, '2020-01-02' as date from TrackedListings) l LEFT OUTER JOIN Prices ON l.listingID = Prices.listingID AND l.date = Prices.date LEFT OUTER JOIN 
(SELECT listingID, date AS prevCloseDate, close AS prevClose
FROM Prices NATURAL JOIN (SELECT listingID, MAX(date)
FROM Prices
WHERE date < '2020-01-02' AND close IS NOT NULL
GROUP BY listingID)) p
ON l.listingID = p.listingID LEFT OUTER JOIN
(SELECT listingID, date AS nextCloseDate, close AS nextClose
FROM Prices NATURAL JOIN (SELECT listingID, MIN(date)
FROM Prices
WHERE date > '2020-01-02' AND close IS NOT NULL
GROUP BY listingID)) q
ON l.listingID = q.listingID;


SELECT l.listingID, COALESCE(close, prevClose, nextClose)



SELECT listingID, date AS prevCloseDate, close AS prevClose
FROM Prices NATURAL JOIN (SELECT listingID, MAX(date)
FROM Prices
WHERE date < '2020-01-02' AND close IS NOT NULL
GROUP BY listingID) t;


SELECT listingID, date AS nextCloseDate, close AS nextClose
FROM Prices NATURAL JOIN (SELECT listingID, MIN(date)
FROM Prices
WHERE date > '2020-01-02' AND close IS NOT NULL
GROUP BY listingID) t;



            FROM (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN CloseStatistics WHERE startDate <= date AND date <= endDate) p1 
                JOIN (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN CloseStatistics2 WHERE startDate <= date AND date <= endDate) p2 
                ON p1.date = p2.date AND p1.listingID < p2.listingID
