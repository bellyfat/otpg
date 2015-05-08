One Time Pad Generator
===

OTPG is a python script which uses a keystore containing randomly generated data and a password to generate a One Time Pad which can be used to encrypt messages of arbitrary lengths.

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
