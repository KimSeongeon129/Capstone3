from pymysql import cursors
import pymysql
db = pymysql.connect(host='127.0.0.1', user='root', password='alstjd1598!', charset='utf8')
cur = db.cursor()   #커서

#계정 변경
def update_account(db, user_pw, name, number, user_admin, user_line, user_id):
    with db.cursor() as cursor:
        sql = "update user set user_pw=%s, name=%s, number=%s, user_admin=%s, user_line=%s where user_id=%s"
        data = (user_pw, name, number, user_admin, user_line, user_id)
        cursor.execute(sql,data)     
    db.commit()

#계정  삭제
def delete_account(db, user_id):
    with db.cursor() as cursor:
        sql = "delete from user where user_id=%s"
        data = (user_id)
        cursor.execute(sql,data)     
    db.commit()

#계정 추가
def update_account(db, user_id, user_pw, name, number, user_admin, user_line):
    with db.cursor() as cursor:
        sql = "insert into user values(%s,%s, %s, %s, %s, %s)"
        data = (user_id, user_pw, name, number, user_admin, user_line)
        cursor.execute(sql,data)     
    db.commit()


#내역 조회
def check_result(db):
    with db.cursor() as cursor:
        sql = "select * from result"
        cursor.execute(sql)
        result = cursor.fetchall()
    
    return result

#bbox그리기
def bbox(db, inspection_number):
    with db.cursor() as cursor:
        sql = "select image, bbox_x1, bbox_x2, bbox_y1, bbox_y2 from image where inspection_number=%s"
        cursor.execute(sql, inspection_number)        
        result = cursor.fetchall()
        #bbox그리기 ,bbox 이미지 반환
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
        

#cur.close()