""" Specifies routing for the application"""
from flask import render_template, request, jsonify, flash
from app import app
from app import database as db_helper

@app.route("/", methods=['GET', 'POST'])
def homepage():
    """ returns rendered homepage """
    cms = db_helper.fetch_cm()
    if request.method == 'POST':
        league_name = request.form.get('LeagueName')
        club_name = request.form.get('ClubName')
        player_name = request.form.get('PlayerName')
        s_function = request.form.get('SFunction')
        items = db_helper.fetch_todo(league_name,club_name,player_name,s_function)
        
    #     for i in items:
    #         if i['Name'] == league_name:
    #             k = i
    #             break
    #     #items = items.query.filter_by(LeagueName=league_name)
    #     return render_template("index.html", items=k)
        # if league_name == None & club_name == None & player_name == None:
        return render_template("index.html", items=items, cms=cms)
        # else:
        #     items = [{"id": 'NONE',"Name": 'NONE',"Nationality": 'NONE'}]
        #     return render_template("index.html", items=items) 
            
    else:
        return render_template("index.html", cms=cms)
    

@app.route("/delete/<int:task_id>", methods=['POST'])
def delete(task_id):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_task_by_id(task_id)
        result = {'success': True, 'response': 'Removed task'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<int:task_id>", methods=['POST'])
def update(task_id):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        if "status" in data:
            db_helper.update_status_entry(task_id, data["status"])
            result = {'success': True, 'response': 'Status Updated'}
        elif "description" in data:
            db_helper.update_task_entry(task_id, data["description"])
            result = {'success': True, 'response': 'Task Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new task """
    data = request.get_json()
    db_helper.insert_new_task(data['description'])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)



