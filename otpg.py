import sys, argparse, getpass, binascii
from operator import mul

def binnifyString (string):
    binString = bin(int(binascii.hexlify(string), 16))[2:]
    if len(binString) % 4 == 3:
        binString = '0' + binString
    elif len(binString) % 4 == 2:
        binString = '00' + binString
    elif len(binString) % 4 == 1:
        binString = '000' + binString
    return binString

def rotatePassword (password):
    binPass = binnifyString (password)
    rotatedBinPass = int(binPass[1:] + binPass[:1], 2)
    rotatedHexPass = '%x' % rotatedBinPass
    if len(rotatedHexPass) % 2 != 0:
        rotatedHexPass = '0' + rotatedHexPass
    rotatedPassword = binascii.unhexlify(rotatedHexPass)
    return rotatedPassword

def findStartingPoint (password):
    passArray = [ ord(char) for char in password ]
    return reduce (mul, passArray, 1) % sum(passArray)

def streamEncrypt (password, keyfile, infile):
    passNumber = 0
    currentPosition = 0
    fileSize = keyfile.size()
    keyLengthArray = [16, 24, 32]
    while True:
        print "Pass Number : %d" % passNumber

        startPoint = findStartingPoint (password)
        print "Starting Point : %s" % startPoint

        keyLen = keyLengthArray[startPoint % 3]
        print "Key Length : %s" % keyLen

        password = rotatePassword (password)
        passNumber = passNumber + 1

def main ():
    argParser = argparse.ArgumentParser (description = 'Parse arguments for One Time Pad Generator')
    argParser.add_argument ('-p', '--passfile', help="File to read password from")
    argParser.add_argument ('-k', '--keyfile', help="File to generate keys", required=True)
    argParser.add_argument ('-i', '--infile', help="File to be encrypted")

    args = vars(argParser.parse_args())

    if args['passfile'] == None:
        password = getpass.getpass('Encryption Password: ')
    else:
        password = open(args['passfile']).read().strip()

    print "User entered password : %s" % password
    print "File to read password from : %s" % args['passfile']
    print "File to use to generate Keys : %s" % args['keyfile']

    if args['infile'] == None:
        print "Reading input from stdin: "
        infile = sys.stdin
    else:
        infile = open(args['infile'])
        print "Reading input from file : %s" % args['infile']

    keyfile = open(args['keyfile'])

    streamEncrypt (password, keyfile, infile)

if __name__ == "__main__":
    main()
