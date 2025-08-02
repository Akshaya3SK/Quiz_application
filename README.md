# 🧠 DBMS-Based Quiz Management System

A Flask-powered web application for managing quizzes with features for admin and user roles. Built as a DBMS project, this app allows administrators to create subjects, chapters, quizzes, and questions, while users can register, take quizzes, and visualize their scores.

> ✅ **Project Completed: December 2024**  Under IIT Madras(IITM) guidance and reviews

---

## 🚀 Features

### 👩‍🏫 Admin Capabilities
- Secure login
- Create/edit/delete:
  - Subjects
  - Chapters
  - Quizzes
  - Questions
- View user data
- Block/unblock users

### 👩‍🎓 User Capabilities
- Sign up and log in
- Browse subjects and take quizzes
- View quiz performance summary (bar chart)
- Edit personal profile

### 📊 Visual Insights
- Uses Matplotlib to generate quiz score graphs for users.

## 🗃️ Database Design

SQLite is used for the backend. Tables include:

- `subjects`: Subject metadata
- `chapter`: Linked to subjects
- `quiz`: Linked to chapters
- `questions`: Linked to quizzes
- `user`: Registered users
- `admin`: Admin credentials
- `scores`: Stores user quiz scores

## 📁 Folder Structure

```
quiz-app/
├── app.py                      
├── requirements.txt          
├── static/                    
│   ├── admin_dashboard.css
│   ├── create_quiz.css
│   ├── user_login.css
│   └── ... (etc.)
├── templates/                 
│   ├── admin_dashboard.html
│   ├── user_login.html
│   ├── create_subject.html
│   └── ... (etc.)
├── models/                     
├── instance/                  


```
## 🛠️ Installation & Setup

### 1. Clone the Repository

git clone https://github.com/Akshaya3SK/Quiz_application.git
cd Quiz_application


### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate   #On windows


### 3. Install Dependencies
pip install -r requirements.txt


### 4. Run the Application
python app.py


### 🔐 Admin Credentials (Default)

Username: admin1
Password: admin123*i


### 📊 Sample Score Visualization
After completing quizzes, users can view a summary of their highest scores across all quizzes in a bar chart, generated using Matplotlib and rendered directly in the browser.

### 🙋‍♀️ Author
Akshaya SK
B.Tech (IT) @ CEG | B.S. Data Science @ IITM
