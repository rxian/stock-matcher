#%%

from connection import *

engine = sqlalchemy.create_engine(os.path.join(host,database)+'?'+options,echo=True)


#%%
with engine.connect() as conn:


    res = conn.execute(sqlalchemy.text('CALL ComputeDistances(:x, :y);'), x='2020-01-01', y='2020-01-02')

    for r in res:
    
        print(r)

# %%

with engine.connect() as conn:
    for r in conn.execute('SELECT * FROM Distances'):
        print(r)


# %%
with engine.connect() as conn:
    conn.execute('DROP PROCEDURE IF EXISTS ComputeDistances;')
    conn.execute('''
        CREATE PROCEDURE ComputeDistances (IN startDate DATE, IN endDate DATE)
        BEGIN

            DROP TEMPORARY TABLE IF EXISTS Stats, Stats2;

            CREATE TEMPORARY TABLE Stats (listingID INT PRIMARY KEY, mean REAL, stddev REAL, INDEX (listingID))
            SELECT listingID, AVG(close) AS mean, IF(STD(close)=0, 1,STD(close)) AS stddev
            FROM Prices
            WHERE startDate <= date AND date <= endDate AND listingID IN (SELECT listingID FROM Listings WHERE tracked = TRUE)
            GROUP BY listingID
            HAVING COUNT(close) >= DATEDIFF(endDate,startDate) + 1;

            CREATE TEMPORARY TABLE Stats2 (listingID INT PRIMARY KEY, mean REAL, stddev REAL, INDEX (listingID))
            SELECT * FROM Stats;

            DROP TABLE IF EXISTS Distances;

            CREATE TABLE Distances (listingID1 INT, listingID2 INT, distance REAL)
            SELECT p1.listingID AS listingID1, p2.listingID AS listingID2, SUM(POW(p1.close - p2.close, 2)) AS distance
            FROM (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN Stats WHERE startDate <= date AND date <= endDate) p1 JOIN (SELECT listingID, date, (close-mean)/stddev AS close FROM Prices NATURAL JOIN Stats2 WHERE startDate <= date AND date <= endDate) p2 ON p1.date = p2.date AND p1.listingID < p2.listingID
            GROUP BY p1.listingID, p2.listingID;

            ALTER TABLE Distances
            ADD PRIMARY KEY (listingID1, listingID2),
            ADD CONSTRAINT FOREIGN KEY (listingID1) REFERENCES Listings(listingID) ON DELETE CASCADE,
            ADD CONSTRAINT FOREIGN KEY (listingID2) REFERENCES Listings(listingID) ON DELETE CASCADE,
            ADD CHECK (listingID1 < listingID2);

            SELECT * FROM Distances;
        END;''')
# %%

def importPricesFromCsv(path):
    with engine.connect() as conn:

        conn.execute('''
            DROP TEMPORARY TABLE IF EXISTS ImportPrices;''')

        conn.execute('''
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
            );''')

        conn.execute(sqlalchemy.text('''
            LOAD DATA INFILE :x
            INTO TABLE ImportPrices
            FIELDS TERMINATED BY ','
            OPTIONALLY ENCLOSED BY '"'
            LINES TERMINATED BY '\\n'
            IGNORE 1 ROWS
            (symbol,date,open,close,high,low,volume,cap);'''),x=path)

        conn.execute('''
            INSERT INTO Listings (symbol, active)
            SELECT s.symbol, 1
            FROM (SELECT DISTINCT symbol FROM ImportPrices) s LEFT OUTER JOIN Listings l ON s.symbol = l.symbol AND l.active = 1
            WHERE l.listingID IS NULL;''')

        conn.execute('''
            UPDATE ImportPrices i, Listings l 
            SET i.listingID = l.listingID
            WHERE i.symbol = l.symbol AND l.active = 1;''')

        conn.execute('''
            INSERT INTO Prices
            SELECT listingID,date,open,close,high,low,volume,cap
            FROM ImportPrices;''')

# %%
