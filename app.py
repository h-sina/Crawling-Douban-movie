import pymysql
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/index')
def home():
    return index()


@app.route('/ciyun')
def ciyun():
    return render_template("ciyun.html")


@app.route('/movies')
def movies():
    movies = []
    con = pymysql.connect(host='localhost', user='root', password='123456', database='jdbc')
    cur = con.cursor()
    sql = "select * from movie250"
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        movies.append(item)
    cur.close()
    con.close()
    return render_template("movies.html", movies=movies)


@app.route('/score')
def score():
    score = []
    num = []
    conn = pymysql.connect(host='localhost', user='root', password='123456', database='jdbc')
    cur = conn.cursor()
    sql = "select score,count(score) from movie250 group by score"
    cur.execute(sql)
    data = cur.fetchall()
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    conn.close()
    return render_template("score.html", score=score, num=num)


if __name__ == '__main__':
    # app.run(host="0.0.0.0", debug=True)
    app.run()
