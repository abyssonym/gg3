# -*- coding: utf-8 -*-
from utils import read_multi, write_multi


table = ("****\n***********"
         "******ＢＲ　*あいうえおか"
         "きくけこさしすせそたちつてとなに"
         "ぬねのはひふへほまみむめもやゆよ"
         "らりるれろわをんっゃゅょ****"
         "****************"
         "*********エモン*ス**"
         "******ー*・？！「」***"
         "********がぎぐげござじず"
         "ぜぞだぢづでどばびぶべぼゴビ**"
         "********ぱぴぷぺぽ***"
         )
table = table.decode('utf-8')

constants = {0xD1: u"！」\n",
             0xD3: u"」\n",
             0xD4: u"ゴエモン　「",
             0xD5: u"エビス丸　「",
             0xD8: u"・・・・",
             0xD9: u"　　　　",
             }

assert len(table) == 0xb0


class Dialogue:
    def __init__(self, pointer):
        self.pointer = pointer

    def __repr__(self):
        s = ""
        for i in self.message:
            if i < len(table) and table[i] != "*":
                s += table[i]
            elif i in constants:
                s += constants[i]
            else:
                s += " %x " % i
        s = "%x %s" % (self.pointer, s)
        return s

    def read_data(self, filename, header=False):
        f = open(filename, 'r+b')
        f.seek(self.pointer)
        if header:
            unknown = f.read(4)
            self.y = f.read(2)
            self.x = f.read(2)
            self.ff = f.read(1)
        nowpointer = f.tell()
        message = []
        while True:
            f.seek(nowpointer)
            byte = ord(f.read(1))
            if byte & 0xF0 == 0xF0:
                # stored word
                wordlength = (byte & 0x0F) + 4
                ctrlptr = read_multi(f, length=2)
                #if ctrlptr >= 0x8000:
                #    print "WARNING1 %x" % ctrlptr
                f.seek((nowpointer & 0xff0000) | ctrlptr)
                word = map(ord, f.read(wordlength))
                message.extend(word)
                nowpointer += 3
            elif byte & 0xF0 == 0xE0:
                # repeated character
                wordlength = (byte & 0x0F) + 3
                char = ord(f.read(1))
                message.extend([char]*wordlength)
                nowpointer += 2
            elif byte & 0xF0 == 0xB0:
                # control command
                nowpointer += 3
            elif byte & 0xF0 == 0xC0:
                message.append(0x18)
                nowpointer += 1
            elif byte & 0xF0 == 0xD0:
                message.append(byte)
                nowpointer += 1
            elif byte == 0x00:
                # termination
                nowpointer += 1
                break
            elif byte < 0xb0:
                # ordinary character
                message.append(byte)
                nowpointer += 1
            else:
                print "WARNING2 %x" % byte
                nowpointer += 1
        f.close()
        self.message = message
        return nowpointer


if __name__ == "__main__":
    from sys import argv
    try:
        #pointer = 0x1ee132
        pointer = int(argv[1], 0x10)
        #d = Dialogue(pointer=0x1b5337)
        #for i in range(547):
        #for i in range(547)[:450]:
        for i in range(3):
            d = Dialogue(pointer=pointer)
            pointer = d.read_data("test.smc")
            print unicode(d)
    except ValueError:
        searchfor = argv[1].decode('utf-8')
        for c in searchfor:
            print c,
            i = table.index(c)
            print "%x" % i
