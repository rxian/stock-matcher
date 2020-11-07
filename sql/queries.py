from connection import sqlalchemy, engine
import pygtrie

#%%
symbolsTrie = None
def getSymbols(prefix=''):
    global symbolsTrie
    if not symbolsTrie:
        symbolsTrie = pygtrie.CharTrie()
        with engine.connect() as conn:
            for r in conn.execute("SELECT symbol, listingID FROM Listings"):
                symbolsTrie[r[0]] = r[1]
    if symbolsTrie.has_node(prefix):
        return symbolsTrie.items(prefix)
    else:
        return []

def insertValues(table,values,schema=None):
    '''
    Sample usage:
    insertValues('Listings',['AAPL',1],schema=['symbol','active'])
    insertValues('Listings',[['AAPL',1],['AMZN',1]],schema=['symbol','active'])
    '''

    if not values:
        return
    if not (type(values) == list or type(values) == tuple) or ((type(values) == list or type(values) == tuple) and not (type(values[0]) == list or type(values[0]) == tuple)):
        values = [values]
    values = dict([['x%d' % i, x] for i,x in enumerate(values)])

    table = ''.join(filter(lambda x: True if x!='`'else False,table))
    raw = 'INSERT INTO `%s` ' % table
    if schema:
        schema = [''.join(filter(lambda x: True if x!='`'else False,y)) for y in schema]
        raw += '(%s) ' % ','.join(['`%s`' % x for x in schema])
    raw += 'VALUES ' + ', '.join([':%s' % k for k in values.keys()])

    q = sqlalchemy.text(raw)
    with engine.connect() as conn:
        conn.execute(q,values)


# %%
