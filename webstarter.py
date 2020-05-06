from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import pymysql

app = Flask(__name__)
#SQL
sql_db = pymysql.connect(host='localhost', user='root', password='root', db='enrollment', cursorclass=pymysql.cursors.DictCursor)

# NoSQL
client = MongoClient("localhost", 27017)

@app.route('/', methods=['GET'])
def test():
    return render_template("choosecollege.html")

###Create###
@app.route('/createmajor',methods = ['POST'])
def createmajor():
    major = request.form['major']
    degree = request.form['degree']
    college = request.form['college']
    dept = request.form['department']
    total = int(request.form['total'])
    men = int(request.form['men'])
    women = int(request.form['women'])
    caucasian = int(request.form['caucasian'])
    asianamerican = int(request.form['asianamerican'])
    africanamerican = int(request.form['africanamerican'])
    hispanic = int(request.form['hispanic'])
    nativeamerican = int(request.form['nativeamerican'])
    hawaiianpacificislander = int(request.form['hawaiianpacificislander'])
    multiracial = int(request.form['multiracial'])

    create_data_from_sql(major, degree, college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial)
    return render_template("back.html")

def create_data_from_sql(major, degree, college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial):
    cur = sql_db.cursor()
    cur.execute("INSERT IGNORE INTO ethsexfa18(Major_Name, Degree, College, Dept, Total, Men, Women, Caucasian, Asian_American, African_American, Hispanic, Native_American, Hawaiian_Pacific_Isl, Multiracial) VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(major, degree, college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial))
    sql_db.commit()
    cur.close()
    return 0

###Search###
@app.route('/searchcollege',methods = ['POST'])
def searchcollege():
    major = request.form['major']
    degree = request.form['degree']
    sql_data = get_major_data_from_sql(major, degree)
    print(sql_data)
    return render_template("majorinfo.html", sql_data = sql_data[0])

def get_major_data_from_sql(major, degree):
    cur = sql_db.cursor()
    cur.execute("SELECT * FROM ethsexfa18 WHERE Major_Name ='{}' AND Degree = '{}'".format(major, degree))
    sql_dictionary = cur.fetchall()
    cur.close()

    return sql_dictionary

###Update###
@app.route('/updatecollege',methods = ['POST'])
def updatecollege():
    major = request.form['major']
    degree = request.form['degree']
    college = request.form['college']
    dept = request.form['department']
    total = request.form['total']
    men = request.form['men']
    women = request.form['women']
    caucasian = int(request.form['caucasian'])
    asianamerican = int(request.form['asianamerican'])
    africanamerican = int(request.form['africanamerican'])
    hispanic = int(request.form['hispanic'])
    nativeamerican = int(request.form['nativeamerican'])
    hawaiianpacificislander = int(request.form['hawaiianpacificislander'])
    multiracial = int(request.form['multiracial'])

    sql_data = update_major_data_from_sql(major, degree, college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial)
    return render_template("back.html")

def update_major_data_from_sql(major, degree, college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial):
    cur = sql_db.cursor()
    cur.execute("UPDATE ethsexfa18 SET College = '{}', Dept = '{}', Total = '{}', Men = '{}', Women = '{}', Caucasian = '{}', Asian_American = '{}', African_American = '{}', Hispanic = '{}', Native_American = '{}', Hawaiian_Pacific_Isl = '{}', Multiracial = '{}' WHERE Major_Name = '{}' AND Degree = '{}'".format(college, dept, total, men, women, caucasian, asianamerican, africanamerican, hispanic, nativeamerican, hawaiianpacificislander, multiracial, major, degree))
    sql_db.commit()
    cur.close()
    return ""

###Delete###
@app.route('/deletecollege',methods = ['GET', 'POST'])
def deletecollege():
    major = request.form['major']
    degree = request.form['degree']
    sql_data = delete_major_data_from_sql(major, degree)
    return render_template("back.html")

def delete_major_data_from_sql(major, degree):
    cur = sql_db.cursor()
    cur.execute("DELETE FROM ethsexfa18 WHERE Major_Name ='{}' AND Degree = '{}'".format(major, degree))
    sql_db.commit()
    cur.close()
    return 0

###Interesting Queries###
@app.route('/minorityengineering')
def minorityengineering():
    sql_data = get_minority_data_from_sql()
    sql_dict = {}
    for row in sql_data:
        sql_dict[row['Major_Name']] = str(row['minorities'])
    print(sql_dict)
    return render_template("minoritieseng.html", sql_data = sql_data)
    
def get_minority_data_from_sql():
    cur = sql_db.cursor()
    cur.execute("SELECT e.Major_Name, (((e.Total - e.Caucasian)*1.0)/e.Total)*100 as minorities FROM ethsexfa18 e WHERE e.Degree = 'BS' AND e.College = 'Engineering' Order by minorities;")
    sql_dictionary = cur.fetchall()
    cur.close()

    return sql_dictionary

###Join Query###
@app.route('/choosecollege', methods = ['POST'])
def choosecollege():
    college = request.form['Collegename']
    no_sql_data = get_data_from_mongo(college)
    sql_data = get_join_data_from_sql(college)
    print(sql_data[0])
    print(no_sql_data)
    return render_template("tableview.html", sql_data= sql_data[0], mongo_data= no_sql_data)


def get_join_data_from_sql(college):
    college_sql = college
    if str(college) == "DGS":
        college_sql =  "Division of General Studies"
    if str(college) == "LAS":
        college_sql = "Liberal Arts & Sciences"
    if str(college) == "FAA":
        college_sql = "Fine & Applied Arts"
    if str(college) == "Engineering":
        college_sql = "Engineering"
    if str(college) == "Business":
        college_sql = "Gies College of Business"
    if str(college) == "AHS":
        college_sql = "Applied Health Sciences"
    if str(college) == "Total Campus":
        college_sql = "All"
    if str(college) == "Social Work":
        college_sql = "School of Social Work"
    if str(college) == "Media":
        college_sql = "College of Media"
    if str(college) == "ACES":
        college_sql = "Agr, Consumer & Env Sciences"
    
    cur = sql_db.cursor()
    cur.execute("SELECT * FROM percent_any_college INNER JOIN percent_same_college ON percent_any_college.department = percent_same_college.department WHERE percent_any_college.department = '{}'".format(college_sql))
    sql_dictionary = cur.fetchall()
    cur.close()
    
    for pair in sql_dictionary:
        for value in pair:
            pair[value] = pair[value]

    return sql_dictionary

###NoSQL Query###
def get_data_from_mongo(department):
    document = client.enrollment.gradrates.find_one({"department": department})
    return document

if __name__ == "__main__":
    app.run()