# Backend

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

4. Apply migrations
   `python manage.py migrate`

5. Start
   `python manage.py runserver`
