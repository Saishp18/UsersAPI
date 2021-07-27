from flask import Flask, jsonify, request
from flaskext.mysql import MySQL
from flask_restful import Resource, Api
import hashlib

app = Flask(__name__)
mysql = MySQL()

api = Api(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'users'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

class User(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from users""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            json_form = request.get_json(force=True)
            print(json_form)

            username = hashlib.md5(json_form['username'].encode()).hexdigest()
            password = hashlib.md5(json_form['password'].encode()).hexdigest()
            insert_user_cmd = """INSERT INTO users(username, password) 
                                VALUES(%s, %s)"""
            cursor.execute(insert_user_cmd, (username, password))
            conn.commit()
            response = jsonify(message='account created', id=cursor.lastrowid)
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
 
#API resource routes
api.add_resource(User, '/user')
# api.add_resource(User, '/user/auth')

if __name__ == "__main__":
    app.run(debug=True)