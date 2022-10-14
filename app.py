from flask import Flask
from db1011 import get_db,close_db,init_db
import login,admin_login,user_main,imgUpload,cameraUpload,list,statistics


app=Flask(__name__)
def main():
    app.register_blueprint(login.bp)
    app.register_blueprint(admin_login.bp)
    app.register_blueprint(user_main.bp)
    app.register_blueprint(imgUpload.bp)
    app.register_blueprint(cameraUpload.bp)
    app.register_blueprint(list.bp)
    app.register_blueprint(statistics.bp)


if __name__ =="__main__" :
    main()
    app.run(debug=True)