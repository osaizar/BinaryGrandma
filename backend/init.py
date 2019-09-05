# coding: latin-1
from database import Base, engine
from werkzeug.security import generate_password_hash
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import *
import os
import sys
import pwd


def main():
    if database_exists(engine.url):
        ans = input("[+] Database found, do you want to delete it? (y/n) ")
        if ans.lower() == "y":
            ans = input("[!] Are you sure? (y/n) ")
            if ans.lower() == "y":
                print ("[+] Deleting the database...")
                drop_database(engine.url)
                os.system("rm -rf output")
                print ("[+] Creating the databse...")
                create_database(engine.url)
                Base.metadata.create_all(engine)
                os.system("mkdir -p output/bin")
                os.system("mkdir -p output/models")
    else:
        ans = input("[+] Database not found, do you want to create it? (y/n) ")
        if ans.lower() == "y":
                print ("[+] Creating the database...")
                create_database(engine.url)
                Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()
