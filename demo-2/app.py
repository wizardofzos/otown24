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

from zoautil_py import datasets


apiroot = '/api/v1/'

app = Flask(__name__)

app.debug = True

allowed_pdses = ['USER.Z25A.PARMLIB','SYS1.PARMLIB','ADCD.Z25A.PARMLIB','SYS1.PROCLIB','USER.Z25A.PROCLIB']

@app.route('/')
@app.route('/<pds>')
def home(pds='USER.Z25A.PARMLIB'):

    if pds not in allowed_pdses:
         return render_template('pages/404.html')
    
    members = datasets.list_members(pds)
    # split members in lists of max-6
    amt = int(len(members) / 6)
    sizes = []
    for i in range(amt):
         sizes.append(6)
    in1 = iter(members)
    filelist = [list(islice(in1, elem)) for elem in sizes]
    
    return render_template('pages/home.html', library=pds, filelist=filelist, pdslist=allowed_pdses)

@app.route('/view/<member>')
def view(member):
    pds = member.split('(')[0]
    if pds not in allowed_pdses:
        return render_template('pages/404.html')
    # just use the zoau datasets.read function :)
    content = datasets.read(member)
    data = content.replace(' ','&nbsp;').replace("'","&#39;").split('\n')
    document = '<pre>'
    for line in data:
         document += f"{line}<br />"
    document += "</pre>"
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
