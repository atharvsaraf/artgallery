import mysql.connector as sql
class DBManager:
    def __init__(self):
        self.conn=sql.connect(database="artdb",user="root",password="admin")
    def login(self,uid,pwd):
        cmd="select userrole from loginmaster where userid=%s and pwd=%s"
        cur=self.conn.cursor()
        cur.execute(cmd,[uid,pwd])
        rec=cur.fetchone()
        if rec==None:
            return None
        else:
            return rec[0]

    def ulogin(self,eid,pswd):
        cmd="select * from regestrations where emailid=%s "
        cur = self.conn.cursor()
        cur.execute(cmd, [eid])
        rec = cur.fetchone()
        if rec == None:
            return None
        else:
            return rec


    def regester(self,nm,email,mobno,add,aadhar,pswd,role):
        cmd="insert into regestrations(pswd,role,name,address,mobno,emailid,aadhar)values(%s,%s,%s,%s,%s,%s,%s)"
        cur=self.conn.cursor()
        cur.execute(cmd,[pswd,role,nm,add,mobno,email,aadhar])
        self.conn.commit()
        cmd = "select max(id) from regestrations"
        cur = self.conn.cursor()
        cur.execute(cmd)
        rec = cur.fetchone()
        id = rec[0]
        cmd = "select * from regestrations where id=%s"
        cur = self.conn.cursor()
        cur.execute(cmd, [id])
        res = cur.fetchone()
        if res == None:
            return False
        else:
            return res



    def email(self,eid):
        cmd="insert into emailid(email) VALUES(%s) "
        cur=self.conn.cursor()
        cur.execute(cmd,[eid])
        self.conn.commit()


    def getCatagories(self):
        cmd="select * from catagories"
        cur=self.conn.cursor()
        cur.execute(cmd)
        lst=cur.fetchall()
        return lst

    def addpainting(self,ast,cid,siz,prc,uid):
        cmd="insert into paintings(artist,cid,size,price,owner) values(%s,%s,%s,%s,%s)"
        cur=self.conn.cursor()
        cur.execute(cmd,[ast,cid,siz,prc,uid])
        self.conn.commit()
        cmd="select max(pid) from paintings"
        cur=self.conn.cursor()
        cur.execute(cmd)
        rec=cur.fetchone()
        return rec[0]

    def getSelectedPaintings(self,selected):
        inlst=","
        inlst=inlst.join(selected)
        cmd="select pid,concat(pid,'.jpg') from paintings where cid in ("+inlst+")"
        print(cmd)
        cur=self.conn.cursor()
        cur.execute(cmd)
        lst=cur.fetchall()
        return lst

    def getPaintingInfo(self,pid):
        cmd="select * from paintings where pid=%s"
        cur = self.conn.cursor()
        cur.execute(cmd,[pid])
        rec=cur.fetchone()
        return rec

    def delPainting(self,pid):
        cmd="delete from paintings where pid=%s"
        cur = self.conn.cursor()
        cur.execute(cmd, [pid])
        self.conn.commit()
        return

    def changePwd(self,uid,opwd,npwd):
        cmd="update loginmaster set pwd=%s where userid=%s and pwd=%s"
        cur = self.conn.cursor()
        cur.execute(cmd, [npwd,uid,opwd])
        if cur.rowcount==1:
            self.conn.commit()
            return True
        else:
            return False
    def showartist(self):
        cmd="select * from regestrations  "
        cur=self.conn.cursor()
        cur.execute(cmd)
        lst=cur.fetchall()
        return lst

class Format:
    @staticmethod
    def getDDL(lst,name,collblindex,colvalindex):
        s="<select name="+name+" >"
        for rec in lst:
            collbl=rec[collblindex]
            colval=rec[colvalindex]
            op="<option value="+str(colval)+" >"+collbl+"</option>"
            s=s+op
        s=s+"</select>"
        return s
    @staticmethod
    def getCBL(lst,name,collblindex,colvalindex,colcount=1):
        s="<table><tr>"
        i=0
        for rec in lst:
            collbl=rec[collblindex]
            colval=rec[colvalindex]
            chk="<td><input type=checkbox name="+name+" value="+str(colval)+" >"+collbl+"</td>"
            s=s+chk
            i=i+1
            if i%colcount==0:
                s=s+"</tr><tr>"
        s=s+"</table>"
        return  s
    def getCBLx(lst,selected,collblindex,colvalindex,colcount=1):
        s="<table><tr>"
        i=0
        for rec in lst:
            collbl=rec[collblindex]
            colval=str(rec[colvalindex])
            if colval in selected:
                chk="checked"
            else:
                chk=""
            chk="<td><input type=checkbox "+chk+" name=chk"+str(i)+" value="+colval+" >"+collbl+"</td>"
            s=s+chk
            i=i+1
            if i%colcount==0:
                s=s+"</tr><tr>"
        s=s+"</table>"
        return  s


