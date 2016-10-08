import random
import png
import struct
import socket
import array
import spectrum


class SoundObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


class FreqConverter:
    def __init__(self):
        r = png.Reader(filename='colorbar.png')
        img = r.asDirect()
        row = list(img[2])[0]
        self.rgb_vals = []
        for i in range(len(row)//4):
            self.rgb_vals.append(row[4*i:4*i + 4])
        self.rgb_vals = self.rgb_vals[::-1]

    def freq_to_rgb(self, freq):
        idx = min(freq * len(self.rgb_vals)//20000, len(self.rgb_vals) - 1)
        rgba = self.rgb_vals[idx][:3]
        rgba_strs = [str(hex(val))[2:] for val in rgba]
        rgba_strs = ["0" + val if len(val) < 2 else val for val in rgba_strs]
        return "#" + "".join(rgba_strs)


class Sampler:
    def __init__(self):
        self.fc = FreqConverter()

    def get_sound_objs(self):
        result = []
        for i in range(3):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            freq = random.randint(0, 20000)
            color = self.fc.freq_to_rgb(freq)
            result.append(SoundObject(x, y, color))
        return result


class BufferClient:
    def __init__(self, client_sock, address):
        self.sock = client_sock
        self.x = -1
        self.y = -1


class BufferServer:
    def __init__(self):
        self.host = ''
        self.serv_port = 8888
        self.backlog = 5
        self.size = 2048
        self.clients = []

    def wait(self, client):
        while True:
            data = client.sock.recv(self.size)
            print(data)

    def send_acks(self):
        for client in self.clients:
            client.sock.send(b'r')

    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.bind((self.host, self.serv_port))
        self.serv_sock.listen(self.backlog)
        for i in range(3):
            client_sock, address = self.serv_sock.accept()
            bc = BufferClient(client_sock, address)
            data = bc.sock.recv(self.size)
            vals = struct.unpack('II', data)
            bc.x, bc.y = vals
            self.clients.append(bc)
            break
        self.send_acks()
        while True:
            aggregated_values = []
            for client in self.clients:
                data = client.sock.recv(self.size)
                data_array = array.array('I', data)
                aggregated_values.append(client, data_array)


    def get_sound_objs(self):
        result = []
        for i in range(3):
            x = random.randint(0, 600)
            y = random.randint(0, 600)
            freq = random.randint(0, 20000)
            color = self.fc.freq_to_rgb(freq)
            result.append(SoundObject(x, y, color))
        return result


def main():
    b_server = BufferServer()
    b_server.start()

    #with open('sampleData', 'rb') as f1:
        #byte = "a"
        #while byte:
            #byte = f1.read(1)
            #if byte:
                #val = struct.unpack('B', byte)[0]
                #print(val)

if __name__ == "__main__":
    main()
