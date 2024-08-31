from flask import Flask, render_template, request
from datetime import datetime
from find import find_stocks, find_pm25, get_pm25_json
import json

# print(__name__)

app = Flask(__name__)
books = {
    1: {
        "name": "Python book",
        "price": 299,
        "image_url": "https://im2.book.com.tw/image/getImage?i=https://www.books.com.tw/img/CN1/136/11/CN11361197.jpg&v=58096f9ck&w=348&h=348",
    },
    2: {
        "name": "Java book",
        "price": 399,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/087/31/0010873110.jpg&v=5f7c475bk&w=348&h=348",
    },
    3: {
        "name": "C# book",
        "price": 499,
        "image_url": "https://im1.book.com.tw/image/getImage?i=https://www.books.com.tw/img/001/036/04/0010360466.jpg&v=62d695bak&w=348&h=348",
    },
}


@app.route("/")
def index():
    today = datetime.now()
    return render_template("index.html", date=today)


@app.route("/books")
def show_books():
    for key in books:
        print(books[key])
    return render_template("books.html", books=books)


@app.route("/book/<int:id>")
def show_book(id):
    try:
        return f"<h1>第{id}本書:{books[id]}</h1>"
    except:
        return f"<h1 style='color:red'>無此編號:{id}</h1>"


@app.route("/sum/x=<x>&y=<y>")
def my_sum(x, y):
    try:
        total = eval(x) + eval(y)
        return f"{x}+{y}={total}"
    except:
        return "數值不正確"


@app.route("/bmi/name=<name>&height=<height>&weight=<weight>")
def my_bmi(name, height, weight):
    try:
        bmi = eval(weight) / (eval(height) ** 2)
        return f"<h1>{name}<br>您的bmi值為:{round(bmi,2)}<h1>"
    except:
        return "數值不正確"


@app.route("/stocks")
def get_stocks():
    datas = find_stocks()
    return render_template("stocks.html", stocks=datas)


@app.route("/pm25", methods=["GET", "POST"])
def get_pm25():
    print(request.form)
    today = datetime.now()
    if request.method == "POST":
        if "sort" in request.form:
            ascending = request.form.get("sort")
            sort = True
            if ascending == "true":
                ascending = True
            else:
                ascending = False
    else:
        sort = False
    columns, values = find_pm25(sort, ascending)
    data = {
        "columns": columns,
        "values": values,
        "today": today.strftime("%Y/%m/%d %H:%M:%S"),
    }
    return render_template("pm25.html", data=data)


@app.route("/pm25-chart")
def pm25chart():
    return render_template("pm25-chart.html")


@app.route("/pm25-data")
def get_pm25chart():
    try:
        json_data = get_pm25_json()
        return json.dumps(json_data, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps({"result": "failure", "exception": str(e)})


app.run(debug=True)
