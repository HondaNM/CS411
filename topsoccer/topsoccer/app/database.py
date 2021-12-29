"""Defines all the functions related to the database"""
from sqlalchemy.util.langhelpers import NoneType
from app import db

def fetch_todo(ln,cn,pn,sf) -> dict:
    """Reads all tasks listed in the todo table

    Returns:
        A list of dictionaries
    """
    indicator = 0
    conn = db.connect()
    # better use another way to implement figure search
    if type(ln)!=NoneType:
        lname = ln
        query_results = conn.execute("Select * from Leagues where LeagueName like '%s' LIMIT 15;"% lname).fetchall()
    else: 
        #don't have league input
        if type(cn)!=NoneType:
            cname = cn
            query_results = conn.execute("Select * from Clubs where ClubName like '%s' LIMIT 15;"% cname).fetchall()
        else:
            #don't have club input
            if type(pn)!=NoneType:
                pname = pn
                indicator = 1
                query_results = conn.execute("Select * from Players where PlayerName like '%s' LIMIT 15;"% pname).fetchall()
            else:
                indicator = 2
                if sf == '0':
                    query_results = conn.execute("SELECT c.ClubName, Count(PlayerId) as num_p FROM Players p NATURAL JOIN Transfers t NATURAL JOIN Clubs c WHERE p.Overall > 80 GROUP BY ClubId ORDER BY num_p DESC LIMIT 15;").fetchall()
                else:
                    query_results = conn.execute("(SELECT COUNT(*) as num_p, Nationality FROM Players p WHERE Shoot > Defending GROUP BY Nationality ORDER BY num_p DESC, Nationality ASC LIMIT 10) UNION (SELECT COUNT(*) as num_p, Nationality FROM Players p WHERE Shoot > Defending GROUP BY Nationality ORDER BY num_p ASC, Nationality ASC LIMIT 10) ORDER BY num_p DESC LIMIT 15;").fetchall()
                    
    conn.close()
    todo_list = []
    if indicator == 1:
        for result in query_results:
            item = {
                "id": result[0],
                "Name": result[1],
                "Nationality": result[2],
                "a4": result[3],
                "a5": result[4],
                "a6": result[5],
                "a7": result[6],
                "a8": result[7],
                "a9": result[8],
                "a10": result[9],
                "a11": result[10],
                "a12": result[11],
                "a13": result[12],
                "a14": result[13],
                "a15": result[14],
                "a16": result[15],
                "a17": result[16],
                "a18": result[17],
                "a19": result[18]
            }
            todo_list.append(item)
    elif indicator == 2:
        for result in query_results:
            item = {
                "id": result[0],
                "Name": result[1],
            }
            todo_list.append(item)
    else:
        for result in query_results:
            item = {
                "id": result[0],
                "Name": result[1],
                "Nationality": result[2]
            }
            todo_list.append(item)

    return todo_list

def fetch_cm() -> dict:
    """Reads all comment listed in the Reviews table

    Returns:
        A list of dictionaries
    """

    conn = db.connect()
    query_results = conn.execute("Select * from Reviews;").fetchall()
    conn.close()
    todo_list = []
    for result in query_results:
        cm = {
            "id": result[0],
            "task": result[1]
        }
        todo_list.append(cm)

    return todo_list

def update_task_entry(task_id: int, text: str) -> None:
    """Updates task description based on given `task_id`

    Args:
        task_id (int): Targeted task_id
        text (str): Updated description

    Returns:
        None
    """

    conn = db.connect()
    query = 'Update Reviews set task = "{}" where id = {};'.format(text, task_id)
    conn.execute(query)
    conn.close()


# def update_status_entry(task_id: int, text: str) -> None:
#     """Updates task status based on given `task_id`

#     Args:
#         task_id (int): Targeted task_id
#         text (str): Updated status

#     Returns:
#         None
#     """

#     conn = db.connect()
#     query = 'Update tasks set status = "{}" where id = {};'.format(text, task_id)
#     conn.execute(query)
#     conn.close()


def insert_new_task(text: str) ->  int:
    """Insert new task to todo table.

    Args:
        text (str): Task description

    Returns: The task ID for the inserted entry
    """

    conn = db.connect()
    previousid = conn.execute("Select max(id) from Reviews;")
    previousid = [x for x in previousid]
    currentid = previousid[0][0] + 1
    query = 'Insert Into Reviews (id,task) VALUES ("{}","{}");'.format(
        currentid,text)
    conn.execute(query)
    query_results = conn.execute("Select  LAST_INSERT__ID();")
    query_results = [x for x in query_results]
    task_id = query_results[0][0]
    conn.close()

    return task_id


def remove_task_by_id(task_id: int) -> None:
    """ remove entries based on task ID """
    conn = db.connect()
    query = 'Delete From Reviews where id={};'.format(task_id)
    conn.execute(query)
    conn.close()
