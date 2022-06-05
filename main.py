from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from database.get_data import get_substance_name, get_substance_table, get_result_table

app = Flask(__name__)
app.config['SECRET_KEY'] = "2b3f12f3ef12a6c86b"
Bootstrap(app)

@app.route("/")
def home():
    substances = get_substance_table()
    return render_template("home.html", substances=substances)

@app.route("/results")
def results():
    sub_id = request.args.get('sub')
    result_table = get_result_table(sub_id)
    sub_name = get_substance_name(sub_id)
    return render_template("results.html", table=result_table, sub_name=sub_name)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('error.html') 

if __name__ == "__main__":
    app.run(debug=True)