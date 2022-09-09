
from flask import Flask,render_template,request,redirect,session,url_for,jsonify
from flask_mysqldb import MySQL
import re

app = Flask(__name__)

app.secret_key = "super secret key"
# app.config['SECRET_KEY']='HelloNikhil'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'myapp'
 
mysql = MySQL(app)

@app.route('/')
def hello():
    return 'hello world'






@app.route('/reg',methods=['POST','Get'])
def reg():

    
    if request.method=='POST':
        Name = request.form["Name"]
        Email = request.form["Email"]
        Password = request.form["Password"]
        Speciality = request.form["Speciality"]
        cur = mysql.connection.cursor()
        cur.execute("Select * from doc_details where Email = %s",(Email, ))
        account = cur.fetchone()
        if account:
           return jsonify("Account already exists!")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',Email):
           return jsonify("Invalid email address! ")
        elif not Name or not Password or not Email:
           return jsonify("Please fill out the form!")
           
        cur.execute("INSERT INTO doc_details(Name,Email,Password,Speciality) VALUES(%s,%s,%s,%s)",(Name,Email,Password,Speciality))
        mysql.connection.commit()
        cur.close()
        return jsonify("Successfully Registered")
    return jsonify("Failed")


@app.route('/login', methods = ['POST'])
def login():
    if request.method == 'GET':
        name1 = request.form['Name']
        password1 = request.form['Password']
        cursor = mysql.connection.cursor()
        cursor.execute("Select * from doc_details where Name = %s and Password=%s",(name1,password1))
        record = cursor.fetchone()
        if record:
            session['loggedin']= True
            session['Name']=record[1]
            return jsonify('Logged In Successfully !')
          
            
        else:
            return jsonify("Incorrect name/password.Try Again!")
    return jsonify("Back to Register Page")
   

@app.route("/users")
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("select * from doc_details")
    if resultValue>0:
        userDetails= cur.fetchall()
        return  render_template('users.html',userDetails=userDetails)
    return jsonify("No Doctor is Registered")

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
     
    cursor = mysql.connection.cursor()
    response_object = {'status' : 'success'}
   
    cursor.execute("Delete from doc_details where Id ={}" .format(id))
    mysql.connection.commit()
    cursor.close()
    response_object['message'] = 'Successfully Deleted'
    return jsonify(response_object)


if __name__ == '__main__':
    #   app.run(host='0.0.0.0', port=5000)
    app.run(debug=True) 


     # if request.method=='POST':
    #     Email = request.form["Email"]
    #     Password = request.form["Password"]
    #     cursor = mysql.connection.cursor()
    #     cursor.execute("Select * from doc_details where Email = %s and Password=%s",(Email,Password))
    #     session['loggedin']= True
    #     token=jwt.encode({
    #         'Email':request.form['Email'],
    #         'exp':datetime.datetime.utcnow() +datetime.timedelta(seconds=60)
    #     },
    #     app.config['SECRET_KEY'])
    #     return jsonify({'token':token.decode('utf-8')})
    # else:
    #     return jsonify("Failed Login")
      

    # msg=''
    
   
   # def check_for_token(func):
#     @wraps(func)
#     def wrapped(*args,**kwargs):
#         token=request.args.get('token')
#         if not token:
#             return jsonify({'message': 'Missing token'}),403
#         try:
#             data=jwt.decode(token,app.config['SECRET_KEY'])
#         except:
#             return jsonify({'message': 'Missing token'}),403
#         return func(*args,**kwargs)
#     return wrapped