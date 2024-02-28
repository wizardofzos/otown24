# -*- coding: utf-8 -*-
from flask import Flask,request,jsonify,redirect,url_for,make_response
from flask import render_template
from functools import wraps
from flask import Response

import datetime
import random

from subprocess import PIPE, Popen
import os

from itertools import islice

apiroot = '/api/v1/'

app = Flask(__name__)

app.debug = True



@app.route('/')
def home():
    # Get the members of USER.Z25A.PARMLIB
    cmd = ['tsocmd', "LISTDS 'USER.Z25A.PARMLIB' MEMBERS"]
    p = Popen(cmd,stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()
    tsout = out.decode('utf-8').split('\n')
    print(tsout)
    
    dcb = tsout[2].split()
    volser = tsout[4]
    library = f"{tsout[0]} (RECFM={dcb[0]}, LRECL={dcb[1]}, BLKSIZE={dcb[2]}, DSORG={dcb[3]}, VOLSER={volser}"
    members1 = tsout[6:-1]
    # rip spaces
    members = [x.strip() for x in members1]
    # split members in lists of max-6
    amt = int(len(members) / 6)
    sizes = []
    for i in range(amt):
         sizes.append(6)
    in1 = iter(members)
    filelist = [list(islice(in1, elem)) for elem in sizes]
    
    return render_template('pages/home.html', library=library, filelist=filelist)

@app.route('/view/<member>')
def view(member):
    # Get the content, copy to /tmp, cat the file, then delete it again
    # Much efficient, very USS, such wow :)
    os.system(f"cp \"//'USER.Z25A.PARMLIB({member})'\" /tmp/b")
    cmd = ['cat', "/tmp/b"]
    p = Popen(cmd,stdout=PIPE, stderr=PIPE)
    out,err = p.communicate()
    # os.system(f"rm /tmp/b")
    data = out.decode('utf-8').replace(' ','&nbsp;').replace("'","&#39;").split('\n')
    document = '<pre>'

    for line in data:
         document += f"{line}<br />"
    document += "</pre>"
    print(document)
    return render_template('/pages/edit.html', document=document, member=member)

# Catch all :)
cool404s = [
		'WR2FvrU-NIM',
		'wNVCJj642n4',
		'dn_CjkNtl6s',
		'f5IRI4oHKNU',
		]





@app.route('/<path:path>')
def catch_all(path):
	return render_template('pages/404.html', video=random.choice(cool404s))
