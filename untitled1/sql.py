import pymysql

db = pymysql.connect("localhost","root","wl5201314","shorurl")
cursor = db.cursor()
def insert(longname,shortname,co):
    sql = 'INSERT INTO s_url(longname,shortname,conut) VALUES ({},{},{}) ON DUPLICATE KEY UPDATE conut=conut+1'.format(longname,shortname,co)
    try:
        print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
db.close()