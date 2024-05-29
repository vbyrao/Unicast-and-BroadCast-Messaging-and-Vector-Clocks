import socket
import threading

HOST = 'localhost'

class Process:
    def __init__(self):
        self.id = 0
        self.clock = [0] * 3

    def broadcast(self):
        while True:
            p = int(input("Enter which process to send 1 or 2\n"))
            broad_msg = input('Enter a message to broadcast: \n')
            print(f'Before sending the message clock - {self.clock}\n')
            self.clock[self.id] += 1
            clk_at_msg = f'{broad_msg}:{self.clock}'.encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, 1234+p))
            s.send(clk_at_msg)
            s.close()

    def receive(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, 1234))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                broad_msg = data.decode('utf-8')
                clk_rcvd = [int(x) for x in broad_msg.split(':')[1][1:-1].split(',')]
                for i in range(3):
                    self.clock[i] = max(self.clock[i], clk_rcvd[i])
                self.clock[self.id] = self.clock[self.id]+1
                print(f'Received message "{broad_msg}" with clock {clk_rcvd} and updated own clock to {self.clock}\n')

process = Process()
threading.Thread(target=process.broadcast).start()
threading.Thread(target=process.receive).start()
