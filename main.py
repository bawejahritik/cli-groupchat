import click
import sys
import redis
import time
import threading

def receive():
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        p = r.pubsub()
        p.subscribe('my-channel')

        while True:
            message = p.get_message()
            if message:
                message = message["data"]
                if type(message) == str:
                # do something with the message
                    i = 0
                    curr = message[i]
                    lengthOfUserName = 0
                    while curr.isnumeric():
                        lengthOfUserName = lengthOfUserName*10 + int(curr)
                        i += 1
                        curr=message[i]
                    print(f'{message[i:i+lengthOfUserName]} -> {message[lengthOfUserName + i : ]}')
            time.sleep(0.001)

def write(username):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    try:
        while True:                                                 #message layout
            message = input('')
            r.publish('my-channel',str(len(username)) + username + message)
            # r.publish('my-channel',{username: username, message: message})
    except:
        pass

@click.command()
@click.option('-s', '--server', 'server', is_flag=True, help="To start the server")
@click.option('-c', '--client', 'client', is_flag=True, help="To start the client")
def main(server, client):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    username = input("Enter your username: ")
    receive_thread = threading.Thread(target=receive)               #receiving multiple messages
    receive_thread.start()
    write_thread = threading.Thread(target=write, args=(username, ))                   #sending messages 
    write_thread.start()
    # if server:
    #     username = input("Enter your username: ")
    #     receive_thread = threading.Thread(target=receive)               #receiving multiple messages
    #     receive_thread.start()
    #     write_thread = threading.Thread(target=write, args=(username, ))                   #sending messages 
    #     write_thread.start()
    #     # while True:
    #     #     msg = input()
    #     #     r.publish("my-channel", str(len(username)) + username + msg)

    
    # if client:
    #       # be nice to the system :)
    #     username = input("Enter your username: ")
    #     receive_thread = threading.Thread(target=receive)               #receiving multiple messages
    #     receive_thread.start()
    #     write_thread = threading.Thread(target=write, args=(username, ))                   #sending messages 
x

if __name__ == '__main__':
    main()