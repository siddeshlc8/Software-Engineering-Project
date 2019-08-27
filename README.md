# Online Cricket Tournaments Management System



Managing score-card of whole tournament with each player's performance is very difficult task to do manually. So we are digitalizing the whole process though our software.

We have created a web application using Django framework (which is high level python framework ) . we have used html, css, javascript for front end design. Pycharm Ide is used for the developing purpose.

The demo can be viewed with this link - [Demo](http://siddeshlc8.pythonanywhere.com/)


Running on Local machine

1. Make sure python 3.XX is used

2. create virtual environment

        python -m venv cricky

3. Activate virtual environment

        windows ->  ./cricky/Scripts/activate
        ubuntu ->   source  cricky/Scripts/activate

4. clone the repo

        git clone https://github.com/siddeshlc8/Software-Engineering-Project.git

5. Go to git directory

        cd Software-Engineering-Project

6. Run pip install

        pip install -r requirements.txt

7. Delete database sqilte3

        delete db.sqlite3 file

8. Run migrate

        python manage.py migrate

9. Run server

        python manage.py runserver

10. Open Browser

        http://127.0.0.1:8000/