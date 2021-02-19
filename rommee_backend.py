from enum import Enum
from random import shuffle
import json
import random
from json import JSONEncoder
import uuid

class Game:
    def __init__(self, number_of_players):
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
                    newArea.append(stoneInDeck)

        finish_area.append(newArea)


    def add_stone_to_temp_space(self,stoneId,playerId):

        playerDeck = self.playerDecks[playerId]
        for num in list(range(0, len(playerDeck))):
            stoneInDeck = playerDeck[num]
            if stoneInDeck.id == stoneId:
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


def create_random_game_id():
    gameIdBase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    MAX_LIMIT = len(gameIdBase)

    random_string = ''

    for _ in range(10):
        random_integer = random.randint(0, MAX_LIMIT)
        # Keep appending random characters using chr(x)
        random_string += (gameIdBase[random_integer-1])
    return random_string

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
            return {'value':o.value, 'color':o.color.name, 'id':str(o.id)}



class Stone:
    def __init__(self, value,color):
        self.value = value
        self.color = color
        self.id = str(uuid.uuid4())

    def __repr__(self):
        return "{};{}".format(
            self.value, self.color
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



if __name__ == '__main__':
    main()