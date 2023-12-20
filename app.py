from flask import Flask, request, redirect, url_for, render_template, session,send_file
from flask_mysqldb import MySQL
import MySQLdb.cursors
import secrets
import pymysql
import io

app = Flask(__name__)

# Use a strong secret key
app.secret_key = secrets.token_hex(16)

# Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aditya2003'
app.config['MYSQL_DB'] = 'laptop_recomendation'
mysql = MySQL(app)

@app.route('/image/<data2_file_name>')
def display_image(data2_file_name):
            print(data2_file_name)
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(f"SELECT image from combine_data where data_file_name= '{data2_file_name}' ")
            result = cur.fetchone()
            if result:
                image_data = result['image']
                image_stream = io.BytesIO(image_data)
                return send_file(image_stream, mimetype='image/jpg')
            else:
                return "Image not found"
    



@app.route('/')
def main():
    try:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM data2  where id<=20")
        rows = cur.fetchall()
        print(rows,len(rows)) 
        return render_template('index.html', rows=rows )
    except Exception as e:
        print(f"Error in main route: {e}")
        return "An error occurred while processing your request."

@app.route('/nextPage/<int:id>')
def nextPage(id):
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute(f"SELECT * FROM data2  where id={id}")
     rows=cur.fetchone()
     return render_template('nextPage.html', rows=rows )
     

@app.route('/comparison')
def comparison():
     brand1=brand2=brand3=""
     laptop1="Laptop1"
     laptop2="Laptop2"
     laptop3="Laptop3"
    #  rows4={}
    #  rows5={}
    #  rows6={}
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute(f"SELECT distinct brand FROM data2 ")
     rows = cur.fetchall()
     print(rows)
     return render_template('comparison.html',rows=rows  ,brand1=brand1,brand2=brand2,brand3=brand3,laptop1=laptop1,laptop2=laptop2,laptop3=laptop3)
     
@app.route('/comparisonNext', methods=['POST'])
def comparisonNext():
     brand1 = request.form['getItem']
     brand2 = request.form['getItem2']
     brand3 = request.form['getItem3']
     laptop1="Laptop1"
     laptop2="Laptop2"
     laptop3="Laptop3"
     
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute(f"SELECT name FROM data2 where brand = '{brand1}'")
     rows1 = cur.fetchall()
     cur.execute(f"SELECT name FROM data2 where brand = '{brand2}' ")
     rows2 = cur.fetchall()
     cur.execute(f"SELECT name FROM data2 where brand = '{brand3}' ")
     rows3 = cur.fetchall()
     
     return render_template('comparison.html',rows1=rows1,rows2=rows2,rows3=rows3,brand1=brand1,brand2=brand2,brand3=brand3,laptop1=laptop1,laptop2=laptop2,laptop3=laptop3)


@app.route('/Docomparison', methods=['post'])
def Docomparison():
     laptop1 =request.form['getItem4']
     laptop2 =request.form['getItem5']
     laptop3 =request.form['getItem6']
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute(f"SELECT distinct brand FROM data2 ")
     rows = cur.fetchall()
     print(rows)
     cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
     cur.execute(f"SELECT * FROM data2 where name = '{laptop1}'")
     rows14 = cur.fetchall()
     cur.execute(f"SELECT * FROM data2 where name = '{laptop2}'")
     rows15 = cur.fetchall()
     cur.execute(f"SELECT * FROM data2 where name = '{laptop3}'")
     rows16 = cur.fetchall()
     print(rows14)
     print(rows15)
     print(rows16)
     return render_template('Docomparison.html',rows=rows,rows14=rows14 ,rows15=rows15,rows16=rows16,laptop1=laptop1,laptop2=laptop2,laptop3=laptop3)



@app.route('/search', methods=['POST'])
def search():
    try:
        brand = request.form['search']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute(f"SELECT * FROM data2 WHERE  brand = '{brand}' ")
        rows = cur.fetchall()
        return render_template('index.html', rows=rows )
    except Exception as e:
        print(f"Error in search route: {e}")
        return "An error occurred while processing your request."

if __name__ == '__main__':
    app.run(debug=True)
