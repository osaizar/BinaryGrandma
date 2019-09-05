from database import Session
from sqlalchemy import and_, or_, func
import traceback
from models import *

class DB():

    def __init__(self):
        self.session = Session()


    def __del__(self):
        self.session.close()


    def add(self, data):
        try:
            self.session.add(data)
            self.session.commit()
            return data
        except Exception as e:
            print(traceback.format_exc())
            return False


    def get_model_by_id(self, model_id):
        try:
            return self.session.query(Model).filter(Model.id == model_id).one()
        except Exception as e:
            print(traceback.format_exc())
            return None


    def get_models(self):
        try:
            return self.session.query(Model).all()
        except Exception as e:
            print(traceback.format_exc())
            return None


    def get_available_models(self):
        try:
            return self.session.query(Model).filter(Model.analyzed == True).all()
        except Exception as e:
            print(traceback.format_exc())
            return None


    def set_model_analyzed(self, model_id):
        try:
            model = self.get_model_by_id(model_id)
            model.analyzed = True
            self.session.commit()
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False


    def get_binary_by_id(self, binary_id):
        try:
            return self.session.query(Binary).filter(Binary.id == binary_id).one()
        except Exception as e:
            print(traceback.format_exc())
            return False


    def get_binaries(self):
        try:
            return self.session.query(Binary).all()
        except Exception as e:
            print(traceback.format_exc())
            return None


    def binary_add_hash(self, binary_id, hash):
        try:
            binary = self.get_binary_by_id(binary_id)
            binary.hash = hash
            self.session.commit()
            return True
        except Exception as e:
            print(traceback.format_exc())
            return False


    def get_results_by_binary_id(self, binary_id):
        try:
            return self.session.query(Result).filter(Result.binary == binary_id).all()
        except Exception as e:
            print(traceback.format_exc())
            return False
