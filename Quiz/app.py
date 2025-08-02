from flask import Flask, render_template,request , flash,url_for,redirect
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text
from models.models import Admin, User, Score,Subject,Chapter,Quiz,Question
from models import db
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app=Flask(__name__)
app.secret_key='aksh03key11sec'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'

db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    value=request.args.get('submit_button')
    if value=="Admin page":
        return render_template("admin_login.html")
    elif value=="User page"  :
        return render_template("user_login.html")


@app.route("/admin_page", methods=['POST'])
def admin_page():
    admin_user=request.form.get('admin_username')
    admin_password=request.form.get('admin_password')
    row = Admin.query.filter_by(Admin_id=admin_user).first()
    if row:
        if(admin_user==row.Admin_id and admin_password==row.Admin_password ):
            subjects = Subject.query.all()
            return render_template("admin_dashboard.html",subjects=subjects)
        else:
            alert_msg="Invalid username or password"
            return render_template("admin_login.html",alert_msg=alert_msg)
    else:
        alert_msg="Invalid username or password..."
        return render_template("admin_login.html",alert_msg=alert_msg)

@app.route("/back_admin_dashboard_login")
def back_admin_dashboard_login():
    return render_template("home.html")

@app.route("/create_subject")
def create_subject():
    return render_template('create_subject.html')

@app.route("/create_chapters" , methods=['POST'])
def create_chapters():
    subject_name=request.form.get('subject_name')
    subject_code=request.form.get('subject_code')
    subject_description=request.form.get('subject_description',None)
    present = Subject.query.filter_by(Subject_id=subject_code).first()
    if not present:  
        new_subject = Subject(Subject_id=subject_code, Subject_name=subject_name, Description=subject_description,No_of_chapters_inside=0)
        db.session.add(new_subject)
        db.session.commit()
        return render_template("create_chapter.html",subject_name=subject_name,subject_id=subject_code)
    else:
        flash("Subject already exists! Please choose a different Subject ID.", "error")
        return redirect(url_for("create_subject"))

@app.route("/create_chapter_subject/<subject_id>/<subject_name>")
def create_chapter_subject(subject_id,subject_name):
    chapters = Chapter.query.filter_by(Subject_id=subject_id).all()
    return render_template("create_chapter.html",subject_name=subject_name,subject_id=subject_id,chapters=chapters)

@app.route("/back_create_chapter_admin_dashboard/")
def back_create_chapter_admin_dashboard():
    subjects = Subject.query.all()
    return render_template("admin_dashboard.html",subjects=subjects)

@app.route("/add_quizzes_chapter/<chapter_id>/<chapter_name>")
def add_quizzes_chapter(chapter_id,chapter_name):
    quizzes=Quiz.query.filter_by(Chapter_id=chapter_id)
    subject_id=Chapter.query.filter_by(Chapter_id=chapter_id).first().Subject_id
    return render_template("create_quiz.html",chapter_name=chapter_name,subject_id=subject_id,chapter_id=chapter_id,quizzes=quizzes)
    

@app.route("/create_quiz",methods=['POST'])
def create_quiz():
    subject_id=request.args.get('subject_id')
    subject_name=request.args.get('subject_name')
    chapter_name=request.form.get('chapter_name')
    chapter_id=request.form.get('chapter_id')
    description=request.form.get('description',None)
    chap = Chapter.query.filter_by(Chapter_id=chapter_id).first()

    if not chap:
        new_chapter = Chapter(
            Chapter_id=chapter_id,
            Chapter_name=chapter_name,
            Description=description,
            Subject_id=subject_id
        )
        db.session.add(new_chapter)
        subject = Subject.query.filter_by(Subject_id=subject_id).first()
        subject.No_of_chapters_inside += 1  
        db.session.commit() 
        return render_template("create_quiz.html",subject_id=subject_id,chapter_name=chapter_name,chapter_id=chapter_id)
    else:
        flash("Chapter already exists! Please choose a different Chapter ID.", "error")
        return redirect(url_for("create_chapter_subject",subject_id=subject_id,subject_name=subject_name))

@app.route("/back_create_quiz_create_chapter/<subject_id>")
def back_create_quiz_create_chapter(subject_id):
    subject_name=Subject.query.filter_by(Subject_id=subject_id).first().Subject_name
    chapters=Chapter.query.filter_by(Subject_id=subject_id).all()   
    return render_template("create_chapter.html",subject_name=subject_name,subject_id=subject_id,chapters=chapters)

@app.route("/add_question",methods=['POST'])
def add_question():
    print("ok")
    chapter_id=request.args.get('chapter_id')
    quiz_id=request.args.get('quiz_id')
    quiz_name=request.args.get('quiz_name')
    duration=request.args.get('duration')
    question=request.form.get('question')
    chapter_name=request.args.get('chapter_name')
    subject_id=request.args.get('subject_id')
    opt1=request.form.get('opt1')
    opt2=request.form.get('opt2')
    opt3=request.form.get('opt3')
    opt4=request.form.get('opt4')
    correct_option=request.form.get('correct_option')
    existing_quiz = Quiz.query.filter_by(Quiz_id=quiz_id).first()
    if not existing_quiz:
        new_quiz = Quiz(
            Quiz_id=quiz_id,
            Quiz_name=quiz_name,
            Chapter_id=chapter_id,
            Time_duration=duration,
            No_of_Questions=1 
        )
        db.session.add(new_quiz)

    new_question = Question(
        Quiz_id=quiz_id,
        Question_Statement=question,
        Option1=opt1,
        Option2=opt2,
        Option3=opt3,
        Option4=opt4,
        Correct_option=correct_option
    )
    db.session.add(new_question)
    db.session.commit() 

    if new_question in db.session:
        quiz = Quiz.query.filter_by(Quiz_id=quiz_id).first()
        if quiz:
            quiz.No_of_Questions += 1  
            db.session.commit()  

    return render_template('/create_quiz.html',quiz_id=quiz_id,quiz_name=quiz_name,duration=duration,chapter_name=chapter_name,chapter_id=chapter_id,subject_id=subject_id)


@app.route("/delete_subject/<subject_id>")
def delete_subject(subject_id):
    print(subject_id)
    sub=Subject.query.filter_by(Subject_id=subject_id).first()
    if sub:
        db.session.delete(sub)
        db.session.commit()
    subjects=Subject.query.all()
    return render_template("/admin_dashboard.html",subjects=subjects)

@app.route("/delete_chapter/<chapter_id>/<subject_id>/<subject_name>")
def delete_chapter(chapter_id,subject_id,subject_name):
    chap=Chapter.query.filter_by(Chapter_id=chapter_id).first()
    if chap:
        db.session.delete(chap)
        subject=Subject.query.filter_by(Subject_id=subject_id).first()
        subject.No_of_chapters_inside-=1  
        db.session.commit()
    chapters=Chapter.query.filter_by(Subject_id=subject_id).all()
    return render_template("create_chapter.html",subject_name=subject_name,subject_id=subject_id,chapters=chapters)

@app.route("/delete_quiz/<quiz_id>/<chapter_name>/<chapter_id>")
def delete_quiz(quiz_id,chapter_name,chapter_id):
    quiz=Quiz.query.filter_by(Quiz_id=quiz_id).first()
    if quiz:
        db.session.delete(quiz)
        db.session.commit()
    quizzes=Quiz.query.filter_by(Chapter_id=chapter_id).all()
    subject_id=Chapter.query.filter_by(Chapter_id=chapter_id).first().Subject_id

    return render_template("/create_quiz.html",chapter_name=chapter_name,chapter_id=chapter_id,quizzes=quizzes,subject_id=subject_id)

@app.route("/edit_subject/<subject_id>/<subject_name>")
def edit_subject(subject_id,subject_name):
    subject=Subject.query.filter_by(Subject_id=subject_id).first()
    return render_template("/edit_subject.html",subject=subject)


@app.route("/modify_subject",methods=['POST'])
def modify_subject():
    subject_id=request.form.get("subject_code")
    subject_name=request.form.get("subject_name")
    subject_description=request.form.get("subject_description")
    subject = Subject.query.filter_by(Subject_id=subject_id).first()

    if subject:
        subject.Subject_name = subject_name
        subject.Description = subject_description
        db.session.commit() 

    subjects = Subject.query.all()
    return render_template("admin_dashboard.html",subjects=subjects)

@app.route("/edit_chapter/<chapter_id>/<subject_name>/<subject_id>")
def edit_chapter(chapter_id,subject_name,subject_id):
    chapter=Chapter.query.filter_by(Chapter_id=chapter_id).first()
    return render_template("/edit_chapter.html",chapter=chapter,subject_name=subject_name,subject_id=subject_id)

@app.route("/modify_chapter/<subject_name>/<subject_id>",methods=['POST'])
def modify_chapter(subject_name,subject_id):
    chapter_id=request.form.get("chapter_id")
    chapter_name=request.form.get("chapter_name")
    description=request.form.get("description")
    
    chapter=Chapter.query.filter_by(Chapter_id=chapter_id).first()

    if chapter:
        chapter.Chapter_name=chapter_name
        chapter.Description=description
        db.session.commit()

    chapters=Chapter.query.filter_by(Subject_id=subject_id).all()
    return render_template("/create_chapter.html",subject_name=subject_name,subject_id=subject_id,chapters=chapters)


@app.route("/edit_quiz/<quiz_id>/<chapter_name>/<chapter_id>")
def edit_quiz(quiz_id,chapter_name,chapter_id):
    quiz=Quiz.query.filter_by(Quiz_id=quiz_id).first()
    return render_template("/edit_quiz.html",quiz=quiz,chapter_id=chapter_id,chapter_name=chapter_name)

@app.route("/modify_quiz/<chapter_name>/<chapter_id>",methods=['POST'])
def modify_quiz(chapter_name,chapter_id):
    quiz_name=request.form.get("quiz_name")
    quiz_id=request.form.get("quiz_id")
    quiz=Quiz.query.filter_by(Quiz_id=quiz_id).first()
    if quiz:
            quiz.Quiz_name=quiz_name
            db.session.commit()

    quizzes=Quiz.query.filter_by(Chapter_id=chapter_id).all()
    subject_id=Chapter.query.filter_by(Chapter_id=chapter_id).first().Subject_id
    return render_template("/create_quiz.html",chapter_name=chapter_name,chapter_id=chapter_id,quizzes=quizzes,subject_id=subject_id)

@app.route("/display_user")
def display_user():
    query = text("""
        SELECT user.User_id, Name, email, Phone_number, COUNT(Quiz_id) AS quiz_count, valid
        FROM user
        LEFT JOIN scores ON user.User_id = scores.User_id
        GROUP BY user.User_id, Name, email, Phone_number, valid
    """)
    result = db.session.execute(query).fetchall()
    #user = [dict(row) for row in result] 
    user = [row._asdict() for row in result]
    return render_template("/display_user.html",users=user)

@app.route("/block_user/<user_id>")
def block_user(user_id):
    present=User.query.filter_by(User_id=user_id).first()
    if present:
        present.valid=0
        db.session.commit()
    query = text("""
        SELECT user.User_id, Name, email, Phone_number, COUNT(Quiz_id) AS quiz_count, valid
        FROM user
        LEFT JOIN scores ON user.User_id = scores.User_id
        GROUP BY user.User_id, Name, email, Phone_number, valid
    """)
    result = db.session.execute(query).fetchall()
    user = [row._asdict() for row in result]   
    return render_template("/display_user.html",users=user)

@app.route("/unblock_user/<user_id>")
def unblock_user(user_id):
    present=User.query.filter_by(User_id=user_id).first()
    if present:
        present.valid=1
        db.session.commit()
    query = text("""
        SELECT user.User_id, Name, email, Phone_number, COUNT(Quiz_id) AS quiz_count, valid
        FROM user
        LEFT JOIN scores ON user.User_id = scores.User_id
        GROUP BY user.User_id, Name, email, Phone_number, valid
    """)
    result = db.session.execute(query).fetchall()
    user = [row._asdict() for row in result]   
    return render_template("/display_user.html",users=user)   

@app.route("/back_display_user_admin_dashboard")
def back_display_user_admin_dashboard():
    subjects=Subject.query.all()
    return render_template("/admin_dashboard.html",subjects=subjects)

@app.route("/user_login")
def user_login():
    userid=request.args.get('userid')
    password=request.args.get('password')
    user = User.query.filter_by(User_id=userid).first()

    if user:
        password_get = user.Password
        name = user.Name
        valid_get = user.valid

        subjects=Subject.query.all()
        if(password==password_get and valid_get==1):
            return render_template('/user_dashboard.html',name=user.Name,subjects=subjects,user_id=userid)
        else:
            alert_msg="Incorrect login credentials"
            return render_template('/user_login.html',alert_msg=alert_msg)
    else:
        alert_msg="Enter the valid username"
        return render_template('/user_login.html',alert_msg=alert_msg)


@app.route("/user_sign_up")
def user_sign_up():
    return render_template("user_sign_up.html")

@app.route("/user_enter")
def user_enter():
    name=request.args.get("name")
    email=request.args.get("email")
    phoneno=request.args.get("phoneno")
    username=request.args.get("username")
    password=request.args.get("password")
    
    new_user = User(
        User_id=username,
        Password=password,
        Name=name,
        email=email,
        Phone_number=phoneno,
        valid=1
        )

    db.session.add(new_user)
    db.session.commit() 
    
    return render_template("user_login.html")


@app.route("/chap_selection/<subjectid>/<subjectname>/<user_id>")
def chapselection(subjectid,subjectname,user_id):
    rows=Chapter.query.filter_by(Subject_id=subjectid).all()
    return render_template('/chapter_selection.html',subject=subjectname,chapters=rows,user_id=user_id)


@app.route("/quiz_page/<chap_id>/<chap_name>/<user_id>")
def quizselection(chap_id,chap_name,user_id):
    rows=Quiz.query.filter_by(Chapter_id=chap_id).all()
    return render_template("/quiz_page.html",chapter=chap_name,quizzes=rows,user_id=user_id,chapter_id=chap_id)

@app.route("/start_quiz/<quiz_id>/<user_id>")
def start_quiz(quiz_id,user_id):
    rows=Question.query.filter_by(Quiz_id=quiz_id).all()
    questions = [
    {
        "Quiz_id": q.Quiz_id,
        "Question_Statement": q.Question_Statement,
        "Option1": q.Option1,
        "Option2": q.Option2,
        "Option3": q.Option3,
        "Option4": q.Option4,
        "Correct_option": q.Correct_option
    }
    for q in rows
]

    duration_time=Quiz.query.filter_by(Quiz_id=quiz_id).first().Time_duration
    duration_format = datetime.strptime(duration_time, "%H:%M").time()
    duration=duration_format.hour*60+duration_format.minute

    return render_template("/start_quiz.html",questions=questions,user_id=user_id,quiz_id=quiz_id,duration=duration)

@app.route("/score_page/<mark>/<user_id>/<quiz_id>/<time_taken>")
def score_page(mark,user_id,quiz_id,time_taken):
    new_score = Score(User_id=user_id, Quiz_id=quiz_id, Score=mark)
    db.session.add(new_score)
    db.session.commit()
    return render_template("/score_page.html",mark=mark,time_taken=time_taken,user_id=user_id,quiz_id=quiz_id)

@app.route("/back_scores_quiz_page/<user_id>/<quiz_id>")
def back_scores_quiz_page(user_id,quiz_id):
    chap_id=Quiz.query.filter_by(Quiz_id=quiz_id).first().Chapter_id
    chap_name=Chapter.query.filter_by(Chapter_id=chap_id).first().Chapter_name
    quizzes=Quiz.query.filter_by(Chapter_id=chap_id).all()
    return render_template("/quiz_page.html",quizzes=quizzes,chapter=chap_name,chapter_id=chap_id,user_id=user_id)

@app.route("/profile/<user_id>")
def profile(user_id):
    user=User.query.filter_by(User_id=user_id).first()
    name=user.Name
    email=user.email
    phoneno=user.Phone_number
    return render_template("/user_profile.html",name=name,email=email,phoneno=phoneno,username=user_id)

@app.route('/submit_profile/<user_name>',methods=['POST'])
def submit_profile(user_name):
    name=request.form.get('name')
    email=request.form.get('email')
    phone_no=request.form.get('phoneno')
    user=User.query.filter_by(User_id=user_name).first()
    user.Name=name
    user.Phone_number=phone_no
    user.email=email
    db.session.commit()
    subjects=Subject.query.all()
    return render_template("user_dashboard.html",name=name,user_id=user_name,subjects=subjects)

@app.route("/summary/<user_id>")
def summary(user_id):
    data = db.session.query(Quiz.Quiz_name, Score.Score).join(Quiz, Score.Quiz_id == Quiz.Quiz_id).filter(Score.User_id == user_id).all()

    df = pd.DataFrame(data, columns=['Quiz_name', 'Score'])
    user_scores = df.groupby('Quiz_name')['Score'].max()

    plt.figure(figsize=(10, 10))
    user_scores.plot(kind='bar', color='skyblue')

    plt.title('Scores obtained so far')
    plt.xlabel('Quiz Name')
    plt.ylabel('Score')
    plt.grid(axis='y')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('summary.html', graph=graph_url,user_id=user_id)

@app.route("/back_chapter_selection_user_dashboard/<user_id>")
def back_chapter_selection_user_dashboard(user_id):
    name=User.query.filter_by(User_id=user_id).first().Name
    subjects=Subject.query.all()
    return render_template("user_dashboard.html",name=name,subjects=subjects,user_id=user_id)

@app.route("/back_quiz_page_chapter_selection/<user_id>/<chapter_id>")
def back_quiz_page_chapter_selection(user_id,chapter_id):
    result = Subject.query.join(Chapter).filter(Chapter.Chapter_id == chapter_id).first()

    if result:
        subject_name = result.Subject_name
        subject_id = result.Subject_id

    chapters=Chapter.query.filter_by(Subject_id=subject_id).all()
    return render_template("chapter_selection.html",chapters=chapters,subject=subject_name,user_id=user_id)

@app.route("/back_profilesummary_user_dashboard/<user_id>")
def back_profilesummary_user_dashboard(user_id):
    user_name=User.query.filter_by(User_id=user_id).first().Name
    subjects=Subject.query.all()
    return render_template('/user_dashboard.html',name=user_name,subjects=subjects,user_id=user_id)

if __name__=="__main__":
    
    with app.app_context():
        db.create_all()
        admin_id = "admin1"
        admin_password = "admin123*i"
        

        if not Admin.query.filter_by(Admin_id=admin_id).first():
            new_admin = Admin(Admin_id=admin_id, Admin_password=admin_password)
            db.session.add(new_admin)
            db.session.commit()        

    app.run(debug="True")
