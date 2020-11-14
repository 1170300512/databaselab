from tkinter import *
from tkinter import messagebox
import pickle
import pymysql
#登录新界面
def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {}
            sql = "select ESSN from employee"
            cursor.execute(sql)
            data=list(cursor.fetchall())
            for i in data:
                usrs_info[i[0]]='123456'
            pickle.dump(usrs_info, usr_file)
    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            # messagebox.showinfo(title='Welcome', message='How are you? ' + usr_name)
            window_login = Toplevel(window)
        else:
            messagebox.showerror(message='登录密码错误,请重新输入')
    else:
        messagebox.showerror(message='该用户名不存在,请重新输入')
    window_login.geometry('400x400')
    window_login.title('人事管理系统')    
    Button(window_login, text='员工信息',command=employee).place(x=120,y=0,height=80,width=160)
    Button(window_login, text='部门信息',command=department).place(x=120,y=100,height=80,width=160)
    Button(window_login, text='项目信息',command=project).place(x=120,y=200,height=80,width=160)
    Button(window_login, text='工作记录信息',command=works_on).place(x=120,y=300,height=80,width=160)

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





