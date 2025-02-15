# Backend

Create a parent folder and put both your frontend and backend folder inside. 

Move the docker-compose.yml out to the same layer as frontend and backend folder.

Your parent folder should have the following structure:
```bash
parent_folder
├── frontend
│      ├── folder1
│      ├── folder2
│      ...
│ 
├── backend
│      ├── folder1
│      ├── folder2
│      ...
│      
└── docker-compose.yml
```

Open docker desktop 
in backend/.env, modify the bootstrap servers (changed in liveupdates document)
```
KAFKA_BOOTSTRAP_SERVERS="kafka:9092" 
```

## Docker commands
Ensure that you have both backend and frontend folders with the latest docker image.
Ensure that your terminal is at the parent folder.

To build the containers
```bash
docker-compose up --build
```

To stop running the container, run
```
docker-compose down
```

In order for the application to reflect new changes, you need to restart the docker
container and rebuild the image.

# ARCHIVES 
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
1 Terminal for testing agent (python manage.py run_testing_agent)