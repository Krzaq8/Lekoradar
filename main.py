from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    # TODO tutaj umieszczam subtancje z osobnego pliku z subtancjami, plik jest tworzony przy starcie apliakcji czy coś
    substances = get_substance_list('substancje.csv')
    return render_template("home.html", substances=substances)

@app.route("/results")
def results():
    # TODO tutaj wstawiam funkcję od Asi, która zwraca tabelę wynikową dla konkretnej substancji aktywnej
    # result_table = get_result_table(request.args.get('sub'))
    result_table = [["a", "b", "c", "d"], ["e", "f", "g", "h"], ["i", "j", "k", "l"]]
    return render_template("results.html", table=result_table, table_header=["h1", "h2", "h3", "h4"])

def get_substance_list(file_address):
    with open(file_address) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        return [el for el in next(reader)]

if __name__ == "__main__":
    app.run(debug=True)