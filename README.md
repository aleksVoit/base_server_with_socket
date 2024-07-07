# Homework #4 - base_server_with_socket 


Your goal is to implement the simplest web application. 
Take the following files as a basis.

By analogy with the example considered in the synopsis, 
create a web application with routing for two HTML pages: 
index.html and message.html.

Also:

Treat static resources during the program: Style.css, logo.png;

Organize work with the form on Message.html;
In case of error 404 Not Found Return Error.html Page
Your app works on port 3000

To work with the form, create a Socket server on the port 5000. 
The algorithm of work is as follows. You enter the data into the form, 
they get into your web application, which forwards it further to processing 
using Socket (UDP), server Socket. Socket server translates the receipt 
byte to the dictionary and stores it in JSON file data.json into the Storage folder.

Data.json file recording format as follows:

{
 "2022-10-29 20: 20: 58.020261": {
 "USERNAME": "KRABATON",
 "MESSAGE": "FIRST MESSAGE"
 },
 "2022-10-29 20: 21: 11.812177": {
 "Username": "Krabat",
 “Message”: “Second Message”
 }
}

Where the key of each message is the time of receiving the message: dateTime.now (). 
That is, each new message from the web program is added to the Storage/Data.json file 
with the time of receipt.

Use one Main.py file to create your web program.

Run http server and Socket server in different streams.

Additional task

​

This is an additional task and can not be done to hand over this homework.

Create Dockerfile and run your app as a docker container
Using the Voluemes mechanism, save data from Storage/Data.json not inside the container

Hint
To implement the Voluemes mechanism, you need to check the existence of the Storage 
Catalog and the Data.json file at the start of the program. And if they are absent, 
then create them.