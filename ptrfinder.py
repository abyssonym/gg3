from utils import read_multi, write_multi
from shutil import copyfile


def ptrfind(filename, ptrsize, minimum, reverse=True):
    ptrsize, minimum = int(ptrsize), int(minimum)
    reverse = False if reverse == "False" else bool(reverse)
    f = open(filename, 'r+b')
    f.seek(0, 2)
    filesize = f.tell()
    location = 0
    discoveries = []
    while True:
        f.seek(location)
        prev = -1
        values = []
        while True:
            if f.tell() + ptrsize >= filesize:
                break
            value = read_multi(f, ptrsize, reverse=reverse)
            if value < prev:
                break
            if value == prev and value == 0 and len(values) == 1:
                break
            values.append(value)
            prev = value
        if len(values) >= minimum and len(set(values)) >= minimum/8:
            discoveries.append((location, values))
            location += len(values) * ptrsize
        else:
            location += 1
        if location + ptrsize >= filesize:
            break
    f.close()
    return discoveries


def tabletest(filename, ptrsize, discoveries, reverse=True):
    testfile = "test.smc"
    print "%s tables to test." % len(discoveries)
    for location, values in discoveries:
        copyfile(filename, testfile)
        f = open(testfile, 'r+b')
        print "%x (%s)" % (location, len(values))
        f.seek(location)
        newvalues = values[:1] + ([values[1]] * len(values[1:]))
        for value in newvalues:
            write_multi(f, value, ptrsize, reverse=reverse)
        f.close()
        raw_input("> ")


if __name__ == "__main__":
    from sys import argv
    discoveries = ptrfind(*argv[1:])
    tabletest(argv[1], int(argv[2]), discoveries)
