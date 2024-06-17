from flask import Flask, render_template, request, redirect,session
from lib import run_query
from data import book,student, issue,admin,history
from flask_session import Session
from functools import wraps
from datetime import date as date_n
from flask_apscheduler import APScheduler


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False

app.config["SESSION_TYPE"] = "filesystem"
Session(app)
#crontab=Crontab(app)
scheduler=APScheduler()


'''
var=0
var1=str(var)
class DataStore():
    username=None
data=DataStore()
'''

def admin_login_required(funct, *args, **kwargs):
    @wraps(funct)
    def inner():
        if session.get('user', 'unknown') == 'unknown':
            return redirect('/admin_login')
        elif session.get('user','unknown') == 'student':
            return redirect('/')
        return funct(*args, **kwargs)
    
    return inner


def login_required(funct,*args, **kwargs):
    @wraps(funct)
    def inner():
        if session.get('user', 'unknown') == 'unknown':
            return redirect('/')
        return funct(*args, **kwargs)
    
    return inner


@app.route('/') 
def home():
    
    return render_template('index.html')


@app.route('/student_login', methods = ("GET", "POST"))
def student_login():
    # load add form after inserting or routing
    if request.method=="POST":
        username=request.form.get("uname")
        password=request.form.get("psw")
        session["username"]="username"
       # data.username=username
        status=run_query(f'select count(*) from student where "USER ID"="{username}" and "PASSWORD"="{password}";')[0][0]
        if(status==1):
            session["user"] = "student"
            session["username"] = username
            return redirect('/student_details')
            #cmd = run_query(f'select * from issue where "USER ID"="{username}";')
            #run_query(f'select * from issue where "USER ID"={username};')
            #return(cmd)
    return render_template('student_login.html')


@app.route('/admin_login', methods = ("GET", "POST"))
def admin_login():
    # load add form after inserting or routing
    if request.method=="POST":
        username=request.form.get("uname")
        password=request.form.get("psw")
        status=run_query(f'select count(*) from admin where "USER ID"="{username}" and "PASSWORD"="{password}";')[0][0]
        if(status==1):
            session["user"] = "admin"
            session["username"] = username
            return redirect('/dashboard')

    return render_template('admin_login.html')


@app.route('/logout')
def logout():
    session['user']=session['username']='unknown'
    return redirect('/')


@app.route('/dashboard')
@admin_login_required
def dash_board():
    return render_template('dashboard.html')


@app.route('/books',methods=('GET','POST'))
def book_list():
    if request.method=="POST":
        sb=request.form.get("BOOK NAME")
        run_query(f"select * from book where 'BOOK NAME'='{sb}';")

    #to display all the available books
    books=run_query('select * from book order by "DEPARTMENT";')
    return render_template(
                'booklist.html', 
                books = books,
                fields=book['keys'],
                user_type=session.get('user','unknown')
            )
   # result and performance analysis  
         
         
'''
@app.route('/search',methods=('GET','POST'))
def book_list():
    if request.method=="POST":
        sb=request.form.get("BOOK NAME")
        run_query(f"select * from book where 'BOOK NAME'='{sb}';")
    return render_template('booklist.html',)   
'''


@app.route('/add_book',methods=['POST','GET'])
@admin_login_required
def add_book():
    #to add a book 
    if request.method=='POST':
        book_id=request.form.get('BOOK CODE')
        book_name=request.form.get('BOOK NAME')
        author_name=request.form.get('AUTHOR NAME')
        edition=request.form.get('EDITION')
        dept=request.form.get('DEPARTMENT')
        no_of_books=request.form.get('NO OF BOOKS')
        cmd=f"insert into book values('{book_id}','{book_name}','{author_name}','{edition}','{dept}','{no_of_books}');"
        
        run_query(cmd)
        return redirect('/books')

    return render_template('addbook.html',fields=book['keys'])


@app.route('/delete_book',methods=['POST','GET'])
@admin_login_required
def delete_book():
    if request.method=="POST":
        book_id=request.form.get('BOOK CODE')
        cmd=f'delete from book where "BOOK CODE"={book_id};'
        #print(cmd)
        run_query(cmd)
        return redirect('/books')


@app.route('/users')
@admin_login_required
def student_list():
    #to display all users
    students=run_query('select * from student;')
    return render_template('userlist.html', students = students,fields=student['keys'])


@app.route('/add_user',methods=['GET','POST'])
@admin_login_required
def add_user():
    #to add user
    if request.method=='POST':
        user_id=request.form.get('USER ID')
        password=request.form.get('PASSWORD')
        full_name=request.form.get('FULL NAME')
        dept=request.form.get('DEPARTMENT')
        mbl=request.form.get('MOBILE NUMBER')
        fine=request.form.get('FINE')
        cmd=f"insert into student values('{user_id}','{password}','{full_name}','{dept}','{mbl}',{fine});"

        run_query(cmd)
        return redirect('/users')
    return render_template('adduser.html',fields=student['keys'])


@app.route('/add_admin',methods=['GET','POST'])
@admin_login_required
def add_admin():
    #to add use admin
    if request.method=='POST':
        user_id=request.form.get('USER ID')
        full_name=request.form.get('ADMIN NAME')
        password=request.form.get('PASSWORD')
        cmd=f"insert into admin values('{user_id}','{full_name}','{password}');"
 
        run_query(cmd)
        return redirect('/admins')
    return render_template('add_admin.html',fields = admin['keys'])


@app.route('/admins')
@admin_login_required
def admin_list():
    lists=run_query('select * from admin;')
    return render_template('admin_list.html', lists = lists,fields=admin['keys'])


@app.route('/delete_admin',methods=['POST','GET'])
@admin_login_required
def delete_admin():

    if request.method=="POST":
        user=request.form.get('USER ID')
        cmd=f'delete from admin where "USER ID"="{user}";'
       # print(cmd)
        run_query(cmd)
        return redirect('/admins')


@app.route('/delete_user',methods=['POST','GET'])
@admin_login_required
def delete_user():

    if request.method=="POST":
        user=request.form.get('USER ID')
        cmd=f'delete from student where "USER ID"="{user}";'
       # print(cmd)
        run_query(cmd)
        return redirect('/users')


@app.route('/issue_book',methods=['GET','POST'])
@admin_login_required
def issue_book():
    # command for listing the books for drop down menu
    cmd=f'select "BOOK CODE" from book where "NO OF BOOKS">0;'
    books=run_query(cmd)
    #print(books)
     # command for listing the users for drop down menu
    cmd=f'select "USER ID" from student;'
    students=run_query(cmd)
    if request.method=="POST":
        user_id=request.form.get('USER ID')
        book_code=request.form.get('BOOK ID')
        issue_date=request.form.get('ISSUE DATE')
        session["issuedate"]=issue_date
        k=run_query(f'select "NO OF BOOKS" from book where "BOOK CODE"={book_code};')[0][0]
        
        # inserting into issue database
        run_query(f"insert into issue('USER ID','BOOK ID','ISSUE DATE') values('{user_id}','{book_code}','{issue_date}');")
    
        #inserting into history database
        run_query(f'insert into history("USER_ID","BOOK_ID","ISSUE_DATE","STATUS") values ("{user_id}","{book_code}","{issue_date}","ISSUED");')

        #decrementing book count by 1
        k-=1
        upd=f'update book set "NO OF BOOKS"= {k} where "BOOK CODE"={book_code};'
        run_query(upd)
        

        return redirect('/issues')
    return render_template('issue.html',books=books,students=students)

@app.route('/issues')
#@admin_login_required
def issue_list():
    #to display all the available books
    issues=run_query('select * from issue;')
    return render_template('issue list.html', issues = issues,fields=issue['keys'])


@app.route('/return',methods=['GET','POST'])
@admin_login_required
def return_book():
    # cmd=f'select "BOOK CODE" from book where "NO OF BOOKS">=0;'
    # books=run_query(cmd)
       
    # cmd=f'select "USER ID" from student;'
    # students=run_query(cmd)
    
    # book id of only currently issued books
    books = run_query('SELECT DISTINCT "BOOK ID" FROM issue;') 

    # user id of only currently issued books
    students = run_query('SELECT DISTINCT "USER ID" FROM issue;')
    
    if request.method=="POST":
        user_id=request.form.get('USER ID')
        book_id=request.form.get('BOOK ID')
        return_date=request.form.get('RETURN DATE')
        session["returndate"]=return_date
        issue_id =run_query(f'select "ISSUE ID" from issue where "USER ID"="{user_id}" and "BOOK ID"={book_id};')[0][0]
        print(issue_id)
        run_query(f'delete from issue where "ISSUE ID"={issue_id};')
        
        k=run_query(f'select "NO OF BOOKS" from book where "BOOK CODE"={book_id};')[0][0]
        k+=1
        run_query(f'update book set "NO OF BOOKS"={k} where "BOOK CODE"={book_id};')
        
        run_query(f'update history set "STATUS"="RETURNED", "RETURN_DATE"="{return_date}" where "ISSUE_ID"={issue_id};')

       # run_query(f'')
        return redirect('/issues')
    return render_template('return.html',books=books,students=students)



def fine_collection(issue_date,issue_id, user_id):
    x=issue_date.split('-')
    yy,mm,dd=map(int,x)
    issue_date = date_n(yy, mm, dd)
    today_date=date_n.today()

    k=(today_date - issue_date).days


    if k>=30:
        fine=run_query(f'select "fine" from history where "ISSUE_ID"={issue_id};')[0][0]
        cmd = f'update history set "fine"={fine+5} where "ISSUE_ID"={issue_id};'
        run_query(cmd)

        cmd = f'select "fine" from student where "USER ID"={user_id};'
        fine=run_query(cmd)[0][0]
        
        run_query(f'update student set "FINE"={fine+5} where "USER ID"={user_id};')
        
    #print(k, "hello", issue_date, issue_id)

def fine_calculation():
    data=run_query(f'select "ISSUE DATE","ISSUE ID", "USER ID" from issue;')

    for issue in data:
        fine_collection(issue[0],issue[1], issue[2])
        print()




@app.route('/student_details')
@login_required
def details():
    issues=run_query(f'select * from history where "USER_ID" = "{session["username"]}";')
    #issues=run_query(f'select * from history')
    return render_template('history.html', issues = issues, fields=history['keys'])

'''
@app.route('/history')
@admin_login_required
def history():
    issues=run_query(f'select * from history;')
    #issues=run_query(f'select * from history')
    return render_template('history.html', issues = issues, fields=history['keys'])

    
    user_id=session.get('user_name')
    print(user_id)
    issues=run_query(f"select * from issue where 'USER ID'='{user_id}';")
    return render_template('issue list.html', issues = issues,fields=issue['keys'],user_id=user_id)
    
    #return redirect('/issues')
    '''
    

if __name__ == "__main__":
    scheduler.add_job(id="fine",func=fine_calculation,trigger="interval",seconds=86400)
    scheduler.start()
    app.run(debug = True)