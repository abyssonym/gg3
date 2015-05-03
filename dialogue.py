# -*- coding: utf-8 -*-
from utils import read_multi, write_multi


table = ("****************"
         "********　*あいうえおか"
         "きくけこさしすせそたちつてとなに"
         "ぬねのはひふへほまみむめもやゆよ"
         "らりるれろわをんっゃゅょ****"
         "****************"
         "****************"
         "******ー**？！「」***"
         "********がぎぐげござじず"
         "ぜぞだぢづでどばびぶべぼ****"
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

    def read_data(self, filename):
        f = open(filename, 'r+b')
        f.seek(self.pointer)
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
                if ctrlptr >= 0x8000:
                    print "WARNING %x" % ctrlptr
                f.seek(0x1b0000 | ctrlptr)
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
            elif byte & 0xF0 == 0xD0:
                message.append(byte)
                nowpointer += 1
            elif byte == 0x00:
                # termination
                break
            elif byte < 0xb0:
                # ordinary character
                message.append(byte)
                nowpointer += 1
            else:
                print "WARNING %x" % byte
                nowpointer += 1
        f.close()
        self.message = message


if __name__ == "__main__":
    d = Dialogue(pointer=0x1b570f)
    d.read_data("test.smc")
    print unicode(d)
