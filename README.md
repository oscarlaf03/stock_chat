# Simple stock bot

This is a thought exercise regarding real time web_socket apps, message broker queues and bot assistants.

When using a chatoorm a user can type a command to the bot by inputing a message that starts with the character: "/".
For now the only valid command  serves to retreive stock market information for a listed share in the Exchange Market, such command is: `"/stock={a stock symbol}"` for example: `/stock=tsla.us`.

Any user message that sends a message starting with "/" will receive a personalized (the bot is addressing the user by their username) and categoric (There is finite number of possible answers that the Bot can articulate) response from the Bot. Including have an update on the price of a given share when the command is followes properly.

**TLDR: You can pass any value as stock symbol to the bot and if it finds any data it will let you know**

### Structure
The root saves two main thins: 1) A Flask chat capp that includes a message broker and 2) a Bot that can receives a text message, compaire it agains it's rules and provide an answer 

#### Chat
The Flask chat app enables chat messaging in the browser via `socket.io`. The app supports user authentication and preserves messages directly on the cloud with atlas `pymongo` so no local data base is to run the app locally. Messages that are flagged as bot commands and Bot repplies are not stored on the Database and are lost at the end of session.

The broker module initiates a`Producer` named "Publiher" using `pika` and `RabbitMQ`. All user's messages are pushed by the `Publisher` class object into the Exchange and queue to be picked up by a `Consumer`. The consumer acts as a worker, it is in charge of deciding whether or not each message is in fact a Bot command and when it is the Consumer propmts the Bot for a reponse and send back that response to chat browser using a connection to the same socket using `socketio` once more but this time also including `redis` for socket queues.

**TLDR: Whenever a message starts with "/" the consumer asks the Bot for an answer and emits the answer back to the chat room using `redis` and `socketio`** 

#### Bot
Bot is a very slim class, in about 65 lines of code the bot initiates by receiving `message` and the `username` of the message's author. The bot can interpret whether or not the command is valid, wheter or not an stock symbo was provided and whether or not there is complee financial information for such stock symbol.

### Requirements:
* RabbitMQ must be installed
* redis-server must be installed
* libraries on: **/requirements.txt**
  * flask
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
1. Install requirements from the root folder using **pipenv** so you can take advantage of the tested Pipfile.lock file. In order to install directly from the Pipfile.lock file and ignore the regular "Pipfile" you must use this command:
  - `pipenv install --ignore-pipfile`
2. Start the server using the make command from the root folder:
  - `make runserver`
3. On another terminal start the worker with make command folder. In order for the Bot to work this worker must be running:
  - `make runwoker`

### Running Tests:
* From the root folder run: `pytest`

## How smart is the bot?

##### Right answer

When the stock command is properly used everything is sweet `/stock=aapl.us`

![Valid command with valid result](/images/valid_stock.png)

##### Invalid Command

When the user enters `/{anything but the right command}` the bots realizes it was not asked for some stock data.
![Invalid Command](/images/invalid_command.png)

##### Bad Stock symbol Command

When the user enters `/stock={an incorrect stock symbol}`. The user might just made a small typo or maybe the user typed the most unusual thing, either way there is not stock data for that stock symbol attempt.

![Invalid stock symbol](/images/invalid_stock_symbol.png)

##### Forgot to add a symbol

When the user enters `/stock=` The command is a valid one but it has no data thus the Bot notice that mishap and reminds the user to provide a stock symbol

![Forgot stock symbol](/images/missing_stock_symbol.png)

## Tutorial

### Account and room setting

##### Home
From the home page click on `Signup`

![Home](/images/home.png)

 ##### Signup
To signup enter your information. The chat app Does not accept duplicated usernames, your username will become your id for all chat purposes

![Singup](/images/signup1.png)

##### Login
Now that you have signup enter your new username and password

![Login](/images/login.png)

##### Welcome
Your home page looks different when you are logged in. Since you are new here you are not a member of any chat room so might as well create a new chatroom, 
![Logged](/images/home_logged.png)

##### Create a Room
When you create your first chat room you will also decides who is able to join you (don't worry you can make changes later). So don't forget to enter the username of a friend of yours to the chatroom so that you can speak with your friends. (enter multiple usernames separated by ",")  Your friend will need to signup too.

![Create Room](/images/create_room.png)

##### Join your Room
All your rooms appear at your home page. So now that you have room you just need to click on it to join the room.

![Join Room](/images/home_with_room.png)

##### That's it now you are chatting
You can chat now when everyone on the room including our Bot

![Chatting](/images/a_room.png)

##### Talk to your friends right next to you
Open a side-by-side window to chat with your friends on the same laptop at the same time! Isn't it wonder how technolgy can truly bring us together?

![Side by side](/images/side_by_side.png)


### Link Structure:

|                   URL                   |       Site     |
|:---------------------------------------:| :--------------: |
| `http://127.0.0.1:5000` | home |
| `http://127.0.0.1:5000/login/` | Login |
| `http://127.0.0.1:5000/signup/` | Signup |
| `http://127.0.0.1:5000/create-room` | Creates a new room  |
| `http://127.0.0.1:5000/rooms/<room_id>` | The interactive chat room  |
| `http://127.0.0.1:5000/rooms/<room_id>/edit` | Edit your chat room |
| `http://127.0.0.1:5000/logout/` | Logout |
