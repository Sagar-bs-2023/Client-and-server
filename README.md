# Client-and-server
A simulation of communication between client and server.
This code is an attempt to simulate and understand the working of the client and server. The code uses python sockets module for connecting the server and client. The server and client in this case can be any two systems connected over a network and there is no requirements for the system running the server side python code to have higher specs or something like that.

How to use?
Step 1 : Run the server.py on a system which should receive files or is the command centre for simplicity.
Step 2 : On running the server.py on the system you get the below message from which you have to use the "<ip-address>:<port-number>" and replace the PORT and SERVER with the <port-number> and <ip-address> respectively in the client.py file.

[STARTING] Server is starting...
[LISTENING] Server is listening on <ip-address>:<port-number>
Enter !CMD: for running commands on the client's command prompt
Enter !GET: for downloading files from the client
Enter !DISCONNECT: for disconnecting from the client
#################################################################

Step 3 : On modifying the client.py with the port number and ip of server just run the client.py on the sender system.
Step 4 : Now u have access to the sender's folder where the client.py is saved. You can perform any actions like getting network information of client by using the "!CMD:ipconfig" etc.
TO download files from client.py first do "!CMD:dir" on doing this you get a list of files. Then just do "!GET:<filename>" just replace <filename> with the filename that you want to download and is prestnt in the list of files you get after doing "!CMD:dir".

Capabilities :
The client.py and server.py combined provides 3 functionalities -- 
1. !CMD : For running the commands on the clients command prompt.
2. !GET : For downloading the files from the folder in which the client.py is stored.
3. !DISCONNECT : To disconnect the from the client.
It should be noted that these command can only be run on the server.py terminal.

Use case :
As of now the only use case I can think of is that using this code for transferring files between systems. This can be achieved by using the !GET command and basic cmd commands. The server.py code should be run on the receiving system and the sender must be running the client.py in the sender system. This code can also be used as a Command and control server but this cab work only for the client.py which is there and you can't send any payloads.
