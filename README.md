# Simple stock bot

This is an thought exercise regarding real time web_socket apps, message broker queues and simple bot assistants

Throughout a command starting with "/" the user can input the one and only valid commando of "/stock={a stock symbol}" for example: `/stock=tsla.us`  and the bot will reply with the stock information obtained in csv format the www.stoq.com api and parsed to articulate the open price summary. The Bot can handle several wrong commands and fall backs

**You can pass any value as stock symbol to the bot and if it finds any data it will let you know**

### Structure
From the root folder you a flask chat app with a message broker module included and a separate folder with a Bot class

#### Chat
Flask app that enables chat messaging via `socket.io`  it supports user authentication, preserves messages directly on the cloud with atlas `pymongo` (no local data base needed).

The broker module initiates a queue via `pika` and `RabbitMQ`, user's messages are pushed  via a `Publisher` class into the queue to be picked up by a `Consumer`, the consumer acts as a middle-ware and knows when and when no to ask for a reply from the `Bot`

Whenever a message starts with "/" the consumer asks the Bot for an answer emits the answer back to the chat room using `redis` and `socketio` 

#### Bot
Bot is a very slim class, in about 65 lines of code the bot initiates with a  `message` and a `username` of who send that message and can interpret whether or not the command is valid and if there is data for the given stock symbol

### Requirements:
* RabbitMQ must be installed
* redis-server must be installed
* libraries on: **/requirements.txt**
  * flask-socketio
  * eventlet
  * pymongo
  * dnspython
  * werkzeug
  * flask-login  
  * bson
  * pika
  * redis
  * gunicorn
  * pytest

### How to run:
1. install requirements from the root folder **pipenv** strongly advised
  - `pipenv install -r requirements.txt`
2. Start the server using the make command from the root folder:
  - `make runserver`
3. On another terminal start the worker with make command folder:
  - `make runwoker`

### Running Tests:
* From the root folder run: `pytest`

## How smart is the bot?

**Right answer**
When the stock command is properly used everything is sweet `/stock=aapl.us`

![Valid command with valid result](/images/valid_stock.png | height=)


