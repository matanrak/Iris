import socket
import threading

class Server(object):

    serverHost = 'localhost'
    serverPort = 8021

    def __init__(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind((self.serverHost, self.serverPort))
        #Builds the socket with the host / port I defined


    def listen(self):

        print ('running server...')
        self.sock.listen(5)
        #Sets the max number of connections in queue, I belive that 5 is the max I can set

        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.processRequest,args = (client,address)).start()



    def processRequest(self, client, address):

        while True:
            try:
                data = client.recv(1024)

                Iris.get_answer(data.decode())
                print data.decode()

                client.close()

            except:
                return False
