from flask import Flask
from db1011 import get_db,close_db,init_db
import login


app=Flask(__name__)
def main():
    app.register_blueprint(login.bp)



if __name__ =="__main__" :
    main()
    app.run(debug=True)