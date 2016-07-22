import os
import time
from flask import Flask, render_template, request, session
from werkzeug import secure_filename
from mydirectory.classes import Data
from mydirectory.classes import RRC
from mydirectory.classes import SYS
from mydirectory.classes import Voip

UPLOAD_FOLDER = 'C:/Users/ss5399/Desktop/test/files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def login_page():
    names = []
    for name in os.listdir("C:/Users/ss5399/Desktop/test/templates/graphs"):
        names.append(name)
    return render_template('login.html', names=names)


@app.route('/home', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        user_name = request.form['user_name']
        session['user_name'] = user_name
        directory = ['C:/Users/ss5399/Desktop/test/static/graphs/'+user_name,
                     'C:/Users/ss5399/Desktop/test/templates/graphs/'+user_name]
        for file in directory:
            if not os.path.exists(file):
                os.makedirs(file)
        return render_template('home.html', name=user_name)
    if request.method == 'GET':
        user_name = session.get('user_name')
        return render_template('home.html', name=user_name)	


@app.route('/Foldermenu')
def generated_graph():
    names = []
    user_name = session.get('user_name')
    for name in os.listdir("C:/Users/ss5399/Desktop/test/templates/graphs/" + user_name):
        names.append(name)
    return render_template('Foldermenu.html', names=names)


@app.route('/Graphmenu', methods=['GET', 'POST'])
def display_folders():
    if request.method == 'POST':
        names=[]
        result = request.form['Name']
        user_name = session.get('user_name')
        session['file_path'] = result
        for name in os.listdir("C:/Users/ss5399/Desktop/test/templates/graphs/" + user_name+'/'+result):
            names.append(name)
        return render_template('Graphmenu.html', names=names)


@app.route('/Graph', methods=['GET', 'POST'])
def display_graphs():
    if request.method == 'POST':
        names=[]
        result = request.form['Name']
        user_name = session.get('user_name')
        file_path = session.get('file_path')
        return render_template('graphs/' +user_name+'/'+ file_path+'/'+ result)


@app.route('/upload')
def upload_files():
    return render_template('upload.html')


@app.route('/uploaded', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        graph = request.form['graph_name']
        date = time.strftime("%m_%d_%Y")
        graph = graph + '_' + date
        file = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
        name = file[:-4]
        session['name'] = name
        session['graph'] = graph
        session['date'] = date
        user_name = session.get('user_name')
        directory = ['C:/Users/ss5399/Desktop/test/static/graphs/'+user_name +'/'+date,
                     'C:/Users/ss5399/Desktop/test/templates/graphs/'+user_name+'/'+time.strftime("%m_%d_%Y")]
        for file in directory:
            if not os.path.exists(file):
                os.makedirs(file)
        if 'RRC' in name:
            graph = graph + '_RRC'
            test = RRC(name, user_name, graph, date).plot_data()
            return render_template('Graphtemplate.html', name = graph, user_name=user_name, time = date, test = test)
            #return render_template('/graphs/'+user_name+'/'+date+'/'+name +'.html')
        elif 'SYS' in name:
            return render_template('SYSmenu.html')
        elif 'Voip' in name:
            return render_template('Voipmenu.html')            
        else:
            return render_template('home.html')


@app.route('/SYSmenu', methods=['GET', 'POST'])
def display_SYS():
    if request.method == 'POST':
        result = request.form['Name']
        file_name = session.get('name')
        user_name = session.get('user_name')
        graph = session.get('graph')
        date = session.get('date')
        graph = graph + '_SYS'
        if result == 'A: Time vs. DL Throughput':
            SYS(file_name, user_name, graph, date).plot_data('A')
            return render_template('/graphs/'+user_name+'/'+date+'/'+graph+'_DL.html')
        elif result == 'B: Time vs. UL Throughput':
            SYS(file_name, user_name, graph, date).plot_data('B')
            return render_template('/graphs/'+user_name+'/'+date+'/'+graph+'_UL.html')


@app.route('/Voipmenu', methods=['GET', 'POST'])
def display_Voip():
    if request.method == 'POST':
        result = request.form['Name']
        file_name = session.get('name')
        user_name = session.get('user_name')
        graph = session.get('graph')
        date = session.get('date')
        graph = graph + '_VoIP'
        if result == "A: VoLTE Attempts":
            Voip(file_name, user_name, graph, date).plot_data('A')
            return render_template('/graphs/'+user_name+'/'+date+'/'+graph+'_Attempts.html')
        elif result == "B: Dropped Call Rate":
            Voip(file_name, user_name, graph, date).plot_data('B')
            return render_template('/graphs/'+user_name+'/'+date+'/'+graph+'_Dropped.html')

if __name__ == '__main__':
    app.secret_key = 'hi'
    app.run(debug=True)
