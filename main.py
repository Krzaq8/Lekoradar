from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from database.get_data import get_routes_for_substance, get_substance_name, get_substance_table, get_result_table
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = "2b3f12f3ef12a6c86b"
Bootstrap(app)

sub_num = len(get_substance_table())

@app.route("/")
def home():
    substances = get_substance_table()
    return render_template("home.html", substances=substances)

@app.route("/results", methods=('GET', 'POST'))
def results():
    
    sub_id = request.args.get('sub')

    if not sub_id.isdecimal() or int(sub_id) >= sub_num:
        return render_template('error.html') 
    
    route = int(request.form.get('route', -1))
    result_table = get_result_table(sub_id, route)

    round_up_data(result_table)
    sub_name = get_substance_name(sub_id)
    res_dict_id = get_cell_merge_dict(result_table, 0)
    return render_template("results.html", table=result_table, sub_name=sub_name,
        res_dict_id=res_dict_id, routes=get_routes_for_substance(sub_id))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('error.html') 


def get_cell_merge_dict(result_table, index):
    res_dict = {}
    last_val = None
    last_index = 1
    rowspan_counter = 0
    
    for i in range(1, len(result_table)):
        if last_val != result_table[i][index]:
            res_dict[last_index + 1] = rowspan_counter
            last_val = result_table[i][index]
            rowspan_counter = 1
            last_index = i
        else:
            rowspan_counter += 1
    res_dict[last_index + 1] = rowspan_counter # jinja has indexes starting from 1
    return res_dict

# changes numbers to strings to get trailing zeros
def round_up_data(result_table):
    for i in range(1, len(result_table)):
        result_table[i][-1] = '{:.2f}'.format(result_table[i][-1])
        result_table[i][-2] = '{:.2f}'.format(result_table[i][-2])



if __name__ == "__main__":
    app.run(debug=True)