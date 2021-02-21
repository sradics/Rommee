from enum import Enum
from random import shuffle
import json
import random
from json import JSONEncoder
import uuid

class Game:
    def __init__(self, number_of_players):
        self.numberOfPlayers = number_of_players
        self.deck = RommeeDeck()
        self.piles = self.deck.distribute(number_of_players)
        self.playerDecks = {}
        self.gameId = create_random_game_id()
        self.tempSpace = TempSpace()
        self.playerFinishAreas = {}
        self.players = []
        self.currentPlayerIndex = None
        self.addedStoneIndex = {}
        self.playerNames = {}
        self.finisher = None
        self.status = GameStatus.NOT_STARTED

    def get_current_player(self):
        return self.players[self.currentPlayerIndex]

    def get_next_player(self):
        self.currentPlayerIndex=self.currentPlayerIndex+1
        if self.currentPlayerIndex>len(self.players)-1:
            self.currentPlayerIndex = 0
        return self.players[self.currentPlayerIndex]

    def add_stones_to_finish_areas(self,stones, playerId):
        if not playerId in self.playerFinishAreas:
            self.playerFinishAreas[playerId]=[]
        finish_area = self.playerFinishAreas[playerId]
        newArea = []
        playerDeck = self.playerDecks[playerId]
        for stone in stones:
            for num in list(range(0, len(playerDeck))):
                stoneInDeck = playerDeck[num]
                if stoneInDeck.id == stone:
                    stoneInDeck.position=None
                    newArea.append(playerDeck.pop(num))
                    break

        finish_area.append(newArea)


    def add_stone_to_temp_space(self,stoneId,playerId):

        playerDeck = self.playerDecks[playerId]
        for num in list(range(0, len(playerDeck))):
            stoneInDeck = playerDeck[num]
            if stoneInDeck.id == stoneId:
                stoneInDeck.position=None
                self.tempSpace.add_stone(playerDeck.pop(num))
                break


    def assign_player(self, playerId):
        if len(self.piles)==0:
            return None

        self.playerDecks[playerId] = self.piles.pop(random.randint(0 ,len(self.piles)-1))
        self.players.append(playerId)
        if len(self.playerDecks[playerId])==15:
            self.currentPlayerIndex=len(self.players)-1
        return self.playerDecks[playerId]

    def game_stats(self):
        total_all_players = {}
        for player in self.players:
            total_for_player = 0
            finished_points = 0
            in_deck_points = 0
            added_to_others = 0

            if player in self.playerFinishAreas:
                for area in self.playerFinishAreas[player]:
                    all_are_ones = True
                    for stone in area:
                        if stone.value!=1 and stone.value!=0: #not a one or a joker
                            all_are_ones = False

                    if all_are_ones:
                        for stone in area:
                            if stone.id not in self.addedStoneIndex: #stone not add by someone else
                                finished_points += 25
                    else:
                        previousValue = 0
                        for stone in area:
                            if stone.id in self.addedStoneIndex:
                                previousValue = stone.value
                                continue
                            if stone.value==0 and previousValue<9:
                                finished_points += 5
                            elif stone.value == 0 and previousValue >= 10:
                                finished_points += 10
                            elif stone.value==1 and previousValue<9:
                                finished_points += 5
                            elif stone.value==1:
                                finished_points += 10
                            elif stone.value>=10:
                                finished_points += 10
                            else:
                                finished_points += 5
                            previousValue = stone.value

            total_for_player+=finished_points

            for stoneKey in self.addedStoneIndex.keys():
                addedStone = self.addedStoneIndex[stoneKey]
                if addedStone.playerId == player:
                    added_to_others+=addedStone.value

            total_for_player+=added_to_others

            playerDeck = self.playerDecks[player]
            for num in list(range(0, len(playerDeck))):
                stoneInDeck = playerDeck[num]
                if stoneInDeck.value==0:
                    in_deck_points-=25
                elif stoneInDeck.value==1:
                    in_deck_points-=25
                elif stoneInDeck.value<10:
                    in_deck_points-=5
                elif stoneInDeck.value>=10:
                    in_deck_points-=10
            total_for_player+=in_deck_points
            if player == self.finisher:
                total_for_player+=25
            in_deck_info = in_deck_points
            if self.status!=GameStatus.FINISHED:
                in_deck_info = "*"

            if not player in self.playerFinishAreas: #player did not yet get out
                total_all_players[player] = {'has_finished': False,
                                             'player': self.playerNames[player],
                                             'total': -100,
                                             'finished': 0,
                                             'added': 0,
                                             'still_in_deck': -100}
            else:
                total_all_players[player]={'has_finished':(player == self.finisher),
                                       'player':self.playerNames[player],
                                       'total':total_for_player,
                                       'finished':finished_points,
                                       'added':added_to_others,
                                       'still_in_deck':in_deck_info}
        return total_all_players



def calc_stone_value_in_area(stone_to_check,area):
    stone_index = None
    for index in list(range(len(area))):
        stone = area[index]
        if stone.id == stone_to_check.id:
            stone_index = index
    if stone_index==None:
        return 0

    all_are_ones = True

    for stone in area:
        if stone.value != 1 and stone.value != 0:  # not a one or a joker
            all_are_ones = False

    if all_are_ones:
        return 25

    previous_stone = None
    next_stone = None
    if len(area)-1>stone_index:
        next_stone=area[stone_index+1]
    if stone_index!=0:
        previous_stone = area[stone_index-1]

    if previous_stone!=None and previous_stone.value!=0:
        if previous_stone.value<9:
            return 5
        else:
            return 10

    if previous_stone != None and previous_stone.value == 0:
        if next_stone==None:
            previousValue_2 = area[stone_index -2].value
            if previousValue_2 < 8:
                return 5
            return 10
        if next_stone.value==0:
            nextValue = area[stone_index + 2].value
            if nextValue<11 and nextValue!=1:
                return 5
            return 10
        if next_stone.value>10 or next_stone==1:
            return 10
        return 5

    if next_stone != None and next_stone.value!=0 and next_stone.value!=1:
        if next_stone.value>10:
            return 10
        else:
            return 5

    if next_stone != None and next_stone.value == 0:
        nextValue = area[stone_index + 2].value
        if nextValue < 11 and nextValue != 1:
            return 5
        return 10

    if next_stone != None and next_stone.value == 1:
        return 10




def create_random_game_id():
    gameIdBase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    MAX_LIMIT = len(gameIdBase)

    random_string = ''

    for _ in range(10):
        random_integer = random.randint(0, MAX_LIMIT)
        # Keep appending random characters using chr(x)
        random_string += (gameIdBase[random_integer-1])
    return random_string

class GameStatus(Enum):
    STARTED=1
    FINISHED=2
    NOT_STARTED=3



class Color(Enum):
    RED=1
    GREEN=2
    BLACK=3
    BLUE=4
    JOKER=5

    @staticmethod
    def convertFromString(value):
        c = None
        if value.upper() == "BLACK":
            c = Color.BLACK
        if value.upper() == "GREEN":
            c = Color.GREEN
        if value.upper() == "BLUE":
            c = Color.BLUE
        if value.upper() == "RED":
            c = Color.RED
        if value.upper() == "JOKER":
            c = Color.JOKER
        return c


class StoneEncoder(JSONEncoder):
        def default(self, o):
            return {'value':o.value, 'color':o.color.name, 'id':str(o.id), 'position':o.position}



class Stone:
    def __init__(self, value,color):
        self.value = value
        self.color = color
        self.id = str(uuid.uuid4())
        self.position = None

    def __repr__(self):
        return "{};{};{},{}".format(
            self.value, self.color, self.id, self.position
        )

class AddedStone:
    def __init__(self, value,stone,playerId):
        self.value = value
        self.stone = stone
        self.playerId = playerId

    def __repr__(self):
        return "{};{};{}".format(
            self.value, self.stone, self.playerId
        )

class TempSpace:
    def __init__(self):
        self.space = []

    def add_stone(self,stone):
        self.space.append(stone)

class RommeeDeck:
    def __init__(self):
        self.flatDeck = []
        self.fill_deck()


    def pop_next_stone(self):
        if len(self.flatDeck)==0:
            return None
        return self.flatDeck.pop()

    def fill_deck(self):
        stones = []
        stones.extend(self.create_stones(Color.RED))
        stones.extend(self.create_stones(Color.RED))
        stones.extend(self.create_stones(Color.GREEN))
        stones.extend(self.create_stones(Color.GREEN))
        stones.extend(self.create_stones(Color.BLACK))
        stones.extend(self.create_stones(Color.BLACK))
        stones.extend(self.create_stones(Color.BLUE))
        stones.extend(self.create_stones(Color.BLUE))
        stones.append(Stone(0, Color.JOKER))
        stones.append(Stone(0, Color.JOKER))

        shuffle(stones)
        self.flatDeck = stones

    def distribute(self, number_of_players):
        players_and_piles = []
        for player in list(range(0, number_of_players)):
            players_and_piles.append([])
        for num in list(range(0, 2)):
            for player in list(range(0,number_of_players)):
                for stoneNr in (list(range(0,7))):
                    players_and_piles[player].append(self.flatDeck.pop())
        #add one more stone for start player
        players_and_piles[0].append(self.flatDeck.pop())
        return players_and_piles



    def create_stones(self,color):
        stones = []
        for num in list(range(1,14)):
            stones.append(Stone(num,color))
        return stones

    def __repr__(self):
        return "Deck:  {} ".format(
            self.flatDeck
        )




def main():
    rommeeDeck = RommeeDeck()
    print(rommeeDeck.flatDeck)
    print(rommeeDeck.distribute(2))
    print(rommeeDeck.flatDeck)

def validate_area_stone_constellation(area):
    differentColors = False
    previousColor = None
    for stone in area:
        if previousColor==None:
            previousColor = stone.color
            continue
        if stone.color != previousColor and stone.color != Color.JOKER:
            differentColors = True
            break
    if differentColors:
        previousValue = None
        colorDict = {}
        for stone in area:
            if previousValue == 0:  # joker
                previousValue = stone.value

            if previousValue == None:
                previousValue = stone.value
                if stone.color!=Color.JOKER:
                    colorDict[stone.color]=stone.color
                    continue
            if previousValue != stone.value and stone.value!=0:
                return False
            if stone.color in colorDict and stone.color!=Color.JOKER:
                return False
            colorDict[stone.color]=stone.color
        return True

    previousValue = -1
    allStonesInOrder = False
    for stone in area:
        if stone.color != Color.JOKER:
            if stone.value <= previousValue:
                return False
            previousValue = stone.value
        allStonesInOrder = True
    return allStonesInOrder

if __name__ == '__main__':
    main()