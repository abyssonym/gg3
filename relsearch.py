from sys import argv
from string import ascii_lowercase
from shutil import copyfile

filename = argv[1]
outfile = "test.smc"
searchstr = argv[2].lower()

if '.' in searchstr:
    searchstr = map(int, searchstr.split('.'))
else:
    numdict = dict([(b, a) for (a, b) in enumerate(ascii_lowercase)])
    searchstr = [numdict[c] if c in numdict else c for c in searchstr]

print searchstr

f = open(filename, 'r+b')
addr = 0
checkstr = None
while True:
    f.seek(addr)
    bytestr = f.read(len(searchstr))
    if len(bytestr) != len(searchstr):
        break
    bytestr = map(ord, bytestr)
    offset = bytestr[0] - searchstr[0]
    newbytestr = [i - offset for i in bytestr]
    if all([a == b for (a, b) in zip(newbytestr, searchstr)]):
        print "%x" % addr
        print bytestr
        check = None
        if not checkstr:
            check = raw_input("> ")
        if check and check.lower()[0] == 'y':
            checkstr = bytestr
        if checkstr and all([a == b for (a, b) in zip(checkstr, bytestr)]):
            copyfile(filename, outfile)
            f2 = open(outfile, 'r+b')
            f2.seek(addr)
            f2.write("".join([chr(bytestr[0]) for _ in bytestr]))
            f2.close()
            check = raw_input("> ")
    addr += 1
