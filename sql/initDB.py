from connection import sqlalchemy, database, host, engine

with sqlalchemy.create_engine(host).connect() as conn:

    # conn.execute('''
    #     DROP DATABASE IF EXISTS %s;''' % (database))

    conn.execute('''
        CREATE DATABASE %s;''' % (database))

with engine.connect() as conn:

    # conn.execute('''
    #     DROP TABLE IF EXISTS Distances15, Distances30, Distances60, Prices, Listings;''')

    conn.execute('''
        CREATE TABLE Listings (
            listingID   INT PRIMARY KEY AUTO_INCREMENT,
            symbol      VARCHAR(50),
            name        VARCHAR(255),
            active     BOOL DEFAULT 1,
            tracked     BOOL DEFAULT 0
        );''')

    conn.execute('''
        CREATE TABLE Prices (
            listingID   INT,
            date        DATE,
            open        REAL,
            close       REAL,
            high        REAL,
            low         REAL,
            volume      REAL,
            cap         REAL,
            PRIMARY KEY (listingID, date),
            CONSTRAINT FOREIGN KEY (listingID) REFERENCES Listings(listingID) ON DELETE CASCADE
        );''')

    # conn.execute('''
    #     CREATE TABLE Distances15 (
    #         listingID1  INT,
    #         listingID2  INT,
    #         distance    REAL,
    #         PRIMARY KEY (listingID1, listingID2),
    #         CONSTRAINT FOREIGN KEY (listingID1) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CONSTRAINT FOREIGN KEY (listingID2) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CHECK (listingID1 < listingID2)
    #     );''')

    # conn.execute('''
    #     CREATE TABLE Distances30 (
    #         listingID1  INT,
    #         listingID2  INT,
    #         distance    REAL,
    #         PRIMARY KEY (listingID1, listingID2),
    #         CONSTRAINT FOREIGN KEY (listingID1) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CONSTRAINT FOREIGN KEY (listingID2) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CHECK (listingID1 < listingID2)
    #     );''')

    # conn.execute('''
    #     CREATE TABLE Distances60 (
    #         listingID1  INT,
    #         listingID2  INT,
    #         distance    REAL,
    #         PRIMARY KEY (listingID1, listingID2),
    #         CONSTRAINT FOREIGN KEY (listingID1) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CONSTRAINT FOREIGN KEY (listingID2) REFERENCES Listings(listingID) ON DELETE CASCADE,
    #         CHECK (listingID1 < listingID2)
    #     );''')
    
with engine.connect() as conn:

    ## ComputeDistances(startDate, endDate)
    ##     Computes pairwise l2 distances of tracked listings' normalized close prices within the inclusive date range, creates and stores the result in `Distances` table.
    ##     Listing is ignored if it is missing one or more close prices in the date range.
    conn.execute('DROP PROCEDURE IF EXISTS ComputeDistances;')
    conn.execute('''
    CREATE PROCEDURE ComputeDistances (IN startDate DATE, IN endDate DATE)
    BEGIN

        DROP TEMPORARY TABLE IF EXISTS `Stats`, `Stats2`;

        CREATE TEMPORARY TABLE `Stats` (`listingID` INT PRIMARY KEY, `mean` REAL, `stddev` REAL, INDEX (`listingID`))
        SELECT `listingID`, AVG(close) AS `mean`, IF(STD(close)=0, 1,STD(close)) AS `stddev`
        FROM Prices
        WHERE startDate <= date AND date <= endDate AND `listingID` IN (SELECT `listingID` FROM `Listings` WHERE tracked = TRUE)
        GROUP BY `listingID`
        HAVING COUNT(close) >= DATEDIFF(endDate,startDate) + 1;

        CREATE TEMPORARY TABLE `Stats2` (`listingID` INT PRIMARY KEY, `mean` REAL, `stddev` REAL, INDEX (`listingID`))
        SELECT * FROM `Stats`;

        DROP TABLE IF EXISTS Distances;

        CREATE TABLE Distances (`listingID1` INT, `listingID2` INT, distance REAL,
        PRIMARY KEY (`listingID1`, `listingID2`))
        SELECT p1.`listingID` AS `listingID1`, p2.`listingID` AS `listingID2`, SUM(POW(p1.close - p2.close, 2)) AS distance
        FROM (SELECT `listingID`, date, (close-`mean`)/`stddev` AS close FROM Prices NATURAL JOIN `Stats` WHERE startDate <= date AND date <= endDate) p1 JOIN (SELECT `listingID`, date, (close-`mean`)/`stddev` AS close FROM Prices NATURAL JOIN `Stats2` WHERE startDate <= date AND date <= endDate) p2 ON p1.date = p2.date AND p1.`listingID` < p2.`listingID`
        GROUP BY p1.`listingID`, p2.`listingID`;

        SELECT * FROM Distances;
    END;''')
