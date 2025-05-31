from sqlalchemy.orm import Session
import models
import datetime

def get_User(db : Session, id : str):
    return db.query(models.ToDo).filter(models.ToDo.id == id).first()

def get_Task(db : Session, task : str):
    return db.query(models.ToDo).filter(models.ToDo.task == task).first()

def create_Task(db : Session,task: str,user_id : str,date : str):
    task = models.ToDo(user_id,task,date)
    db.session.add(task)
    db.session.commit()

    return "create success"

def Task_Event(db : Session,user_id : str,is_create_task,is_set_notify):
    event = models.context_list(user_id,is_create_task,is_set_notify)
    db.session.add(event)
    db.session.commit()

    return f"{user_id}Context in add Task"

def update_Task():
    pass

from sqlalchemy.orm import Session
import models