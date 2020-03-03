from flask_sqlalchemy import SQLAlchemy
from flask import redirect,url_for
from flask.app import Flask,request
from flask.templating import render_template
from datetime import date
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="oracle://system:virat123@127.0.0.1/XE"
db=SQLAlchemy(app)

class user_details(db.Model):
    __tablename__="user_details";
    rollno=db.Column(db.String(6),primary_key=True)
    name=db.Column(db.String(20))
    password=db.Column(db.String(20))
    dept=db.Column(db.String(20))
    phone_no=db.Column(db.Integer)

class book_details(db.Model):
    __tablename__="book_details"
    rollno=db.Column(db.String(6),primary_key=True)
    book_name=db.Column(db.String(50))  
    borrowed_date=db.Column(db.String(20))
    
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        username=request.form["username"]
        password=request.form["password"]
        detail=user_details.query.filter_by(name=username).first()
        if detail is not None:
            check_username=detail.name
            check_password=detail.password
            rollno=detail.rollno
            if username==check_username:
                if password==check_password:
                    return render_template("home_page.html",user=check_username,rollno=rollno)
                else:
                    return render_template("display.html",result="username")
            else:
                return render_template("display.html",result="username")
        else:
            return render_template("display.html",result="no_user")
            

@app.route("/new_user",methods=["POST","GET"])
def new_user():
    if request.method=="GET":
        return render_template("new_user.html")
    else:
        rollno=(request.form["rollno"]).upper()
        name=request.form["name"]
        password=request.form["password"]
        dept=request.form["dept"]
        phone_no=int(request.form["phone_no"])
        option=request.form["option"]
        if option=="CREATE":
            obj=user_details(rollno=rollno,name=name,dept=dept,phone_no=phone_no,password=password)
            db.session.add(obj)
            db.session.commit()
            return render_template("display.html",result="inserted",rollno=rollno)
        elif option=="BACK":
            return render_template("login.html")
            


@app.route("/borrow<rollno>",methods=["POST","GET"])
def borrow(rollno):
    if request.method=="GET":
        return render_template("borrow.html")
    else:
        today=date.today()
        option=request.form["option"]
        if option=="BORROW":
            book_name=request.form["book_name"]
            book1=book_details(book_name=book_name,rollno=rollno,borrowed_date=today)
            db.session.add(book1)
            db.session.commit()
            return render_template("display.html",result="borrowed",rollno=rollno)
        elif option=="BACK":
            return render_template("home_page.html",rollno=rollno)
            
@app.route("/return_book<rollno>")
def return_book(rollno):
    book=book_details.query.filter_by(rollno=rollno).first()
    if book is not None:
        db.session.delete(book)
        db.session.commit()
        return render_template("display.html",result="deleted",rollno=rollno)
    else:
        return render_template("display.html",result="not_deleted",rollno=rollno)
    
@app.route("/view_record<rollno>")
def view_record(rollno):
    book=book_details.query.filter_by(rollno=rollno).first()  
    if book is not None:
        return render_template("view_record.html",result="show",name=book.book_name,date=book.borrowed_date,rollno=rollno)
    else:
        return render_template("view_record.html",result="not_deleted",rollno=rollno)
    
@app.route("/home_page<rollno>",methods=["POST","GET"])
def home_page(rollno):
    if request.method=="GET":
        return render_template("home_page.html",rollno=rollno)
    else:
        option=request.form["option"];
        if option=="BORROW BOOK":
            book=book_details.query.filter_by(rollno=rollno).first()
            if book is None:
                return render_template("borrow.html",rollno=rollno)
            else:
                return render_template("display.html",result="already_available",rollno=rollno)
        elif option=="RETURN BOOK":
            return redirect(url_for('return_book',rollno=rollno))
        elif option=="VIEW RECORD":
            return redirect(url_for('view_record',rollno=rollno))

if __name__=="__main__":
    db.create_all()
    app.run(debug=True)
