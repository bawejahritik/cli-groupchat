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
                # do something with the message
                message = message["data"]
                print(message)
            time.sleep(0.001)

def write(username):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    while True:                                                 #message layout
        message = input('')
        # r.publish('my-channel',str(len(username)) + username + message)
        r.publish('my-channel',{username: username, message: message})

@click.command()
@click.option('-s', '--server', 'server', is_flag=True, help="To start the server")
@click.option('-c', '--client', 'client', is_flag=True, help="To start the client")
def main(server, client):
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    if server:
        username = input("Enter your username: ")
        while True:
            msg = input()
            r.publish("my-channel", str(len(username)) + username + msg)

    
    if client:
          # be nice to the system :)
        username = input("Enter your username: ")
        receive_thread = threading.Thread(target=receive)               #receiving multiple messages
        receive_thread.start()
        write_thread = threading.Thread(target=write, args=(username, ))                   #sending messages 
        write_thread.start()

if __name__ == '__main__':
    main()