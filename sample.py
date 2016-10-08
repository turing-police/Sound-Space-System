import random
import png
import struct
import socket

class SoundProcessor:
    def __init__(self):
        pass

    # data_pairs should be 3 pairs in a list
    # each pair[0] is the client and each pair[1] is an int array containing sound intensities
    # returns a list of length 3.  list[0] is the x position of the sound, list[1] is the y position.  list[2] is the average intensity
    def process(data_pairs):
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
        for i in range(512):
            #intensity0 = struct.unpack("I", stream0.readline(4))[0]
            #intensity1 = struct.unpack("I", stream1.readline(4))[0]
            #intensity2 = struct.unpack("I", stream2.readline(4))[0]
            intensity0 = arr[i]
            intensity1 = arr[i]
            intensity2 = arr[i]
            intensitySum = intensitySum + intensity0 + intensity1 + intensity2
            xytuple = processClients(client0, client1, client2, intensity0, intensity1, intensity2)
            locX.append(xytuple[0])
            locY.append(xytuple[1])
        sumx = 0
        sumy = 0
        for num in intensitiesx:
            sumx += num
        for num in intensitiesy:
            sumy += num

        averageIntensity = intensitySum/(512*3)
        return (sumx/(512*averageIntensity), sumy/(512*averageIntensity), averageIntensity)

    def processClients(c0, c1, c2, i0, i1, i2):
        x = ((c0.x * i0)+(c1.x * i1)+(c2.x * i2))/3
        y = ((c0.y * i0)+(c1.y * i1)+(c2.y * i2))/3
        return (x, y)

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
    def __init__(self, client_num, address):
        self.client_num = client_num
        self.x = -1
        self.y = -1


class BufferServer:
    def __init__(self):
        self.host = ''
        self.serv_port = 8888
        self.backlog = 5
        self.size = 1024
        self.clients = []

    def start(self):
        self.serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv_sock.bind((self.host, self.serv_port))
        self.serv_sock.bind.listen(self.backlog)
        for i in range(3):
            client, address = self.serv_sock.accept()
            self.clients.append(BufferClient(client, address))
            data = client.recv(self.size)
            if data:
                client.send(data)
            client.close()

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
    with open('sampleData', 'rb') as f1:
        byte = "a"
        while byte:
            byte = f1.read(1)
            if byte:
                val = struct.unpack('B', byte)[0]
                print(val)

if __name__ == "__main__":
    main()
