from flask import g,Blueprint
from contextlib import nullcontext
from pymysql import cursors, connect
import pymysql
import bcrypt

def init_db():

    db = connect(host='127.0.0.1', user='root', password='root', db='mydb', charset='utf8',cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()   #커서
   
    with db.cursor() as cursor: #DB가 없으면 만들어라.
        sql = "CREATE DATABASE IF NOT EXISTS mydb "
        cursor.execute(sql)
    db.commit()

    db.select_db('mydb')
    
    with db.cursor() as cursor: #DB가 없으면 만들어라.
    
        sql1= "CREATE TABLE IF NOT EXISTS mydb.`user` (`user_id` VARCHAR(100) NOT NULL, `nickname` VARCHAR(100) NOT NULL,`user_admin` VARCHAR(100) , `user_line` VARCHAR(100) ,PRIMARY KEY (`user_id`))"
        sql2= "CREATE TABLE IF NOT EXISTS mydb.`admin` (`admin_id` VARCHAR(100) NOT NULL, `admin_pw` VARCHAR(100) NOT NULL, `number` VARCHAR(100) NOT NULL, `name` VARCHAR(100) NOT NULL,PRIMARY KEY (`admin_id`))"
        sql3= "CREATE TABLE IF NOT EXISTS mydb.`result` (`part_id` VARCHAR(45) NOT NULL, `part_name` VARCHAR(45) NOT NULL, `part_category` VARCHAR(45) NOT NULL, `part_judge` VARCHAR(45) NOT NULL, `user_id` VARCHAR(100) NOT NULL, `inspection_number` INT(100) NOT NULL AUTO_INCREMENT PRIMARY KEY, `date` TIMESTAMP DEFAULT NOW()) "
        sql4= "CREATE TABLE IF NOT EXISTS mydb.`image` (`inspection_number` INT(100) NOT NULL,`bbox_x1` DOUBLE NOT NULL,`bbox_x2` DOUBLE NOT NULL,`bbox_y1` DOUBLE NOT NULL,`bbox_y2` DOUBLE NOT NULL,`image` VARCHAR(100) NOT NULL, PRIMARY KEY (`inspection_number`), FOREIGN KEY (`inspection_number`) REFERENCES `result` (`inspection_number`) ON DELETE cascade ON UPDATE cascade) "
        
        cursor.execute(sql1)   
        cursor.execute(sql2)   
        cursor.execute(sql3)   
        cursor.execute(sql4)
        add_admin(db,'id','1234','010','pms')
    db.commit
    db.close


def get_db(): #이거 개중요
    if 'db' not in g:     # 플라스크의 전역변수 g 속에 db 가 없으면
        g.db = connect(host='127.0.0.1', user='root', password='root', db='mydb', charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
        # 내꺼 db에 접속.

def close_db(): #db 연결 종료
    db=g.pop('db',None) #db라는 거를 팝.
    if db is not None: #팝 한게 비어있지 않으면
        if db.open: #db가 열려있으면
            db.close() #종료해라


#계정 변경(user)
def update_user(db,  nickname , user_admin, user_line, user_id):
    with db.cursor() as cursor:
        sql = "update user set nickname=%s, user_admin=%s, user_line=%s where user_id=%s"
        data = ( nickname, user_admin, user_line, user_id)
        cursor.execute(sql, data)     
    db.commit()

#계정 삭제(user)
def delete_user(db, user_id):
    with db.cursor() as cursor:
        sql = "delete from user where user_id=%s"
        data = (user_id)
        cursor.execute(sql,data)     
    db.commit()

#user_id 찾기
def find_id_user(db, user_id):
    with db.cursor() as cursor:
        sql= "select user_id from mydb.user where user_id=%s"
        cursor.execute(sql, user_id)
        result = cursor.fetchall()
        #db에 id가 존재함
        return result       
         
#user 계정 추가
def add_user(db, user_id, nickname):
    with db.cursor() as cursor:
        sql = "insert into mydb.user values(%s, %s, NULL, NULL)"
        data = (user_id, nickname) 
        cursor.execute(sql, data)
    db.commit()


#admin_id 찾기
def find_id_admin(db, admin_id):
    with db.cursor() as cursor:
        sql= "select admin_id from admin where admin_id=%s"
        cursor.execute(sql, admin_id)
        result = cursor.fetchone()
       
        return result
     

#admin id로 pw 찾아서 db와 비교후 반환 반환 값 true 또는 false
def get_admin_login(db, admin_id, admin_pw):
    with db.cursor() as cursor:
        sql = "select admin_pw from mydb.admin where admin_id=%s"
        data = (admin_id) 
        cursor.execute(sql, data)
        db_password = cursor.fetchone() #db에 저장되어있는 비밀번호    
        bytes_db_password=db_password['admin_pw'].encode('utf-8')
        bytes_admin_password=admin_pw.encode('utf-8')
        
        result = bcrypt.checkpw(bytes_admin_password ,bytes_db_password ) #아니 이게 위치가 정해진...하              
    return result    #일치하면 true 반환
        


#admin 계정 추가
def add_admin(db, admin_id, admin_pw,number,name):
    with db.cursor() as cursor:

        if (find_id_admin(db,admin_id)):        #db에 이미 계정이 존재하면
            return 
        else:
            encode_pw=admin_pw.encode('utf-8') #bytes 타입 변환
            salt = bcrypt.gensalt()
            hashed_pw=bcrypt.hashpw(encode_pw, salt) #해쉬키로 암호화
            decode_pw = hashed_pw.decode()   #db에 저장하기 전 unicode로 타입 변환
            sql = "insert into mydb.admin values(%s, %s, %s, %s)"
            data = (admin_id, decode_pw, number, name) 
            cursor.execute(sql, data)
            db.commit()



#내역 조회
def check_result(db):
    with db.cursor() as cursor:
        sql = "select * from result"
        cursor.execute(sql)
        result = cursor.fetchall()
    
    return result

#검사번호로 내역 찾기
def search_result(db, inspection_number):
    with db.cursor() as cursor:
        sql = "select * from result where inspection_number=%s"
        data=(inspection_number)
        cursor.execute(sql,data)
        result = cursor.fetchall()
    
    return result

#bbox 좌표, 이미지 가져오기
def bbox(db, inspection_number):
    with db.cursor() as cursor:
        sql = "select image, bbox_x1, bbox_x2, bbox_y1, bbox_y2 from image where inspection_number=%s"
        data=(inspection_number)
        cursor.execute(sql, data)        
        result = cursor.fetchall()
        
    return result

#상세조회
def detailed_result(db, inspection_number):
    with db.cursor() as cursor:
        sql = "select * from result where inspection_number=%s"
        cursor.execute(sql, inspection_number)
        result = cursor.fetchall()
    
    return result

#part_id로 inspection_number 찾기
def find_inspection_number(db, part_id):
    with db.cursor() as cursor:
        sql = "select inspection_number from result where part_id=%s"
        data = (part_id)
        cursor.execute(sql, data)
        result = cursor.fetchall()
        result = result[0]['inspection_number']
        
    return result
        
    

#검사 결과 추가(저장)
def add_result(db, part_id, part_name, part_category, part_judge, user_id):
    with db.cursor() as cursor:
        sql = "insert into result (part_id,part_name,part_category,part_judge,user_id,date) values(%s,%s,%s,%s,%s, DEFAULT)"
        data = (part_id,  part_name, part_category, part_judge, user_id)
        cursor.execute(sql, data)
        
        db.commit()
        


 #검사 이미지 추가
def add_image(db, inspection_number, bbox_x1, bbox_x2, bbox_y1, bbox_y2, image):
    with db.cursor() as cursor:
        sql = "insert into image values(%s,%s,%s,%s,%s,%s)"
        data = (inspection_number, bbox_x1, bbox_x2, bbox_y1, bbox_y2, image)
        cursor.execute(sql, data)
        db.commit()
        


#부품 내역 삭제
def delete_result(db, inspection_number):
    with db.cursor() as cursor:
        sql = "delete from result where inspection_number=%s"
        data = (inspection_number)
        cursor.execute(sql, data)
        db.commit()
        



#부품 내역 변경
def update_result(db, part_category, part_judge,  inspection_number):
    with db.cursor() as cursor:
        sql = "update result set part_category=%s, part_judge=%s where inspection_number=%s"
        data = (part_category, part_judge, inspection_number)
        cursor.execute(sql, data)
        db.commit()
        
        


#db.close()