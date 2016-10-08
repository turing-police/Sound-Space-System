#import random
import png
import struct
import socket
import array

class SoundProcessor:
    def __init__(self):
        self.fc = FreqConverter()


    # data_pairs should be 3 pairs in a list
    # each pair[0] is the client and each pair[1] is an int array containing sound intensities
    # returns a list of length 3.  list[0] is the x position of the sound, list[1] is the y position.  list[2] is the average intensity
    def process(self, data_pairs, sample_rate):
        pair0 = data_pairs[0]
        pair1 = data_pairs[1]
        pair2 = data_pairs[2]
        client0 = pair0[0]
        client1 = pair1[0]
        client2 = pair2[0]
        arr0 = pair0[1]
        arr1 = pair1[1]
        arr2 = pair2[1]
        locX = []
        locY = []
        intensitySum = 0
        #print(str(len(arr0)) + " " + str(len(arr1)) + " " + str(len(arr2)))
        for i in range(sample_rate):
            intensity0 = abs(arr0[i]) * client0.scale
            intensity1 = abs(arr1[i]) * client1.scale
            intensity2 = abs(arr2[i]) * client2.scale
            #intensity0 = abs(arr0[i])
            #intensity1 = abs(arr1[i])
            #intensity2 = abs(arr2[i])
            intensitySum = intensitySum + intensity0 + intensity1 + intensity2
            xytuple = self.processClients(client0, client1, client2, intensity0,
                                     intensity1, intensity2)
            locX.append(xytuple[0])
            locY.append(xytuple[1])
        sumx = 0
        sumy = 0
        for num in locX:
            sumx += num
        for num in locY:
            sumy += num

        averageIntensity = intensitySum/(sample_rate*3)
        so = SoundObject(sumx/(sample_rate*averageIntensity),
                         sumy/(sample_rate*averageIntensity), averageIntensity,
                         self.fc)
        return so

    def processClients(self, c0, c1, c2, i0, i1, i2):
        x = ((c0.x * i0)+(c1.x * i1)+(c2.x * i2))/ 3
        y = ((c0.y * i0)+(c1.y * i1)+(c2.y * i2))/ 3
        return (x, y)


class SoundObject:
    def __init__(self, x, y, intensity, fc):
        self.x = x
        self.y = y
        self.color = fc.freq_to_rgb(intensity)
        self.size = fc.freq_to_size(intensity)
        print(self.size)

    def __str__(self):
        return " ".join([str(self.x), str(self.y), self.color])


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
        idx = min(int(freq*4) * len(self.rgb_vals)//2147000000, len(self.rgb_vals) - 1)
        rgba = self.rgb_vals[idx][:3]
        rgba_strs = [str(hex(val))[2:] for val in rgba]
        rgba_strs = ["0" + val if len(val) < 2 else val for val in rgba_strs]
        return "#" + "".join(rgba_strs)

    def freq_to_size(self, freq):
        #lowerBound = 1e5
        #upperBound = 1e9
        #diff = upperBound - lowerBound
        #return 2 ** (((freq - diff)/diff)*6)
        #return 20 * ((freq/2147000000) ** 2)
        return 200 * freq /2147000000

#class Sampler:
    #def __init__(self):
        #self.fc = FreqConverter()

    #def get_sound_objs(self):
        #result = []
        #for i in range(3):
            #x = random.randint(0, 600)
            #y = random.randint(0, 600)
            #freq = random.randint(0, 20000)
            #color = self.fc.freq_to_rgb(freq)
            #result.append(SoundObject(x, y, color))
        #return result


class BufferClient:
    def __init__(self, client_sock, address):
        self.sock = client_sock
        self.x = -1
        self.y = -1
        self.scale = 1


class BufferServer:
    def __init__(self):
        self.host = ''
        self.serv_port = 8888
        self.backlog = 5
        self.size = 4096
        self.clients = []
        self.sound_objs = []
        self.sp = SoundProcessor()

    def update_sound_objs(self, data_pairs, min_len):
        self.sound_objs = [self.sp.process(data_pairs, min_len//4)]
        #print(self.sound_objs[0])

    def get_sound_objs(self):
        #result = []
        #for i in range(3):
            #x = random.randint(0, 600)
            #y = random.randint(0, 600)
            #freq = random.randint(0, 20000)
            #color = self.fc.freq_to_rgb(freq)
            #result.append(SoundObject(x, y, color))
        return self.sound_objs

    def wait(self, client):
        while True:
            data = client.sock.recv(self.size)

    def send_acks(self):
        for client in self.clients:
            client.sock.send(b'r')

    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serv_sock.bind((self.host, self.serv_port))
        self.serv_sock.listen(self.backlog)
        for i in range(3):
            client_sock, address = self.serv_sock.accept()
            bc = BufferClient(client_sock, address)
            data = bc.sock.recv(16)
            vals = struct.unpack('IId', data)
            bc.x, bc.y, bc.scale = vals
            print(bc.scale)
            self.clients.append(bc)
        self.send_acks()
        while True:
            data_pairs = []
            min_len = self.size
            for client in self.clients:
                data = client.sock.recv(self.size)
                data_array = array.array('i', data)
                if len(data) < min_len:
                    min_len = len(data)
                data_pairs.append((client, data_array))
            self.update_sound_objs(data_pairs, min_len)


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
