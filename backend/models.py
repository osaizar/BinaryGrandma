from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
import datetime, string, random
from database import Base
import string
import random

def string_generator(size=15, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Model(Base):
    __tablename__ = "models"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    desc = Column(String(255), nullable=False)
    benign = Column(Boolean, nullable=False)
    analyzed = Column(Boolean)
    filename = Column(String(255))


    def __init__(self, name, desc, benign):
        self.name = name
        self.desc = desc
        self.benign = benign
        self.analyzed = False
        self.filename = string_generator()


    def serialize(self):
        return {"id" : self.id, "name" : self.name, "desc" : self.desc, \
                "benign" : self.benign, "analyzed" : self.analyzed}


class Binary(Base):
    __tablename__ = "binaries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    hash = Column(String(255))
    filename = Column(String(255))
    date = Column(DateTime, default=datetime.datetime.utcnow)


    def __init__(self, name):
        self.name = name
        self.filename = string_generator()


    def serialize(self):
        return {"id" : self.id, "name" : self.name, "hash" : self.hash,
                "date" : self.date}


class Result(Base):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True, autoincrement=True)
    binary = Column(Integer, ForeignKey("binaries.id"))
    model = Column(Integer, ForeignKey("models.id"))
    score = Column(Integer)


    def __init__(self, binary, model, score):
        self.binary = binary
        self.model = model
        self.score = score


    def serialize(self):
        return {"id" : self.id, "binary" : self.binary, "model" : self.model, \
                "score" : self.score}

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)
    ended = Column(Boolean, default=False)
    name = Column(String(255))
    log = Column(String(1000))


    def __init__(self, name):
        self.name = name
        self.log = ""
        self.add_log("Job started")


    def add_log(self, msg):
        self.log += "[{}] {}\n".format(datetime.datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"), msg)


    def serialize(self):
        return {"id" : self.id, "start_time" : self.start_time.strftime("%Y/%m/%d %H:%M:%S"), "end_time" : self.end_time.strftime("%Y/%m/%d %H:%M:%S"),
                "ended" : str(self.ended), "name" : self.name, "log" : self.log}
