import sys, argparse, getpass, binascii, os
from operator import mul

def binnifyString (string):
    binString = bin(int(binascii.hexlify(string), 16))[2:]
    if   len(binString) % 4 == 3: binString = '0'   + binString
    elif len(binString) % 4 == 2: binString = '00'  + binString
    elif len(binString) % 4 == 1: binString = '000' + binString
    return binString

def rotatePassword (password):
    binPass = binnifyString (password)
    rotatedBinPass = int(binPass[1:] + binPass[:1], 2)
    rotatedHexPass = '%x' % rotatedBinPass
    if len(rotatedHexPass) % 2 != 0:
        rotatedHexPass = '0' + rotatedHexPass
    return binascii.unhexlify(rotatedHexPass)

def findStartingPoint (password):
    passArray = [ ord(char) for char in password ]
    return reduce (mul, passArray, 1) % sum(passArray)

def readByteAt (position, keyfile):
    keyfile.seek(position, 0)
    return keyfile.read(1)

def msgBlkEncr (encrKey, msgBlock, outfile):
    for i in range(len(msgBlock)):
        outfile.write(chr(encrKey[i] ^ ord(msgBlock[i])))

def streamEncrypt (password, keyfile, infile, outfile):
    passNumber = 0
    keyFileSize = os.fstat(keyfile.fileno()).st_size
    inFileSize = os.fstat(infile.fileno()).st_size
    keyLengthArray = [24,16,24,16,32,32,32,32,24,16,32,16,32,24,32,32,32,32,32,16,32,24,32,24,24,32,24,32,32,16,32,16,32,24,24,16,24]

    x1_pos = len(password)
    x1_val = ord(readByteAt (x1_pos, keyfile))

    while inFileSize > 0:
        startPoint = findStartingPoint (password) % keyFileSize
        keyLen = keyLengthArray[startPoint % len(keyLengthArray)]
        # print >> sys.stderr, "# %d  Key Length : %s Starting Point : %s" % (passNumber, keyLen, startPoint)

        encrKey = list()

        x2_pos = startPoint + x1_pos
        x2_val = ord(readByteAt(x2_pos, keyfile))
        encrKey.append(x2_val)
        # sys.stderr.write(chr(x2_val))

        for i in range (1, keyLen):
            x3_pos = int (0.64372 * x2_pos + 71) % keyFileSize
            x3_val = ord(readByteAt(x3_pos, keyfile))
            x1_pos = x2_pos
            x1_val = x2_val
            x2_pos = x3_pos
            x2_val = x3_val

            encrKey.append(x3_val)
            # sys.stderr.write(chr(x3_val))

        msgBlock = infile.read(keyLen)
        msgBlkEncr (encrKey, msgBlock, outfile)

        inFileSize = inFileSize - keyLen
        password = rotatePassword (password)
        passNumber = passNumber + 1

def main ():
    argParser = argparse.ArgumentParser (description = 'Parse arguments for One Time Pad Generator')
    argParser.add_argument ('-p', '--passfile', help="File to read password from")
    argParser.add_argument ('-k', '--keyfile', help="File to generate keys", required=True)
    argParser.add_argument ('-i', '--infile', help="File to be encrypted", required=True)
    argParser.add_argument ('-o', '--outfile', help="File to write encrypted content")
    args = vars(argParser.parse_args())

    keyfile = open(args['keyfile'], mode='rb')
    infile = open(args['infile'], mode='rb')

    if args['passfile'] == None:
        password = getpass.getpass('Encryption Password: ')
    else:
        password = open(args['passfile']).read().strip()

    if args['outfile'] == None:
        outfile = sys.stdout
    else:
        outfile = open(args['outfile'], mode='wb')

    streamEncrypt (password, keyfile, infile, outfile)

if __name__ == "__main__":
    main()
