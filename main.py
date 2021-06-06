import flash as flash
from flask import Flask, render_template, request, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "flash message"

@app.route('/payment')
def payment():
    return render_template('payment.html')

########################################################################################################################
########################################################################################################################

@app.route('/')
def index():
    return render_template('index.html')


########################################################################################################################
########################################################################################################################

@app.route('/update', methods=['POST', 'GET'])
def update():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gymmanagementsystem"
    )
    mycursor = mydb.cursor()

    if request.method == "POST":
        result = request.form.to_dict()
        userid = result['userid']
        amount = result['amount']
        paymentdate = result['paymentdate']
        duedate = result['duedate']
        mycursor.execute(""" update payment set amount=%s,paymentdate=%s,duedate=%s
        where userid=%s
        """, (amount, paymentdate, duedate, userid))

        flash("data updated successfully!")
        mydb.commit()
        mycursor.close()
        return render_template('admin.html')


########################################################################################################################
########################################################################################################################

@app.route('/delete/<userid>', methods=['POST', 'GET'])
def deletion(userid):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gymmanagementsystem"
    )
    mycursor = mydb.cursor()
    flash("data deleted successfully!")
    mycursor.execute("delete from payment where userid='" + userid + "'")

    mydb.commit()
    mycursor.close()
    return render_template("admin.html")


########################################################################################################################
########################################################################################################################

@app.route('/insert', methods=['POST'])
def insert():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gymmanagementsystem"
    )
    mycursor = mydb.cursor()

    if request.method == "POST":
        flash("data inserted successfully!")

        result = request.form.to_dict()
        userid = result['userid']
        name = result['firstname']
        paymentdate = result['paymentdate']
        duedate = result['duedate']

        mycursor.execute("insert into payment (userid,firstname,paymentdate,duedate) values (%s,%s,%s,%s)",
                         (userid, name, paymentdate, duedate))

        mydb.commit()
        mycursor.close()
        return render_template("admin.html")


########################################################################################################################
########################################################################################################################

@app.route('/result', methods=['POST', 'GET'])
def result():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gymmanagementsystem"
    )

    mycursor = mydb.cursor()

    # login part!
    if request.method == 'POST' and 'confirmpassword' not in request.form:
        singup = request.form
        username = singup['user']
        password = singup['pass']
        mycursor.execute(
            "select * from userregistration where firstname='" + username + "' and password='" + password + "'")
        r = mycursor.fetchall()
        count = mycursor.rowcount

        if count == 1 and username == 'admin':
            mycursor.execute("select * from payment")
            data = mycursor.fetchall()

            return render_template("admin.html", data=data)

        elif count == 1 and username != '1':
            return render_template("test.html")


        else:
            return render_template("index.html")

    # registration part!!

    if request.method == 'POST' and 'confirmpassword' in request.form:
        result = request.form.to_dict()
        firstname = result['firstname']
        lastname = result['lastname']
        email = result['email']
        password = result['password']
        confirmpassword = result['confirmpassword']

        if password == confirmpassword:
            mycursor.execute(
                "insert into userregistration (firstname,lastname,email,password,confirmpassword)values(%s,%s,%s,%s,%s)",
                (firstname, lastname, email, password, confirmpassword))

        else:
            return render_template("index.html")

        mydb.commit()
        mycursor.close()
        return render_template("index.html")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
