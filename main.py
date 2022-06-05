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
    res_dict_id = get_cell_merge_dict(result_table, 0)
    res_dict_form = get_cell_merge_dict(result_table, 2)
    res_dict_route = get_cell_merge_dict(result_table, 3)
    res_dict_dose = get_cell_merge_dict(result_table, 4)
    return render_template("results.html", table=result_table, sub_name=sub_name,
     res_dict_id=res_dict_id, res_dict_form=res_dict_form, res_dict_dose=res_dict_dose, res_dict_route=res_dict_route)

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
    res_dict[last_index + 1] = rowspan_counter
    return res_dict

if __name__ == "__main__":
    app.run(debug=True)