import numpy as np
from players import *
import random,os 
from grids import *
from ships import *

class StackMoves:
    def __init__(self):
        self.stack = []

    def StackPush(self,item):
        self.stack.insert(0,item)

    def StackPeek(self):
        return self.stack[0]

    def StackPop(self):
        return self.stack.pop(0)

class Q_Learning_Agent(Player):
    def __init__(self,name,epsilon,learning_rate,discount_factor,opponent):
        super().__init__(name)
        self.state = None 
        self.x = None 
        self.y = None
        self.epsilon = epsilon
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.opponent = opponent
        if os.path.exists('q_table.txt'):
            self.q_table = self.LoadQTable()
        else:
            self.q_table = np.zeros((2,100))
        self.states = ["X","O"]

    def ResetEnvironment(self): 
        self._grids = Grid()
        self._ships = self.SetUpShips()
        self._total_ships = 5

    def SetUpEnvironmentShips(self):
        for ship in self._ships:
            ship.PlaceRandomShip()

    def ChooseAction(self,state,epsilon):
        random_num = np.random.random()
        if random_num > epsilon:
            #print("\nIndex of maximum value in array: ",np.argmax(self.q_table[state])) For testing
            return np.argmax(self.q_table[state])
        else:
            random_num = random.randint(0,99)
            #print(f"\nRandom action: {y}\n") For testing
            return random_num

    def GetTotalActions(self):
        actions = []
        for i in range(len(self._grids.GetTotalCoordinates())):
            actions += self._grids.GetTotalCoordinates()[i]
        return actions

    def UpdateQTable(self,state,action,reward,new_state):
        #print(f"Values passed into method: State {state}, action {action}, reward {reward}, new state {new_state}")  For testing
        #print(f"Values for bellman equation: Reward {reward}, Discount factor {self.discount_factor}, Learning rate {self.learning_rate}, max value of array {max(self.q_table[new_state])}, Current Q-value {self.q_table[state][action]}")  For testing
        temporal_difference = reward + self.discount_factor * max(self.q_table[new_state]) - self.q_table[state][action]
        #print(f"Temporal difference {temporal_difference}")  For testing
        q_value = self.q_table[state][action] + self.learning_rate * (temporal_difference)
        #print(f"Q-Value: {q_value}")  For testing
        self.q_table[state][action] = q_value

    def ValidAction(self,x,y):
        if repr(self.opponent.GetGrids().GetShipGrid()[x][y]) == "X" or repr(self.opponent.GetGrids().GetShipGrid()[x][y]) == "O":
            return True
        else:
            return False  

    def GetInitialAction(self):
        x = np.random.randint(0,9)
        y = np.random.randint(0,9)
        return x,y

    def GetState(self,x,y):
        ship = repr(self.opponent.GetGrids().GetShipGrid()[x][y])
        value = self.opponent.GetGrids().GetShipGrid()[x][y].GetValue()
        if ship == "B":
            self.opponent.GetBattleship().GetLocation().remove(value)
        elif ship == "C": 
            self.opponent.GetCarrier().GetLocation().remove(value)
        elif ship == "c":
            self.opponent.GetCruiser().GetLocation().remove(value)
        elif ship == "S":
            self.opponent.GetSubmarine().GetLocation().remove(value)
        elif ship == "D":
            self.opponent.GetDestroyer().GetLocation().remove(value)
        self.opponent.GetGrids().GetShipGrid()[x][y].SetSelected()
        return self.states.index(repr(self.opponent.GetGrids().GetShipGrid()[x][y]))

    def GetCoordinates(self,action):
        coordinate = self.GetTotalActions()[action]
        x = self.opponent.GetGrids().GetRowIndex()[coordinate[0]]
        y = int(coordinate[1])
        return x,y

    def SaveQTable(self):
        np.savetxt("q_table.txt",self.q_table)

    def LoadQTable(self):
        return np.loadtxt("q_table.txt")

    def HitGrid(self):
        # print("\n\n\nAI TURN: ",self._turn) For testing
        if self._turn == 1:
            # self.GetGrids().DisplayGrid()  for testing purposes 
            x,y = self.GetInitialAction()
            #print(f"Initial x coordinate {x}, initial y coordinate {y}\n\n") For testing
            state = self.GetState(x,y)
            #print(f"Initial state {state}  {self.states[state]}\n\n")  For testing
            action = self.ChooseAction(state,self.epsilon)
            #print(f"Initial action {action}\n\n")  For testing
        else:
            x = self.x
            y = self.y
            while self.ValidAction(x,y):
                # print(self.x,self.y,"\n\n") For testing
                action = self.ChooseAction(self.state,self.epsilon)
                #print("ACTION:",action,"\n\n")  For testing
                x,y = self.GetCoordinates(action) 
                #print("X value: ",x,"Y value: ",y,"\n\n")  For testing
                # self.opponent.GetGrids().DisplayGrid() For testing
            # state = self.GetState(x,y)  For testing
            # print("STATE:",state,self.states[state],"\n\n") For testing
            state = self.state
        reward = self.opponent.GetGrids().GetShipGrid()[x][y].GetReward()
        #print("REWARD:",reward,"\n\n")  For testing
        # x,y = self.GetCoordinates(action) For testing
        # print("X,Y",x,y)  For testing
        new_state = self.GetState(x,y)
        #print("NEW STATE:",new_state,self.states[new_state],"\n\n") For testing
        #print("Q_TABLE: ",self.q_table,"\n\n") For testing
        self.UpdateQTable(state,action,reward,new_state)
        self.SaveQTable()
        self.state = new_state
        self.x = x
        self.y = y
        for ship in range(len(self.opponent.GetShips())):
            self.opponent.GetShips()[ship].ShipStatus(self)
