One Time Pad Generator
===

OTPG is a python script which uses a keystore containing randomly generated data and a password to generate a One Time Pad which can be used to encrypt messages of arbitrary lengths.

This version of the script uses a simple XOR encryption. Each byte of the message is XOR'd with a corresponding byte from the OTP.

Intermediate passwords in the OTP are generated in 16, 24 or 32 Bytes (128, 192 or 256 bits) which can be used for other encryption techniques such as the AES.

```
usage: otpg.py [-h] [-p PASSFILE] -k KEYFILE -i INFILE [-o OUTFILE]

Parse arguments for One Time Pad Generator

optional arguments:
  -h, --help            show this help message and exit
  -p PASSFILE, --passfile PASSFILE
                        File to read password from
  -k KEYFILE, --keyfile KEYFILE
                        File to generate keys
  -i INFILE, --infile INFILE
                        File to be encrypted
  -o OUTFILE, --outfile OUTFILE
                        File to write encrypted content
```

##Encryption
```
python2 otpg.py -p passwordFile -k keystore -i plain.txt -o encr.txt
```

##Decryption
```
python2 otpg.py -p passwordFile -k keystore -i encr.txt -o decr.txt
```

##Verification
```
md5sum encr.txt decr.txt plain.txt
1541a2e8f70fcaf248701820d13e62a5  encr.txt
2180c3ef87ce21c27e7c10052b7c105e  decr.txt
2180c3ef87ce21c27e7c10052b7c105e  plain.txt
```
