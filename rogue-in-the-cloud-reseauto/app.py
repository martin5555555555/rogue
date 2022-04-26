from flask import Flask, render_template, make_response
from flask_socketio import SocketIO
from flask import request
import requests
from game_backend import Game
import uuid

app = Flask(__name__)
socketio = SocketIO(app)
game = Game()

domain_lists = []
number_players = 0 
dico_correspondance = {}

@app.route("/")
def index():
    map = game.getMap()
    temp  = render_template("index.html", mapdata=map, n_row=len(map), n_col=len(map[0]) )
    resp = make_response(temp)
    id_user = getcookie()
    if id_user == None:
        return setcookie(resp) 
    return resp

@socketio.on("move")
def on_move_msg(json, methods=["GET", "POST"]):
    print("received move ws message")
    global dico_correspondance
    dx = json['dx']
    dy = json["dy"]
    user_id = json["user_id"]
    print(dico_correspondance)
    numero_joueur = dico_correspondance[user_id]
    
    data, ret = game.move(dx,dy, numero_joueur)
    if ret:
        socketio.emit("response", data)

@socketio.on("memorize")



@socketio.on("deconnection")
def on_connection_msg(json, methods=["GET", "POST"]):
    print("received connection ws message")
    global number_players
    global dico_correspondance
    global domain_lists
    
    
    

def setcookie(resp):
    id_user = uuid.uuid1()
    global dico_correspondance
    global number_players
    dico_correspondance[str(id_user)] = number_players
    number_players += 1
    game.add_player(str(id_user))
    print(dico_correspondance)


    
    resp.set_cookie('user_id', str(id_user))
    return resp

def getcookie():
   username = request.cookies.get('user_id')
   return username

@app.route('/cookie/', methods = ['POST', 'GET'])
def cookie():
        resp = requests.request("POST", 'http://127.0.0.1:5001/set-cookie/')
        return resp




 
        

if __name__=="__main__":
    socketio.run(app, port=5001)


