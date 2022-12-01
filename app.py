from flask import Flask
from db1011 import init_db,get_db,close_db
import login,admin_login,user_main,imgUpload,cameraUpload,list,statistics,admin_main,account, accountUpdate, accountDelete ,admin_list,admin_statistics,admin_part
app=Flask(__name__)
app.secret_key="@!$qefq34@$1234wefQA#$233ASEDFs"


init_db()
app.register_blueprint(login.bp)
app.register_blueprint(user_main.bp)
app.register_blueprint(admin_login.bp)
app.register_blueprint(admin_main.bp)
app.register_blueprint(admin_list.bp)
app.register_blueprint(admin_statistics.bp)
app.register_blueprint(admin_part.bp)
app.register_blueprint(account.bp)  
app.register_blueprint(accountUpdate.bp)
app.register_blueprint(accountDelete.bp)    
app.register_blueprint(imgUpload.bp)
app.register_blueprint(cameraUpload.bp)
app.register_blueprint(list.bp)
app.register_blueprint(statistics.bp)
   
    

@app.before_request # 요청이 오기 직전에 db 연결
def before_request():
    get_db()

@app.teardown_request # 요청이 끝난 직후에 db 연결 해제
def teardown_request(exception):
    close_db()
    
if __name__ =="__main__" :
    app.run(port=5000, debug=True)

    