# Backend

You need to have mongo installed (I use mongoDB Compass for the GUI)
Before running below, go to your terminal and start mongo (command below), then open compass and connect

## Set Up Kafka
1. Install Zookeeper
`brew install zookeeper`

2. Install Kafka
`brew install kafka`

3. Start Zookeeper
`zkServer start`

4. Start Kafka Server (default port is localhost:9092)
`kafka-server-start /usr/local/etc/kafka/server.properties` (/opt/homebrew/etc/kafka/server.properties for macos)
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

### Instantiate/ Re-deploy Server
4. Create migrations
   `python manage.py makemigrations`

5. Create Superuser
   `python manage.py createsuperuser`
   uid just put admin, password just password
   admin page is at localhost:8000/admin

6. Apply migrations
   `python manage.py migrate`

7. Start
   `python manage.py runserver`

8. Daphne (Websocket server)
   `daphne -b 0.0.0.0 -p 8000 core.asgi:application`

## Useful commands
`deactivate` to stop the virtual env

`mongod --dbpath /usr/local/var/mongodb` to start mongo terminal (depends on where you place)
I created a database with name "users" 

## Common Errors Faced
`Error: That port is already in use.`

1. Check processes running on your port (Based on where the server is running). 
`bash lsof -i :<port>` 
2. Look for the PID that your server is running on and kill it.
`kill -9 <PID>`

1 Terminal for frontend
1 Terminal for Django backend
1 Terminal for Daphne backend (Websockets)
1 Terminal for zookeeper
1 Terminal for kafka
1 Terminal for analysis agent (python manage.py run_analysis_agent)
