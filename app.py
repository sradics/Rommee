from flask import Flask, render_template, request, session
from rommee_backend import *
from flask_socketio import SocketIO, emit,join_room,leave_room, rooms
import json
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'


socketio = SocketIO(app ,cors_allowed_origins="*",ping_timeout=20,http_compression=False)


games = {}
rooms_and_games = {}

def create_random_user_id():
    MAX_LIMIT = 255

    random_string = ''

    for _ in range(10):
        random_integer = random.randint(0, MAX_LIMIT)
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string



@app.route('/testsocket', methods=['GET','POST'])
def index():
    if not 'player' in session:
        session["player"]=create_random_user_id()
    print(session["player"])
    return render_template('index.html')

@socketio.on('next_stone')
def next_stone():
    game = games[session["current_game"]]
    if game.status == GameStatus.FINISHED:
        sendGameFinishedMessage()
        return
    stone = game.deck.pop_next_stone()
    render_next_stone(stone)

def render_next_stone(stone):
    game = games[session["current_game"]]
    game.playerDecks[session["player"]].append(stone)
    response = {'data': stone}
    responseAsJson = json.dumps(response, cls=StoneEncoder)
    emit('next_stone', json.loads(responseAsJson))
    render_remaining_piles()




@socketio.on('init_game')
def init_game(message):

    number_players = message['data']
    game = Game(int(number_players))

    global games
    games[game.gameId]=game
    session["current_game"]=game.gameId


    join_room(game.gameId)
    rooms_and_games[game.gameId]=game

    response = {'data':game.gameId}
    responseAsJson = json.dumps(response)

    emit('init_game', json.loads(responseAsJson))


def render_remaining_piles():
    game = games[session["current_game"]]
    response = {'data': game.deck.flatDeck}
    responseAsJson = json.dumps(response, cls=StoneEncoder)

    emit('remaining_piles', json.loads(responseAsJson), broadcast=True, room=game.gameId)


@socketio.on('getdeck')
def get_deck(message):
    global games

    game_id = message['gameId']
    if game_id != None and len(game_id)>0:
        join_room(game_id)
        game = games[game_id]
        session["current_game"]=game.gameId
        deck = game.assign_player(session["player"])
        if deck == None:
            send_game_message("Ungültiger Spieler",False,game)
            return
        game.playerNames[session["player"]] = message['playerName']

        if len(game.piles)==0:
            emit('requestDeck', broadcast=True, room=game.gameId)
            game.status=GameStatus.STARTED
            send_game_message("Spiel startet. SpielerIn " + str(game.playerNames[game.get_current_player()]) + " beginnt", True,game)
        else:
            send_game_message("Warte auf weitere "+str(len(game.piles))+" SpielerInnen", True,game)



@socketio.on('fetchdeck')
def fetch_deck():
    renderDeck()
    render_remaining_piles()

def renderDeck():
    game = games[session["current_game"]]
    player = game.playerDecks[session["player"]]

    response = {'data': player, 'playerId': session["player"]}
    pilesAsJson = json.dumps(response, cls=StoneEncoder)

    emit('getdeck', json.loads(pilesAsJson))



@socketio.on('replace_joker')
def replace_joker(message):
    game = games[session["current_game"]]
    if game.status == GameStatus.FINISHED:
        sendGameFinishedMessage()
        return

    stone = message['stone']
    joker = message['joker']
    playerWithJoker = message['playerId']

    finishAreasWithJoker = game.playerFinishAreas[playerWithJoker]
    jokerStone = None
    deckToAddJoker = game.playerDecks[session["player"]]
    replaceIndex = 0
    replaceArray = None

    for num in list(range(0, len(finishAreasWithJoker))):
        finishArea = finishAreasWithJoker[num]
        for numFinishArea in list(range(0, len(finishArea))):
            stoneFinishArea = finishArea[numFinishArea]
            if stoneFinishArea.id == joker:
                jokerStone = stoneFinishArea
                replaceArray = finishArea
                replaceIndex = numFinishArea
                break


    replaceStone = None
    for num in list(range(0, len(deckToAddJoker))):
        stoneInDeck = deckToAddJoker[num]
        if stoneInDeck.id == stone:
            replaceStone = deckToAddJoker.pop(num)
            break
    replaceArray[replaceIndex] = replaceStone

    refresh_finish_area_others()
    render_next_stone(jokerStone)


@socketio.on('pick_from_temp_space')
def pick_from_temp_space(message):
    game = games[session["current_game"]]

    if game.status == GameStatus.FINISHED:
        sendGameFinishedMessage()
        return
    stoneId = message['stone']

    playerDeck = game.playerDecks[session["player"]]

    lengthTempSpace = len(game.tempSpace.space)
    index = 0
    for num in list(range(0, lengthTempSpace)):
        stoneTempSpace = game.tempSpace.space[num]
        if stoneTempSpace.id==stoneId:
            index = num
            break
    stones_to_add = game.tempSpace.space[index:len(game.tempSpace.space)]
    game.tempSpace.space = game.tempSpace.space[0:index]
    playerDeck.extend(stones_to_add)
    renderDeck()

    response = {'data': game.tempSpace.space}
    tempSpaceAsJson = json.dumps(response, cls=StoneEncoder)
    emit('tempSpace', json.loads(tempSpaceAsJson), broadcast=True, room=game.gameId)


@socketio.on('add_stone')
def add_stones(message):
    game = games[session["current_game"]]

    if game.status == GameStatus.FINISHED:
        sendGameFinishedMessage()
        return

    stone = message['stone']
    row = int(message['row'])
    appendix = message['appendix']
    playerId = message['playerId']
    playerDeck = game.playerDecks[session["player"]]

    for num in list(range(0, len(playerDeck))):
        stoneInDeck = playerDeck[num]
        if stoneInDeck.id == stone:
            if (appendix=="_start"):
                game.playerFinishAreas[playerId][row].insert(0, stoneInDeck)
            else:
                game.playerFinishAreas[playerId][row].append(stoneInDeck)
            stoneValue = calc_stone_value_in_area(stoneInDeck,game.playerFinishAreas[playerId][row])
            playerDeck.pop(num)

            if playerId!=session["player"]:

                game.addedStoneIndex[stoneInDeck.id]=AddedStone(stoneValue,stoneInDeck,session["player"])
            break
    refresh_finish_area_others()


@socketio.on('publish_stones')
def publish_stones(message):
    game = games[session["current_game"]]
    if game.status==GameStatus.FINISHED:
        sendGameFinishedMessage()
        return

    published_stones = message['data'];

    game.add_stones_to_finish_areas(published_stones, session["player"])
    refresh_finish_area_others()

def send_game_message(message, broadcast,game):
    response = {'data': message}
    if broadcast==True:
        emit('game_message', response, broadcast=broadcast, room=game.gameId)
    else:
        emit('game_message', response, broadcast=broadcast)


def refresh_finish_area_others():
    game = games[session["current_game"]]
    keys = game.playerFinishAreas.keys()
    others = {}
    names = {}
    for key in keys:
        others[key]=game.playerFinishAreas[key]
        names[key]=game.playerNames[key]
        #if key != session["player"]:


    response = {'data': others,'names':names}
    tempSpaceAsJson = json.dumps(response, cls=StoneEncoder)
    emit('finishArea_others', json.loads(tempSpaceAsJson), broadcast=True, room=game.gameId)


@socketio.on('list_games')
def list_games():
    gamesInfo = []
    for game_keys in games.keys():
        game = games[game_keys]
        gamesInfo.append({'id':game.gameId,'status':game.status.name,'num_players':game.numberOfPlayers,'joined':len(game.players)})
    resultAsJson = json.dumps(gamesInfo)
    emit('list_all_games', json.loads(resultAsJson))


@socketio.on('print_stats')
def print_status():
    game = games[session["current_game"]]
    resultAsJson = json.dumps(game.game_stats(), cls=StoneEncoder)
    emit('stats', json.loads(resultAsJson), broadcast=True, room=game.gameId)
    print(str(game.game_stats()))

@socketio.on('droppedstone_temp')
def dropped_stone_temp(message):
    stoneIdAsStr = message['data'][len("draggable_"):]

    if 'current_game' in session:
        game = games[session["current_game"]]
        if game.status == GameStatus.FINISHED:
            sendGameFinishedMessage()
            return

        game.add_stone_to_temp_space(stoneIdAsStr,session["player"])
        response = {'data': game.tempSpace.space}
        tempSpaceAsJson = json.dumps(response, cls=StoneEncoder)
        emit('tempSpace', json.loads(tempSpaceAsJson), broadcast=True, room=game.gameId)

        if len(game.playerDecks[session["player"]])==0: #game finished
            game.finisher=session["player"]
            game.status=GameStatus.FINISHED
            send_game_message("Spiel beendet. Spieler "+game.playerNames[session["player"]]+" hat das Spiel beendet",True,game)
            print_status()
            return

        if len(game.deck.flatDeck)==0: #stones finished
            game.status = GameStatus.FINISHED
            send_game_message("Spiel beendet. Alle Spielsteine verwendet",True,game)
            print_status()
            return

        response = {'next_player': game.get_next_player()}
        emit('next_player', response, broadcast=True, room=game.gameId)
        send_game_message("Spieler "+game.playerNames[game.get_current_player()]+" ist am Zug",True,game)

def sendGameFinishedMessage():
    send_game_message("Spiel beendet.", False, games[session["current_game"]])


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect')
def test_connect():
    emit('my response', {'data': 'Connected'})
    #print("Rooms when connect:" + str(socketio.server.manager.rooms["/"].keys()))

@socketio.on('disconnect')
def test_disconnect():
    #print("Rooms after disconnect:"+str(socketio.server.manager.rooms["/"].keys()))
    print('Client disconnected')

    for game_rooms_key in rooms_and_games.keys():
        room_still_open = False
        for key in socketio.server.manager.rooms["/"].keys():
            if key == game_rooms_key:
                room_still_open = True
                break
        if room_still_open == False:
            try:
                rooms_and_games.pop(game_rooms_key)
                games.pop(game_rooms_key)
            except KeyError:
                pass



if __name__ == '__main__':
    print("test")
    socketio.run(app)
