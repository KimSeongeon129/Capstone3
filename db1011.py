from contextlib import nullcontext
from pymysql import cursors
import pymysql
import bcrypt
db = pymysql.connect(host='127.0.0.1', user='root', password='alstjd1598!', db='capstoneDB', charset='utf8')
cur = db.cursor()   #커서


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
        sql= "select user_id from user where user_id=%s"
        cursor.execute(sql, user_id)
        result = cursor.fetchall()
    if result==user_id:     #db에 id가 존재함
        return True
    else:                   #db에 id가 존재하지 않음 
        return False
     
#user 계정 추가
def add_user(db, user_id, nickname):
    with db.cursor() as cursor:
        sql = "insert into user values(%s, %s, NULL, NULL)"
        data = (user_id, nickname) 
        cursor.execute(sql, data)
    db.commit()


#admin_id 찾기
def find_id_admin(db, admin_id):
    with db.cursor() as cursor:
        sql= "select admin_id from admin where admin_id=%s"
        cursor.execute(sql, admin_id)
        result = cursor.fetchall()

        if result == admin_id:      #db에 id가 존재함 -> 기존 회원
            return True
        else:                   #db에 id가 존재하지 않음 -> 신규회원 
            return False
     


#admin id로 pw 찾아서 db와 비교후 반환
def admin_login(db, admin_id, admin_pw):
    with db.cursor() as cursor:
        sql = "select admin_pw from admin where admin_id=%s"
        data = (admin_id) 
        cursor.execute(sql, data)
        result = cursor.fetchall()
              
    return bcrypt.checkpw(result.encode('utf-8'), admin_pw.encode('utf-8'))   #일치하면 true 반환
        


#admin 계정 추가
def add_admin(db, admin_id, admin_pw,number,name):
    with db.cursor() as cursor:
        hashed_pw=bcrypt.hashpw(admin_pw.encode('utf-8'), bcrypt.gensalt()) #bytes 타입 변환후 해쉬키로 암호화
        save_pw = hashed_pw.decode('utf-8')   #db에 저장하기 전 unicode로 타입 변환 

        sql = "insert into admin values(%s, %s, %s, %s)"
        data = (admin_id, save_pw, number, name) 
        cursor.execute(sql, data)
        db.commit()


add_admin(db, 'id15', 'qw12', '01012345678', '홍길동' )  #샘
add_admin(db, 'id22', 'ee44', '01045645645', '이몽룡' )  #플
add_admin(db, 'id66', 'tt66', '01077778888', '성춘향' )  #입니당

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

#검사 결과 추가(저장)
def add_result(db, part_id, date, part_name, part_category, part_judge, user_id, inspection_number):
    with db.cursor() as cursor:
        sql = "insert into result values(%s,%s,%s,%s,%s,%s,%s)"
        data = (part_id, date, part_name, part_category, part_judge, user_id, inspection_number)
        cursor.execute(sql, data)
        db.commit()
        

 #검사 이미지 추가
def add_image(db, inspection_number, img_id, bbox_x1, bbox_x2, bbox_y1, bbox_y2, image):
    with db.cursor() as cursor:
        sql = "insert into image values(%s,%s,%s,%s,%s,%s,%s)"
        data = (inspection_number, img_id, bbox_x1, bbox_x2, bbox_y1, bbox_y2, image)
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