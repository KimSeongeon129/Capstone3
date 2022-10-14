from flask import Flask
from db1011 import get_db,close_db,init_db
import login,admin_login,user_main,imgUpload,cameraUpload,list,statistics


app=Flask(__name__)
def main():
    init_db()
    app.register_blueprint(login.bp)
    app.register_blueprint(admin_login.bp)
    app.register_blueprint(user_main.bp)
<<<<<<< HEAD

@app.before_request # 요청이 오기 직전에 db 연결
def before_request():
    get_db()

@app.teardown_request # 요청이 끝난 직후에 db 연결 해제
def teardown_request(exception):
    close_db()
=======
    app.register_blueprint(imgUpload.bp)
    app.register_blueprint(cameraUpload.bp)
    app.register_blueprint(list.bp)
    app.register_blueprint(statistics.bp)
>>>>>>> fac1570c281384e96f3739d37f0b5d5488371d77


if __name__ =="__main__" :
    main()
    app.run(debug=True)