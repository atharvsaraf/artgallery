from flask import *
from flask_mail import Mail,Message
from random import randint
from DBManager import *
app = Flask(__name__)
app.secret_key="art@12ka4"



db=DBManager()
mail=Mail(app)

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='atharvsaraf6@gmail.com'
app.config['MAIL_PASSWORD']='Atharv@19112000'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)


@app.route('/')
def index():
    return render_template("front.html",loginmsg="")
#@app.route("/userlogin")

@app.route('/userlogin',methods=["GET","POST"])
def userlogin():
    if request.method=="GET":
        return render_template("userlogin.html")
    if request.method=="POST":
        usrnm=request.form["name"]
        pswd=request.form["password"]
        print(usrnm,pswd)
        rec=db.ulogin(usrnm,pswd)
        print(usrnm,pswd)
        session["userid"] = usrnm


        if rec==None:
            msg="Username or password is incorrect"
            return render_template("userlogin.html",msg=msg)
        else:
            return render_template("user.html",rec=rec)

@app.route('/artistlogin',methods=["GET","POST"])
def artistlogin():
    if request.method=="GET":
        return render_template("artistlogin.html")
    if request.method=="POST":
        usrnm=request.form["name"]
        pswd=request.form["password"]
        rec=db.ulogin(usrnm,pswd)
        session["userid"]=usrnm

        if rec==None:
            msg="Username or password is incorrect"
            return render_template("artistlogin.html",msg=msg)
        else:
            return render_template("artist.html",rec=rec)



@app.route('/adminlogin',methods=["GET","POST"])
def adminlogin():
    if request.method=="GET":
        return render_template("adminlogin.html")
    if request.method=="POST":
        uid=request.form["name"]
        pwd=request.form["password"]
        res = db.login(uid, pwd)
        if res=="admin":
            session["userid"] = uid
            return render_template("adminindex.html")

        else:
            msg="Username or password is incorrect"
            return render_template("adminlogin.html",msg=msg)

@app.route('/reg',methods=["GET","POST"])
def regestration():
    """if request.method=="GET":
        return render_template("regester.html")"""
    if request.method=="POST":
        nm=request.form["nm"]
        email=session["email"]
        mobno=request.form["mobno"]
        add=request.form["add"]
        aadhar=request.form["aadhar"]
        pswd=request.form["pswd"]
        role=request.form["role"]

        rec=db.regester(nm,email,mobno,add,aadhar,pswd,role)
        if rec:
            if rec[2]=="artist":
                msg="Account created successfully."
                return render_template("artist.html",rec=rec)
            elif rec[2]=="user":
                msg = "Account created successfully."
                return render_template("user.html", rec=rec)
        else:
            msg="Try Again Later."
            return render_template("regestration.html",msg=msg)

@app.route('/verify',methods=["GET","POST"])
def verify():
    if request.method=="GET":
        return render_template("verify.html")
    if request.method=="POST":

        email=request.form['email']
        session['email']=email
        msg=Message(subject='OTP',sender='atharvsaraf6@gmail.com',recipients=[email])
        msg.body=str(otp)
        mail.send(msg)
        return render_template('validate.html')
@app.route('/validate',methods=["GET",'POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        db.email(session['email'])
        msg="Email varification succesfull"
        return render_template("regester.html",msg1=msg)
    else:
        msg="Wrong OTP,Please Try Again."
        return render_template("validate.html", msg=msg)





@app.route("/adminaddpainting",methods=["GET","POST"])
def adminaddpainting():
    if request.method=="GET":
        lst=db.getCatagories()
        ddlclst=Format.getDDL(lst,"cid",1,0)
        return render_template("adminaddpainting.html",catagories=ddlclst)
    if request.method=="POST":
        ast=request.form["artist"]
        cid=request.form["cid"]
        siz=request.form["size"]
        prc=request.form["price"]
        uid=session["userid"]
        pid=db.addpainting(ast,cid,siz,prc,uid)
        photoobj=request.files["photo"]
        photoobj.save("static/paintings/"+str(pid)+".jpg")
        msg=f"Painting added successfully..<br><img src='static/paintings/{pid}.jpg' height=200px>"
        return render_template("adminresult.html",title="Add Painting",msg=msg)

@app.route("/adminpaintings")
def adminpaintings():
    selected=list(request.args.values())
    if len(selected)==0:
        selected.append('0')
    plst=db.getSelectedPaintings(selected)
    lst=db.getCatagories()
    cblclst=Format.getCBLx(lst,selected,1,0,6)
    return render_template("adminpaintings.html",catagories=cblclst,paintings=plst)

@app.route("/adminshowpainting")
def adminshowpainting():
    pid=request.args["pid"]
    rec=db.getPaintingInfo(pid)
    inm=str(pid)+".jpg"
    return render_template("adminshowpainting.html",record=rec,inm=inm)

@app.route("/admindelpainting")
def admindelpainting():
    pid=request.args["pid"]
    db.delPainting(pid)
    return render_template("adminresult.html",title="Delete Painting",msg="painting deleted successfully..")

@app.route("/adminchangepwd",methods=["GET","POST"])
def adminchangepwd():
    if request.method=="GET":
        return render_template("adminchangepwd.html")
    if request.method=="POST":
        npwd=request.form["npwd"]
        opwd = request.form["opwd"]
        uid=session["userid"]
        res=db.changePwd(uid,opwd,npwd)
        if res==True:
            msg="Password Changed Successfully.."
        else:
            msg="Invalid Old Password.."
        return render_template("adminresult.html",title="Change Password",msg=msg)

@app.route('/faq',methods=["GET","POST"])
def faq():
    return render_template("faq.html")

@app.route("/userpaintings")
def userpaintings():
    selected=list(request.args.values())
    if len(selected)==0:
        selected.append('0')
    plst=db.getSelectedPaintings(selected)
    lst=db.getCatagories()
    cblclst=Format.getCBLx(lst,selected,1,0,6)
    return render_template("userpaintings.html",catagories=cblclst,paintings=plst)

@app.route("/usershowpainting")
def usershowpainting():
    pid=request.args["pid"]
    rec=db.getPaintingInfo(pid)
    inm=str(pid)+".jpg"
    return render_template("usershowpainting.html",record=rec,inm=inm)





"""@app.route("/showartist",methods=["GET"])
def showartist():
    lst=db.showartist()
    return render_template("showartists.html",lst=lst)"""




if __name__ == '__main__':
    app.run()
