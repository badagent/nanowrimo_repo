#!/usr/bin/env python3
import argparse
import os
import sys
from cryptography.fernet import Fernet


NOVEL_DIR = '.'+os.sep+'novel'
NOVEL_EXTENSION = '.md'
ENC_EXTENSION = '.enc'
OUT_FILE = '.'+os.sep+'out'+os.sep+'novel.md'
TEMPLATE_TEXT = "# Chapter %d\nAdd some content"
TEMPLATE_NAME = "chapter_%s.md"
#Parser Arguments
parser = argparse.ArgumentParser(description='NaNoWriMo Management Script')
parser.add_argument('-c','--count',action='store_true',help='Output wordcount')
parser.add_argument('-k','--generatekey',action='store_true',help='Generate new Key and store to secret.key')
parser.add_argument('-e','--encrypt',action='store_true',help='Encrypt Novel')
parser.add_argument('-d','--decrypt',action='store_true',help='Decrypt Novel')
parser.add_argument('-m','--merge',action='store_true',help='Merge Novel')
parser.add_argument('-g','--generate',metavar='N',help='Generate Template with N chapters')
args = parser.parse_args();

def generateKey():
    key = Fernet.generate_key()
    #TODO Safety: Don't overwrite old key
    with open("secret.key",'w') as tmp:
        tmp.write(key)

def loadKey():
    with open("secret.key",'r') as tmp:
        key = tmp.read()
    return key
    
def getNovelFiles(path,extension):
    if(path[-1:]==os.sep):
        path=path[:-1]
    files = []
    for filename in os.listdir(path):
        if(filename[-len(extension):]==extension):
            files.append(path+os.sep+filename)
    return files

def generate(path,extension,numberOfChapters):
    for i in range(numberOfChapters):
        chapter = i+1
        filename = path + os.sep + TEMPLATE_NAME%str(chapter).zfill(2)
        with open(filename,'w') as tmp:
            tmp.write(TEMPLATE_TEXT%chapter)
        print(filename)



def merge(path,extension,outfile):
    files = getNovelFiles(path,extension)
    print(files)
    with open(outfile,'w') as out:
        for file in files:
            with open(file,'r') as tmp:
                text = tmp.read()
                print(text)
                out.write(text)
                out.write('\n---\n')

def encrypt(path,extension,enc_extension):
    key = loadKey()
    f = Fernet(key)
    files = getNovelFiles(path,extension)
    for file in files:
        file_enc = file+enc_extension
        print("%s -> %s"%(file,file_enc))
        with open(file,'r') as plain:
            token = f.encrypt(plain.read())
            with open(file_enc,'w') as cipher:
                cipher.write(token)

def decrypt(path,extension,enc_extension):
    key = loadKey()
    f = Fernet(key)
    files = getNovelFiles(path,enc_extension)
    for file in files:
        file_dec = file[:-len(enc_extension)]
        print("%s -> %s"%(file,file_dec))
        with open(file,'r') as cipher:
            plaintext = f.decrypt(cipher.read())
            with open(file_dec,'w') as plain:
                plain.write(plaintext)

def getWordCount():
    files = getNovelFiles(NOVEL_DIR,NOVEL_EXTENSION)
    count = 0
    for file in files:
        with open(file,'r') as tmp:
            text = tmp.read()
            splitted = text.split()
            print("%s (%d)"%(file,len(splitted)))
            count = count + len(splitted)
    print("Total Word count: %d"%count)

if(args.count):
    getWordCount()
    sys.exit()

if(args.generatekey):
    generateKey()
    print("Generated Key. Exiting.")
    sys.exit()

if(args.encrypt):
    encrypt(NOVEL_DIR,NOVEL_EXTENSION,ENC_EXTENSION)
    print("Done.")
    sys.exit(0)

if(args.decrypt):
    decrypt(NOVEL_DIR,NOVEL_EXTENSION,ENC_EXTENSION)
    print("Done.")
    sys.exit(0)

if(args.merge):
    merge(NOVEL_DIR,NOVEL_EXTENSION,OUT_FILE)
    print("Done.")
    sys.exit(0)

if(args.generate):
    numberOfChapters = int(args.generate)
    print("Generating %d chapters in directory %s"%(numberOfChapters,NOVEL_DIR))
    generate(NOVEL_DIR,NOVEL_EXTENSION,numberOfChapters)
