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

![Valid command with valid result](/images/valid_stock.png)

**Invalid Command**

When the user enters `/{anything but the right command}`
![Valid command with valid result](/images/invalid_command.png)

**Bad Stock symbol Command**

When the user enters `/stock={anything but a stock symbol}`
When you pass stock symbol that doesn't exists the Bot does not find any data on Stooq thus it understand that the data is missing or incomplete and prompts message according to that situation
![Valid command with valid result](/images/invalid_stock_symbol.png)

**Forgot to add a symbol**

When the user enters `/stock=`
The command is a valid one but it has no data thus the Bot notice that mishap 
![Valid command with valid result](/images/missing_stock_symbol.png)

## Tutorial

### Account and room setting

**Home**
From the home page click on `Signup`
![Valid command with valid result](/images/home.png)

**Signup**
To signup enter your information. The chat app Does not accept duplicated usernames, your username shall become your id for all chat purposes
![Valid command with valid result](/images/signup1.png)

**Login**
Now that you have signup enter your new username and password
![Valid command with valid result](/images/login.png)

**Welcome**
Your home page looks different when you are logged in. Since you are new here you are not a member of any chat room so might as well create a new chatroom, 
![Valid command with valid result](/images/home_logged.png)

**Create a Room**
Time to create your first chat room and decides who is able to join you
don't forget to enter the username of a friend of yours to the chatroom so that you speak with a friend. Your friend will need to signup too
![Valid command with valid result](/images/create_room.png)


**Join your Room**
All your rooms appear at your home page, so now that you have room you just need to click on it to join
![Valid command with valid result](/images/home_with_room.png)

**That's it now you are chatting**
You can chat now when everyone on the room including the our Bot
![Valid command with valid result](/images/a_room.png)

**Talk to your friends right next to you**
Open a side-by-side window to chat with your friends on the same laptop at the same time.. Technolgy really can bring us together!
![Valid command with valid result](/images/side_by_side.png)

