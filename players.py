from grids import *
from ships import *

class Player:
    def __init__(self,name):
        self._name = name
        self._turn = 0
        self._total_ships = 5
        self._grids = Grid()    
        self._ships = self.SetUpShips()

    def SetUpShips(self):
        self._battleship = Battleship(self._grids)
        self._carrier = Carrier(self._grids)
        self._cruiser = Cruiser(self._grids)
        self._submarine = Submarine(self._grids)
        self._destroyer = Destroyer(self._grids)
        return [self._battleship,self._carrier,self._cruiser,self._submarine,self._destroyer]

    def GetBattleship(self):
        return self._battleship

    def GetCarrier(self):
        return self._carrier

    def GetCruiser(self):
        return self._cruiser

    def GetSubmarine(self):
        return self._submarine

    def GetDestroyer(self):
        return self._destroyer

    def GetTotalShips(self):
        return self._total_ships

    def DecreaseShip(self):
        self._total_ships -= 1 

    def GetGrids(self):
        return self._grids

    def GetShips(self):
        return self._ships

    def GetName(self):
        return self._name

    def GetTurn(self):
        return self._turn 

    def UpdateTurn(self):
        self._turn += 1 

    def SpawnShips(self):
        self.DisplayUserGrids()
        for ship in self._ships:
            ship.PlaceShip(self)

    def SpawnRandomShips(self):
        self.DisplayUserGrids()
        for ship in self._ships:
            ship.PlaceRandomShip()

    def ValidCoordinateOnGrid(self,coordinate):
        for row in range(len(self._grids.GetTotalCoordinates())):
            if coordinate in self._grids.GetTotalCoordinates()[row]:
                return True
        return False 

    def DisplayUserGrids(self):
        print(f"{self._name}'s Turn \n")
        print(f"Turn {self._turn}\n")
        self._grids.DisplayGrid()

    def HitGrid(self,player):
        running = True
        while running:
            self.TotalShipStatus(player.GetShips())
            coordinate = input("Enter Coordinates: ").upper() 
            if self.ValidCoordinateOnGrid(coordinate):
                x = self._grids.GetRowIndex()[coordinate[0]]
                y = int(coordinate[1])
                if self._grids.GetPlayerGrid()[x][y].GetSelected() == False:
                    if player.GetGrids().GetShipGrid()[x][y].GetOccupied() == True:
                        self._grids.GetPlayerGrid()[x][y] = Ship(None,None,None)
                        self._grids.GetPlayerGrid()[x][y].SetSelected()                   
                        player.GetGrids().GetShipGrid()[x][y].SetSelected()
                        for ship in range(len(player.GetShips())):
                            if coordinate in player.GetShips()[ship].GetLocation():
                                player.GetShips()[ship].GetLocation().remove(coordinate)
                        os.system("clear")
                        self.DisplayUserGrids()
                        print("\nShip hit! ")
                        running = False
                    else:
                        self._grids.GetPlayerGrid()[x][y].SetSelected()
                        player.GetGrids().GetShipGrid()[x][y].SetSelected()
                        os.system("clear")
                        self.DisplayUserGrids()
                        print("\nYou missed ")
                        running = False 
                    for ship in range(len(player.GetShips())):
                        player.GetShips()[ship].ShipStatus(self)     
                else:
                    os.system("clear")
                    self.DisplayUserGrids()
                    print("You have already selected this coordinate, please try again")
            else:
                os.system("clear")
                self.DisplayUserGrids()
                print("Invalid Coordinates")

    def TotalShipStatus(self,Player_Ships):
        print("\nOpponents ship status:")
        for i in range(len(Player_Ships)):
            if Player_Ships[i].GetShipDestroyed():
                print(f"{Player_Ships[i].GetName()} Destroyed")
            else:
                print(f"{Player_Ships[i].GetName()} Active")
