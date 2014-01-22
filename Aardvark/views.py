from flask import render_template
from Aardvark import Aardvark

@Aardvark.route('/')
def index():
    return render_template('index.html')
