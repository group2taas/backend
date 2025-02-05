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
`kafka-server-start /usr/local/etc/kafka/server.properties`

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

5. Apply migrations
   `python manage.py migrate`

6. Start
   `python manage.py runserver`

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

