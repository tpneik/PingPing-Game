#!/usr/bin/env python
import socket, select, sys, time, simplejson
sys.dont_write_bytecode = True
from lib import settings
import types
import selectors

buffer_size = 2000
delay = 0.01
rackets = {}


# class GameServer:
#
#     def __init__(self, host, port):
#         self.input_list = []
#         self.channel = {}
#
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.server.bind((host, port))
#         self.server.listen(0)
#
#     def main_loop(self):
#         self.input_list.append(self.server)
#         while 1:
#             time.sleep(delay)
#             inputr, outputr, exceptr = select.select(self.input_list, [], [])
#             for self.s in inputr:
#                 if self.s == self.server:
#                     self.on_accept()
#                     break
#                 else:
#                     self.data = self.s.recv(buffer_size)
#                 if len(self.data) == 0:
#                     self.on_close()
#                 else:
#                     self.on_recv()
#
#     def on_accept(self):
#         clientsock, clientaddr = self.server.accept()
#         print(f"{clientaddr} has connected")
#         rackets[clientaddr[1]] = {}
#         self.input_list.append(clientsock)
#
#     def on_close(self):
#         clientaddr = self.s.getpeername()
#         print(f"{clientaddr} has disconnected")
#         del(rackets[clientaddr[1]])
#         self.input_list.remove(self.s)
#
#     def on_recv(self):
#         player_id = self.s.getpeername()[1]
#         rackets[player_id] = simplejson.loads(self.data.decode('utf-8'))
#         self.s.send(simplejson.dumps(rackets).encode('utf-8'))


class Server:

    def __init__(self, host, port):
        self.max_cap = 2
        self.sel = selectors.DefaultSelector()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        print(f"Listening on {(host, port)}")
        self.server.setblocking(False)
        self.sel.register(self.server, selectors.EVENT_READ, self.accept)

    def main_loop(self):
        try:
            while True:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self.sel.close()





    def accept(self,sock,mask):
        if self.max_cap > 0:
            conn, addr = sock.accept()
            print(f"Accepted connection from {addr}")
            conn.setblocking(False)
            rackets[addr[1]] = {}
            self.sel.register(conn, selectors.EVENT_READ, self.receive)
            self.max_cap -= 1




    def receive(self, conn, mask):
        data = conn.recv(buffer_size)
        if data:
            player_id = conn.getpeername()[1]
            rackets[player_id] = simplejson.loads(data.decode('utf-8'))
            conn.send(simplejson.dumps(rackets).encode('utf-8'))
        else:
            print('closing', conn)
            player_id = conn.getpeername()[1]
            del rackets[player_id]
            self.sel.unregister(conn)
            conn.close()
            self.max_cap += 1





if __name__ == '__main__':
        server = Server(settings.SERVER_IP, settings.SERVER_PORT)
        print("Server listening...")
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)


