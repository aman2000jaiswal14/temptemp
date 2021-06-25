import os
from flask import Flask,render_template,request

from flask_cors import cross_origin


app = Flask(__name__)

import random

range1 = (97, 122)
range2 = (65, 90)
range3 = (48, 57)


def encodeOrg(org):
    orgflg = 0
    encode = ''
    for i in org:
        chflg = 0
        chflg2 = 0
        if (range1[0] <= ord(i) <= range1[1]):
            chflg2 = 0
        elif (range2[0] <= ord(i) <= range2[1]):
            chflg2 = 1
        else:
            chflg = 1

        if (orgflg == 0):
            ch = '(' + str(chflg) + bin(ord(i))[2:] + str(chflg2) + ')'
            orgflg = 1
        else:
            ch = '(' + str(chflg2) + bin(ord(i))[2:] + str(chflg) + ')'
            orgflg = 0
        encode += ch
    return encode


def encodeUser(user):
    usermapper = {'@': '$', '$': '@', '&': '^', '^': '&', '#': '+', '+': '#', '*': '%', '%': '*'}
    encode = ''
    for i in user:
        onebit = 0
        twobit = 0
        non = 0
        val = i
        if (range1[0] <= ord(i) <= range1[1]):
            onebit = 0
            if (range1[0] <= ord(i) <= range1[0] + 12):
                twobit = 0
            else:
                i = chr(range1[0] + range1[1] - ord(i))

                twobit = 1
        elif (range2[0] <= ord(i) <= range2[1]):
            onebit = 1
            i = i.lower()
            if (range1[0] <= ord(i) <= range1[0] + 12):
                twobit = 0
            else:
                i = chr(range1[0] + range1[1] - ord(i))
                twobit = 1
        elif (range3[0] <= ord(i) <= range3[1]):
            onebit = 2
            i = int(i)
            i = 9 - i
            i = str(i)
        else:
            non = 1
            if (i in usermapper):
                i = usermapper[i]

        if (non):
            encode += i
        else:
            encode += (i + str(onebit) + str(twobit))

    return encode


def decodeUser(user):
    userdmapper = {'@': '$', '$': '@', '&': '^', '^': '&', '#': '+', '+': '#', '*': '%', '%': '*'}
    duser = ''
    num = 0
    while (num < len(user)):
        u = user[num]
        if (range1[0] <= ord(u) <= range1[1] or range3[0] <= ord(u) <= range3[1]):
            onebit = int(user[num + 1])
            twobit = int(user[num + 2])
            if (onebit == 0):
                if (twobit == 1):
                    idd = ord(u) - range1[0]
                    idd = range1[0] + 25 - idd
                    u = chr(idd)


            elif (onebit == 1):
                if (twobit == 1):
                    idd = ord(u) - range1[0]
                    idd = range1[0] + 25 - idd
                    u = chr(idd)
                u = u.upper()
            elif (onebit == 2):
                u = int(u)
                u = 9 - u
                u = str(u)

            num += 3
        else:
            num += 1
            if (u in userdmapper):
                u = userdmapper[u]

        duser += u
    return duser


def encodePass(pas):
    usermapper = {'@': '+', '+': '@', '$': '*', '*': '$', '&': '^', '^': '&', '#': '%', '%': '#'}
    user = pas
    encode = ''
    for i in user:
        onebit = 0
        twobit = 0
        non = 0
        val = i
        if (range1[0] <= ord(i) <= range1[1]):
            onebit = 0
            if (range1[0] <= ord(i) <= range1[0] + 12):
                twobit = 0
            else:
                i = chr(range1[0] + range1[1] - ord(i))

                twobit = 1
        elif (range2[0] <= ord(i) <= range2[1]):
            onebit = 1
            i = i.lower()
            if (range1[0] <= ord(i) <= range1[0] + 12):
                twobit = 0
            else:
                i = chr(range1[0] + range1[1] - ord(i))
                twobit = 1
        elif (range3[0] <= ord(i) <= range3[1]):
            onebit = 2
            i = int(i)
            i = 9 - i
            i = str(i)
        else:
            non = 1
            if (i in usermapper):
                i = usermapper[i]

        if (non):
            encode += i
        else:
            encode += (i + str(onebit) + str(twobit))

    return encode


def addNoise(encode):
    noisetype = random.randint(0, 9)

    noiser = ''' $%^&*!@#~`abcdefghijklm*nopqurstuvwxyzABCDEF.,GHIJK>LMN<OPQRSTUVWXYZ1234567?89[]{|}+-'''
    n = len(noiser)

    noencode = ''
    if (noisetype % 2 == 0):
        for i in encode:
            noencode += i
            idd = random.randint(0, n - 1)
            noencode += noiser[idd]
    else:
        for num, i in enumerate(encode):
            idd = random.randint(0, n - 1)
            if (num % 3 == 0):
                noencode += noiser[idd]
            noencode += i

    noencode += str(noisetype)
    return noencode


def supernoise(noise):
    noisetype = random.randint(0, 9)

    noiser = ''' $%^&*!@#~`abcdefghijklm*nopqurstuvwxyzABCDEF.,GHIJK>LMN<OPQRSTUVWXYZ1234567?89[]{|}+-'''
    n = len(noiser)
    extra = ''
    for i in range(5):
        idd = random.randint(0, n - 1)
        extra += noiser[idd]
    return noise + extra


def encoder(org, user, pas):
    encode = ''
    encode += encodeUser(user)
    encode += encodeOrg(org)
    encode += encodePass(pas)
    encode = addNoise(encode)
    encode = supernoise(encode)
    return encode


def removeNoise(noencode):
    last = int(noencode[-1])
    noencode = noencode[:-1]
    encode = ''
    if (last % 2 == 0):
        for num, i in enumerate(noencode):
            if (num % 2 == 0):
                encode += i
    elif (last % 2 != 0):
        flg2 = 0
        for num, i in enumerate(noencode):
            if (flg2 != 0):
                encode += i
            flg2 += 1
            flg2 = flg2 % 4

    return encode


def removeSuperNoise(noencode):
    return noencode[:-5]


def splitEncode(encode):
    i1 = encode.index('(')
    i2 = -1
    for num, i in enumerate(encode):
        if (i == ')'):
            i2 = num

    return encode[:i1], encode[i1:i2 + 1], encode[i2 + 1:]


def decodeOrg(org):
    orglist = org.split(')')[:-1]
    dorg = ''
    for num, o in enumerate(orglist):
        chrflg = o[2]
        chrflg2 = o[-1]
        if (num % 2 != 0):
            chrflg, chrflg2 = chrflg2, chrflg
        o = o[2:-1]
        dorg += chr(int(o, 2))
    return dorg

    return org


def decodePass(pas):
    userdmapper = {'@': '+', '+': '@', '$': '*', '*': '$', '&': '^', '^': '&', '#': '%', '%': '#'}
    user = pas
    duser = ''
    num = 0
    while (num < len(user)):
        u = user[num]
        if (range1[0] <= ord(u) <= range1[1] or range3[0] <= ord(u) <= range3[1]):
            onebit = int(user[num + 1])
            twobit = int(user[num + 2])
            if (onebit == 0):
                if (twobit == 1):
                    idd = ord(u) - range1[0]
                    idd = range1[0] + 25 - idd
                    u = chr(idd)


            elif (onebit == 1):
                if (twobit == 1):
                    idd = ord(u) - range1[0]
                    idd = range1[0] + 25 - idd
                    u = chr(idd)
                u = u.upper()
            elif (onebit == 2):
                u = int(u)
                u = 9 - u
                u = str(u)

            num += 3
        else:
            num += 1
            if (u in userdmapper):
                u = userdmapper[u]

        duser += u
    return duser


def decoder(noencode):
    noencode = removeSuperNoise(noencode)
    encode = removeNoise(noencode)
    encodedUser, encodedOrg, encodedPas = splitEncode(encode)
    decode0, decode1, decode2 = decodeOrg(encodedOrg), decodeUser(encodedUser), decodePass(encodedPas)
    return decode0, decode1, decode2

    return decode

@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/toencode',methods=['GET','POST'])
@cross_origin()
def toencode():
    if (request.method == "POST"):
        org = request.form['org']
        user = request.form['user']
        pas = request.form['pas']
        enc = encoder(org, user, pas)
        return render_template('index.html',encoded_value=enc)
    else:
        return render_template('index.html')
@app.route('/decode',methods=['GET'])
@cross_origin()
def decodehomepage():
    return render_template('secret.html')

@app.route('/todecode', methods=['GET','POST'])
@cross_origin()
def todecode():
    if (request.method == "POST"):
        enc = request.form['enc']
        dorg, duser, dpas = decoder(enc)
        return render_template('secret.html',decoded_org=dorg,decoded_user=duser,decoded_pas = dpas)
    else:
        render_template('secret.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001)
