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
    res_dict = get_cell_merge_dict(result_table)
    return render_template("results.html", table=result_table, 
        sub_name=sub_name, res_dict=res_dict)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('error.html') 


def get_cell_merge_dict(result_table):
    res_dict = {}
    last_group_num = 1
    last_index = 1
    rowspan_counter = 0
    
    for i in range(1, len(result_table)):
        if last_group_num != result_table[i][0]:
            res_dict[last_index + 1] = rowspan_counter
            last_group_num = result_table[i][0]
            rowspan_counter = 1
            last_index = i
        else:
            rowspan_counter += 1
    res_dict[last_index + 1] = rowspan_counter
    return res_dict

if __name__ == "__main__":
    app.run(debug=True)