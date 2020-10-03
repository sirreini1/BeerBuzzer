from flask import Flask
import sqlite3

app = Flask(__name__)
dbName = "beer.db"

"""holt bierCount und erhöht ihn um 1, gibt neuen beerCount zurück"""
@app.route('/<name>/')
def beer(name):
    con = sqlite3.connect(dbName)
    c = con.cursor()
    ret = c.execute('SELECT * FROM beer WHERE name=?', (name,))
    ret = ret.fetchone()

    #neuen eintrag, falls nicht vorhanden
    if(ret is None):
        c.execute(f"INSERT INTO beer VALUES ('{name}','0')")
        con.commit()
        ret = c.execute('SELECT * FROM beer WHERE name=?', (name,))
        ret = ret.fetchone()

    #alten beerCount holen und um 1 erhöhen
    print(ret)
    count = ret[1] + 1
    c.execute(f"UPDATE beer SET beerCount={count} WHERE name=?",(name,))
    con.commit()
    con.close()
    return f"{name} trinkt sein {count}es bier!"


"""holt nur den aktuellen count"""
@app.route('/<name>/count/')
def count(name):
    count = 0
    con = sqlite3.connect(dbName)
    c = con.cursor()
    ret = c.execute('SELECT * FROM beer WHERE name=?', (name,))
    ret = ret.fetchone()
    if ret is not None:
        count = ret[1]
    con.close()
    return count

"""gibt alle namen und deren beerCount zurück"""
@app.route('/all/')
def test():
    con = sqlite3.connect(dbName)
    c = con.cursor()
    ret = c.execute('SELECT * FROM beer')
    ret = ret.fetchall()
    con.close()
    return str(ret).strip('[]')

""" erstellt die DB und Table (nur einmal am anfang aufrufen!)"""
@app.route('/create/create/')
def create():
    con = sqlite3.connect(dbName)
    con.execute("CREATE TABLE beer (name TEXT PRIMARY KEY, beerCount INTEGER)")
    con.close()
    return "database created"

@app.route('/')
def home():
    return "BeerBuzzer! Anleitung:" \
           "    /name ,um count zu erhöhen." \
           "    /name/count ,um nur den count zu kriegen." \
           "    /all , um alle stats zu sehen."

if __name__ == '__main__':
    app.run()