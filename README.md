# Backend

You need to have mongo installed (I use mongoDB Compass for the GUI)
Before running below, go to your terminal and start mongo (command below), then open compass and connect

## Setting Up

1. Clone the repo
   `git clone <repository_url>`
    `cd backend`

2. Set up Virtual Env
\
   `python3 -m venv venv` (linux/macOS)
   `source venv/bin/activate`
\
   `python -m venv venv` (windows)
   `venv\Scripts\activate` 
   
3. Install
   `pip install -r requirements.txt`

4. Create migrations
   `python manage.py makemigrations`

5. Apply migrations
   `python manage.py migrate`

6. Start
   `python manage.py runserver`



## Useful commands
`deactivate` to stop the virtual env
`mongod --dbpath /usr/local/var/mongodb` to start mongo terminal (depends on where you place)
I created a database with name "users" 