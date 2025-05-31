from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ToDo(db.Model):
    __tablename__ = "list"
    id = db.Column(db.Integer,primary_key = True)
    userID = db.Column(db.String(255),nullable = False)
    task = db.Column(db.String(255))
    Date = db.Column(db.String(10))
    is_notify = db.Column(db.Boolean)

    def __init__(self,userID,task,Date):
        self.userID = userID 
        self.task = task
        self.Date = Date
        self.is_notify = False

    def __repr__(self): # 增加 __repr__ 方法方便調試
        return f"<ToDo {self.id}: {self.task[:20]}>"
    
class context_list(db.Model):
    __tablename__ = "context"
    channelID = db.Column(db.String(255),primary_key = True)
    is_add_task = db.Column(db.Boolean)
    is_set_notify = db.Column(db.Boolean)