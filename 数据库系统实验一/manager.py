from tkinter import *
from tkinter import messagebox
import pickle
import pymysql

def cx1():
    a=entryt1.get()
    if a=='':
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:      
        a='\''+str(a)+'\''
        windowcx1 = Tk()
        windowcx1.title('查询1')
        windowcx1.geometry('200x400')
        Label(windowcx1,text="员工名").place(x=0,y=0)
        sql="select distinct ENAME from EMPLOYEE natural join WORKS_ON natural join PROJECT where PNAME = %s"%a
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        l1=Listbox(windowcx1)
        for i in data:
            m=''
            for j in i:
                m=j
            a.append(m)
        for each in a:
            l1.insert(END, each)
        l1.place(x=0,y=50,height=350,width=200)

def cx2():
    a=entryt21.get()
    b=entryt22.get()
    if a=='' or b=='':
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:      
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        windowcx2 = Tk()
        windowcx2.title('查询2')
        windowcx2.geometry('200x400')
        Label(windowcx2,text="部门名").place(x=0,y=0)
        Label(windowcx2,text="地址").place(x=160,y=0)
        sql='select distinct ENAME,ADDRESS from EMPLOYEE natural join DEPARTMENT where DEPARTMENT.DNAME = %s and EMPLOYEE.SALARY < %s'%(a,b)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        l1=Listbox(windowcx2)
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        for each in a:
            l1.insert(END, each)
        l1.place(x=0,y=50,height=350,width=200)

def cx3():
    windowcx3 = Tk()
    windowcx3.title('查询3')
    windowcx3.geometry('200x400')
    Label(windowcx3,text="部门名").place(x=0,y=0)
    Label(windowcx3,text="平均工资").place(x=150,y=0)
    sql='select DNAME,avg(SALARY) from EMPLOYEE natural join DEPARTMENT group by DNO'
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    l1=Listbox(windowcx3)
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*25
        a.append(m)
    for each in a:
        l1.insert(END, each)
    l1.place(x=0,y=50,height=350,width=200)

def cx4():
    a=entryt4.get()
    if a=='':
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:      
        a='\''+str(a)+'\''
        windowcx4 = Tk()
        windowcx4.title('查询4')
        windowcx4.geometry('200x400')
        Label(windowcx4,text="员工名").place(x=0,y=0)
        Label(windowcx4,text="地址").place(x=170,y=0)
        sql='select EMPLOYEE.ENAME,DNAME from EMPLOYEE natural join DEPARTMENT join EMPLOYEE as LEADER on EMPLOYEE.SUPERSSN = LEADER.ESSN and EMPLOYEE.ESSN <> LEADER.ESSN where LEADER.ENAME = %s'%a
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        l1=Listbox(windowcx4)
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*30
            a.append(m)
        for each in a:
            l1.insert(END, each)
        l1.place(x=0,y=50,height=350,width=200)

def cx5():
    a=entryt51.get()
    b=entryt52.get()
    if a=='' or b=='':
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:      
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        windowcx5 = Tk()
        windowcx5.title('查询5')
        windowcx5.geometry('200x400')
        Label(windowcx5,text="员工号").place(x=0,y=0)
        sql='select distinct a.ESSN from (select ESSN from WORKS_ON where PNO = %s) as a join (select ESSN from WORKS_ON where PNO = %s) as b on a.ESSN = b.ESSN'%(a,b)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        l1=Listbox(windowcx5)
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        for each in a:
            l1.insert(END, each)
        l1.place(x=0,y=50,height=350,width=200)
def cx6():
    windowcx6 = Tk()
    windowcx6.title('查询6')
    windowcx6.geometry('200x400')
    Label(windowcx6,text="员工名").place(x=0,y=0)
    sql='select ENAME from EMPLOYEE natural join WORKS_ON group by ESSN,ENAME having count(PNO) >= 3 and sum(HOURS) <= 8'
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    l1=Listbox(windowcx6)
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*36
        a.append(m)
    for each in a:
        l1.insert(END, each)
    l1.place(x=0,y=50,height=350,width=200)

#登录新界面
def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('manager_info.pickle', 'rb') as usr_file:
            manager_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('manager_info.pickle', 'wb') as usr_file:
            manager_info = {'admin': 'admin'}
            sql = "select ESSN from employee"
            cursor.execute(sql)
            data=list(cursor.fetchall())
            for i in data:
                manager_info[i[0]]='123456'
            pickle.dump(manager_info, usr_file)
    if usr_name in manager_info:
        if usr_pwd == manager_info[usr_name]:
            # messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
            window_login = Toplevel(window)
        else:
            messagebox.showerror(message='登录密码错误,请重新输入')
    else:
        messagebox.showerror(message='该用户名不存在,请重新输入')
    window_login.geometry('700x400')
    window_login.title('人事管理系统')    
    Button(window_login, text='员工信息',command=employee).place(x=120,y=0,height=80,width=160)
    Button(window_login, text='部门信息',command=department).place(x=120,y=100,height=80,width=160)
    Button(window_login, text='项目信息',command=project).place(x=120,y=200,height=80,width=160)
    Button(window_login, text='工作记录信息',command=works_on).place(x=120,y=300,height=80,width=160)
    Label(window_login, text='1：查询参加了某项目的所有员工名字').place(x=300, y=0)
    global entryt1,entryt21,entryt22,entryt4,entryt51,entryt52
    Label(window_login, text='项目名').place(x=300, y= 30)    
    entryt1=Entry(window_login)
    entryt1.place(x=350, y= 30)
    Button(window_login, text='查询',command=cx1).place(x=500,y=30)
    Label(window_login, text='2：查询在某部门名工作且工资低于多少元的员工名字和地址').place(x=300, y= 60)
    Label(window_login, text='部门名').place(x=300, y= 90)    
    entryt21=Entry(window_login)
    entryt21.place(x=360, y= 90,width=50)
    Label(window_login, text='工资小于').place(x=420, y= 90)    
    entryt22=Entry(window_login)
    entryt22.place(x=480, y= 90,width=50)
    Button(window_login, text='查询',command=cx2).place(x=540,y=90)
    Label(window_login, text='3：每个部门的员工平均工资').place(x=300, y= 120)
    Button(window_login, text='查询',command=cx3).place(x=300,y=150)
    Label(window_login, text='4：由某领导的工作人员的姓名和所在部门的名字').place(x=300, y= 180)
    Label(window_login, text='领导名').place(x=300, y= 210)    
    entryt4=Entry(window_login)
    entryt4.place(x=350, y= 210)
    Button(window_login, text='查询',command=cx4).place(x=500,y=210)
    Label(window_login, text='5：查询参加了项目编号为 P1 和 P2 的项目的员工号').place(x=300, y= 240)
    Label(window_login, text='项目编号1').place(x=300, y= 270)    
    entryt51=Entry(window_login)
    entryt51.place(x=360, y= 270,width=50)
    Label(window_login, text='项目编号2').place(x=420, y= 270)    
    entryt52=Entry(window_login)
    entryt52.place(x=480, y= 270,width=50)
    Button(window_login, text='查询',command=cx5).place(x=540,y=270)
    Label(window_login, text='6：至少参与了 3 个项目且工作总时间不超过 8 小时的员工名字').place(x=300, y= 300)
    Button(window_login, text='查询',command=cx6).place(x=300,y=330)

#employee
def employeecx():    
    a,b,c,d,e,f=entrye1.get(),entrye2.get(),entrye3.get(),entrye4.get(),entrye5.get(),entrye6.get()
    if a=="":
        a='is not null'
    else:
        a='=\''+str(a)+'\''
    if b=="":
        b='is not null'
    else:
        b='=\''+str(b)+'\''
    if c=="":
        c='is not null'
    else:
        c='=\''+str(c)+'\''
    if d=="":
        d='is not null'
    else:
        d='=\''+str(d)+'\''
    if e=="":
        e='is not null'
    else:
        e='=\''+str(e)+'\''
    if f=="":
        f='is not null'
    else:
        f='=\''+str(f)+'\''  
    sql="select * from employee where ESSN %s and ENAME %s and ADDRESS %s and SALARY %s and SUPERSSN %s and DNO %s"%(a,b,c,d,e,f)
    print(sql)
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*25
        a.append(m)
    lb1.delete(0,END)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)

def employeezj():    
    a,b,c,d,e,f=entrye1.get(),entrye2.get(),entrye3.get(),entrye4.get(),entrye5.get(),entrye6.get()
    if(a=='' or b==''or c=='' or d==''or e==''or f==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        with open('manager_info.pickle', 'rb') as usr_file:
            manager_info = pickle.load(usr_file)
        with open('manager_info.pickle', 'wb') as usr_file:
            manager_info[a]='123456'
            pickle.dump(manager_info, usr_file)
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        e='\''+str(e)+'\''
        f='\''+str(f)+'\''        
        sql="insert into employee (ESSN,ENAME,ADDRESS,SALARY,SUPERSSN,DNO) values (%s,%s,%s,%s,%s,%s)"%(a,b,c,d,e,f)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from employee"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def employeexg():
    a,b,c,d,e,f=entrye1.get(),entrye2.get(),entrye3.get(),entrye4.get(),entrye5.get(),entrye6.get()
    if(a=='' or b==''or c=='' or d==''or e==''or f==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        e='\''+str(e)+'\''
        f='\''+str(f)+'\''
        sql="update employee set ENAME=%s,ADDRESS=%s,SALARY=%s,SUPERSSN=%s,DNO=%s where essn=%s"%(b,c,d,e,f,a)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from employee"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def employeesc():
    a,b,c,d,e,f=entrye1.get(),entrye2.get(),entrye3.get(),entrye4.get(),entrye5.get(),entrye6.get()
    if(a==''and b==''and c=='' and d==''and e==''and f==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        if a=="":
            a='is not null'
        else:
            a='=\''+str(a)+'\''
        if b=="":
            b='is not null'
        else:
            b='=\''+str(b)+'\''
        if c=="":
            c='is not null'
        else:
            c='=\''+str(c)+'\''
        if d=="":
            d='is not null'
        else:
            d='=\''+str(d)+'\''
        if e=="":
            e='is not null'
        else:
            e='=\''+str(e)+'\''
        if f=="":
            f='is not null'
        else:
            f='=\''+str(f)+'\'' 
        sql="delete from employee where ESSN %s and ENAME %s and ADDRESS %s and SALARY %s and SUPERSSN %s and DNO %s"%(a,b,c,d,e,f)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from employee"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def employee(): 
    global window_employee
    window_employee = Tk()
    window_employee.geometry('700x600')
    window_employee.title('员工信息管理系统') 
    Label(window_employee,text="员工号\t\t      姓名\t\t        地址\t            工资\t\t  领导号\t\t   部门号").place(x=0,y=0)
    Label(window_employee,text='员工号').place(x=200,y=360)
    Label(window_employee,text='姓名').place(x=200,y=400)
    Label(window_employee,text="地址").place(x=200,y=440)
    Label(window_employee,text="工资").place(x=200,y=480)
    Label(window_employee,text="领导号").place(x=200,y=520)
    Label(window_employee,text="部门号").place(x=200,y=560)
    global entrye1,entrye2,entrye3,entrye4,entrye5,entrye6
    entrye1=Entry(window_employee)
    entrye1.place(x=250,y=360)
    entrye2=Entry(window_employee)
    entrye2.place(x=250,y=400) 
    entrye3=Entry(window_employee)
    entrye3.place(x=250,y=440)
    entrye4=Entry(window_employee)
    entrye4.place(x=250,y=480)
    entrye5=Entry(window_employee)
    entrye5.place(x=250,y=520)
    entrye6=Entry(window_employee)
    entrye6.place(x=250,y=560)
    sql = "select * from employee"
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*25
        a.append(m)
    global lb1
    lb1 = Listbox(window_employee)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)
    Button(window_employee,text='查询',command=employeecx).place(x=450,y=400,width=80)
    Button(window_employee,text='增加',command=employeezj).place(x=450,y=440,width=80)
    Button(window_employee,text='修改',command=employeexg).place(x=450,y=480,width=80)
    Button(window_employee,text='删除',command=employeesc).place(x=450,y=520,width=80)
    
#department
def departmentcx():    
    a,b,c,d=entryd1.get(),entryd2.get(),entryd3.get(),entryd4.get()
    if a=="":
        a='is not null'
    else:
        a='=\''+str(a)+'\''
    if b=="":
        b='is not null'
    else:
        b='=\''+str(b)+'\''
    if c=="":
        c='is not null'
    else:
        c='=\''+str(c)+'\''
    if d=="":
        d='is not null'
    else:
        d='=\''+str(d)+'\''  
    sql="select * from department where DNO %s and DNAME %s and MGRSSN %s and MGRSTARTDATE %s"%(a,b,c,d)
    print(sql)
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*25
        a.append(m)
    lb1.delete(0,END)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)

def departmentzj():    
    a,b,c,d=entryd1.get(),entryd2.get(),entryd3.get(),entryd4.get()
    if(a=='' or b==''or c=='' or d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        sql="insert into department values (%s,%s,%s,%s)"%(a,b,c,d)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from department"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def departmentxg():
    a,b,c,d=entryd1.get(),entryd2.get(),entryd3.get(),entryd4.get()
    if(a=='' or b==''or c=='' or d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        sql="update department set DNAME=%s,MGRSSN=%s,MGRSTARTDATE=%s where DNO=%s"%(b,c,d,a)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from department"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def departmentsc():
    a,b,c,d=entryd1.get(),entryd2.get(),entryd3.get(),entryd4.get()
    if(a==''and b==''and c=='' and d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        if a=="":
            a='is not null'
        else:
            a='=\''+str(a)+'\''
        if b=="":
            b='is not null'
        else:
            b='=\''+str(b)+'\''
        if c=="":
            c='is not null'
        else:
            c='=\''+str(c)+'\''
        if d=="":
            d='is not null'
        else:
            d='=\''+str(d)+'\''
        sql="delete from department where DNO %s and DNAME %s and MGRSSN %s and MGRSTARTDATE %s"%(a,b,c,d)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from department"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*25
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def department(): 
    global window_department
    window_department = Tk()
    window_department.geometry('700x600')
    window_department.title('部门信息管理系统') 
    Label(window_department,text="部门号\t\t      部门名\t\t      领导编号\t \t      领导上任日期").place(x=0,y=0)
    Label(window_department,text='部门号').place(x=200,y=360)
    Label(window_department,text='部门名').place(x=200,y=400)
    Label(window_department,text="领导编号").place(x=200,y=440)
    Label(window_department,text="领导上任日期").place(x=160,y=480)
    global entryd1,entryd2,entryd3,entryd4
    entryd1=Entry(window_department)
    entryd1.place(x=250,y=360)
    entryd2=Entry(window_department)
    entryd2.place(x=250,y=400) 
    entryd3=Entry(window_department)
    entryd3.place(x=250,y=440)
    entryd4=Entry(window_department)
    entryd4.place(x=250,y=480)
    sql = "select * from department"
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*32
        a.append(m)
    global lb1
    lb1 = Listbox(window_department)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)
    Button(window_department,text='查询',command=departmentcx).place(x=450,y=360,width=80)
    Button(window_department,text='增加',command=departmentzj).place(x=450,y=400,width=80)
    Button(window_department,text='修改',command=departmentxg).place(x=450,y=440,width=80)
    Button(window_department,text='删除',command=departmentsc).place(x=450,y=480,width=80)
    
#project
def projectcx():    
    a,b,c,d=entryp1.get(),entryp2.get(),entryp3.get(),entryp4.get()
    if a=="":
        a='is not null'
    else:
        a='=\''+str(a)+'\''
    if b=="":
        b='is not null'
    else:
        b='=\''+str(b)+'\''
    if c=="":
        c='is not null'
    else:
        c='=\''+str(c)+'\''
    if d=="":
        d='is not null'
    else:
        d='=\''+str(d)+'\''  
    sql="select * from project where PNO %s and PNAME %s and PLOCATION %s and DNO %s"%(a,b,c,d)
    print(sql)
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*36
        a.append(m)
    lb1.delete(0,END)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)

def projectzj():    
    a,b,c,d=entryp1.get(),entryp2.get(),entryp3.get(),entryp4.get()
    if(a=='' or b==''or c=='' or d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        sql="insert into project values (%s,%s,%s,%s)"%(a,b,c,d)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from project"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def projectxg():
    a,b,c,d=entryp1.get(),entryp2.get(),entryp3.get(),entryp4.get()
    if(a=='' or b==''or c=='' or d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        d='\''+str(d)+'\''
        sql="update project set PNAME=%s,PLOCATION=%s,DNO=%s where PNO=%s"%(b,c,d,a)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from project"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def projectsc():
    a,b,c,d=entryp1.get(),entryp2.get(),entryp3.get(),entryp4.get()
    if(a==''and b==''and c=='' and d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        if a=="":
            a='is not null'
        else:
            a='=\''+str(a)+'\''
        if b=="":
            b='is not null'
        else:
            b='=\''+str(b)+'\''
        if c=="":
            c='is not null'
        else:
            c='=\''+str(c)+'\''
        if d=="":
            d='is not null'
        else:
            d='=\''+str(d)+'\''
        sql="delete from project where PNO %s and PNAME %s and PLOCATION %s and DNO %s"%(a,b,c,d)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from project"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def project(): 
    global window_project
    window_project = Tk()
    window_project.geometry('700x600')
    window_project.title('项目信息管理系统') 
    Label(window_project,text="项目号\t\t      项目名\t\t      项目地址\t \t      所属部门号").place(x=0,y=0)
    Label(window_project,text='项目号').place(x=200,y=360)
    Label(window_project,text='项目名').place(x=200,y=400)
    Label(window_project,text="项目地址").place(x=200,y=440)
    Label(window_project,text="所属部门号").place(x=180,y=480)
    global entryp1,entryp2,entryp3,entryp4
    entryp1=Entry(window_project)
    entryp1.place(x=250,y=360)
    entryp2=Entry(window_project)
    entryp2.place(x=250,y=400) 
    entryp3=Entry(window_project)
    entryp3.place(x=250,y=440)
    entryp4=Entry(window_project)
    entryp4.place(x=250,y=480)
    sql = "select * from project"
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*36
        a.append(m)
    global lb1
    lb1 = Listbox(window_project)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)
    Button(window_project,text='查询',command=projectcx).place(x=450,y=360,width=80)
    Button(window_project,text='增加',command=projectzj).place(x=450,y=400,width=80)
    Button(window_project,text='修改',command=projectxg).place(x=450,y=440,width=80)
    Button(window_project,text='删除',command=projectsc).place(x=450,y=480,width=80)
    
#works_on
def works_oncx():    
    a,b,c=entryp1.get(),entryp2.get(),entryp3.get()
    if a=="":
        a='is not null'
    else:
        a='=\''+str(a)+'\''
    if b=="":
        b='is not null'
    else:
        b='=\''+str(b)+'\''
    if c=="":
        c='is not null'
    else:
        c='=\''+str(c)+'\'' 
    sql="select * from works_on where ESSN %s and PNO %s and HOURS %s "%(a,b,c)
    print(sql)
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*36
        a.append(m)
    lb1.delete(0,END)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)

def works_onzj():    
    a,b,c=entryp1.get(),entryp2.get(),entryp3.get()
    if(a=='' or b==''or c=='' or d==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        
        sql="insert into works_on values (%s,%s,%s)"%(a,b,c)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from works_on"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def works_onxg():
    a,b,c=entryp1.get(),entryp2.get(),entryp3.get()
    if(a=='' or b==''or c==''):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        a='\''+str(a)+'\''
        b='\''+str(b)+'\''
        c='\''+str(c)+'\''
        
        sql="update works_on set PNO=%s,HOURS=%s where ESSN=%s"%(b,c,a)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from works_on"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def works_onsc():
    a,b,c=entryp1.get(),entryp2.get(),entryp3.get()
    if(a==''and b==''and c=='' ):
        messagebox.showerror(message='信息未填写完整,请继续填写')
    else:
        if a=="":
            a='is not null'
        else:
            a='=\''+str(a)+'\''
        if b=="":
            b='is not null'
        else:
            b='=\''+str(b)+'\''
        if c=="":
            c='is not null'
        else:
            c='=\''+str(c)+'\''
        sql="delete from works_on where ESSN %s and PNO %s and HOURS %s "%(a,b,c)
        print(sql)
        cursor.execute(sql)
        db.commit()  #提交数据
        sql="select * from works_on"
        print(sql)
        cursor.execute(sql)
        data=list(cursor.fetchall())
        a=[]
        for i in data:
            m=''
            for j in i:
                m=m+str(j)+' '*36
            a.append(m)
        lb1.delete(0,END)
        for each in a:
            lb1.insert(END, each)
        lb1.place(x=0,y=50,height=280,width=700)

def works_on(): 
    global window_works_on
    window_works_on = Tk()
    window_works_on.geometry('700x600')
    window_works_on.title('工作时间信息管理系统') 
    Label(window_works_on,text="员工号\t\t\t项目号\t\t        工作时间").place(x=0,y=0)
    Label(window_works_on,text='员工号').place(x=200,y=360)
    Label(window_works_on,text='项目号').place(x=200,y=420)
    Label(window_works_on,text="工作时间").place(x=200,y=480)
    global entryp1,entryp2,entryp3
    entryp1=Entry(window_works_on)
    entryp1.place(x=250,y=360)
    entryp2=Entry(window_works_on)
    entryp2.place(x=250,y=420) 
    entryp3=Entry(window_works_on)
    entryp3.place(x=250,y=480)
    sql = "select * from works_on"
    cursor.execute(sql)
    data=list(cursor.fetchall())
    a=[]
    for i in data:
        m=''
        for j in i:
            m=m+str(j)+' '*36
        a.append(m)
    global lb1
    lb1 = Listbox(window_works_on)
    for each in a:
        lb1.insert(END, each)
    lb1.place(x=0,y=50,height=280,width=700)
    Button(window_works_on,text='查询',command=works_oncx).place(x=450,y=360,width=80)
    Button(window_works_on,text='增加',command=works_onzj).place(x=450,y=400,width=80)
    Button(window_works_on,text='修改',command=works_onxg).place(x=450,y=440,width=80)
    Button(window_works_on,text='删除',command=works_onsc).place(x=450,y=480,width=80)




# cursor.close()
# db.close()

config={
    "host":"127.0.0.1",
    "user":"root",
    "password":"",
    "database":"company"
}
db = pymysql.connect(**config)
cursor = db.cursor()


#主窗口设置
window = Tk()
window.title('人事系统登录')
window.geometry('450x350')
# 加welcome,label,entry
canvas = Canvas(window, height=200, width=500)
image_file = PhotoImage(file='welcome.gif')
image = canvas.create_image(0,0, anchor='nw', image=image_file)
canvas.pack(side='top')
Label(window, text='User name: ').place(x=50, y= 150)
Label(window, text='Password: ').place(x=50, y= 190)
var_usr_name = StringVar()
entry_usr_name = Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=150)
var_usr_pwd = StringVar()
entry_usr_pwd = Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=190)
var_usr_name.set('员工SSN或admin')
# var_usr_name.set('admin')
# var_usr_pwd.set('admin')
# login 
btn_login = Button(window, text='登录', command=usr_login)
btn_login.place(x=200, y=230)
Label(window, text='注:管理员登录用户账号密码均为admin\n员工登录用户名为员工SSN,密码为123456\n管理员可以进行查询以及增删改,\n用户只能进行查询').place(x=80, y=280)
window.mainloop()