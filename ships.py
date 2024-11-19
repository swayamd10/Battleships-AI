import os
import random

class Ship:
    def __init__(self,ship_grid,name,size):
        self._name = name 
        self._size = size
        self.ship_grid = ship_grid
        self._ship_destroyed = False
        self._location = []
        self._occupied = True
        self._hit = "X"
        self._selected = False
        self._orientation = ["Horizontal","Vertical"]
        self._ships_placed = False
        self._value = None
        self._cell_destroyed = False
        self._reward = 1

    def GetName(self):
        return self._name

    def GetSize(self):
        return self._size

    def GetReward(self):
        return self._reward

    def GetOccupied(self):
        return self._occupied

    def SetCellDestroyed(self):
        self._cell_destroyed = True

    def GetCellDestroyed(self):
        return self._cell_destroyed

    def GetLocation(self):
        return self._location

    def SetLocation(self,location):
        self._location = location

    def GetShipDestroyed(self):
        return self._ship_destroyed

    def SetShipDestroyed(self):
        self._ship_destroyed = True

    def SetSelected(self):
        self._selected = True

    def GetSelected(self):
        return self._selected

    def SetValue(self,value):
        self._value = value

    def GetValue(self):
        return self._value

    def __repr__(self):
        if self._selected:
            return self._hit

    def ValidPlacement(self):
        running = True
        while running:
            confirm_ship = input(f"Are you happy with the placement of the {self.GetName()}? Yes(Y) or No(N): ").upper()
            if confirm_ship == "Y" or confirm_ship == "YES":
                return True
            elif confirm_ship == "N" or confirm_ship == "NO":
                return False
            else:
                print("Invalid input try again")

    def ShipStatus(self,Player):
        if len(self._location) == 0 and self._ship_destroyed == False:
            self._ship_destroyed = True
            Player.DecreaseShip() 

    def ShipOccupied(self,ship_cells):
        for ship in ship_cells:
            x = self.ship_grid.GetRowIndex()[ship[0]]
            y = int(ship[1])
            if self.ship_grid.GetShipGrid()[x][y].GetOccupied() == True:
                print("Cell occupied, try again")
                return False
        return True

    def CreateShips(self):
        running = True 
        row_index = self.ship_grid.GetRowIndex()
        while running:
            try:
                print(f"\nPlace {self._name}") 
                print(f"{self._name} size is {self._size}")
                start_location = input("Enter start location: ").upper()
                end_location = input("Enter end location: ").upper()
                index = self.ship_grid.GetKey().index(start_location[0])
                if len(start_location) == 2 and  len(end_location) == 2:
                    if start_location[1] == end_location[1]:
                        if row_index[end_location[0]] - row_index[start_location[0]] == self._size - 1:
                            ship_cells = [self.ship_grid.GetKey()[index + i] + start_location[1] for i in range(self._size)] 
                            print(f"This is the location of the ship: {ship_cells}")
                            if self.ValidPlacement():
                                if self.ShipOccupied(ship_cells):
                                    for ship in ship_cells:
                                        x = row_index[ship[0]]
                                        y = int(ship[1])
                                        self.ship_grid.GetShipGrid()[x][y] = self.GetInstance()
                                    running = False
                                    self.SetLocation(ship_cells)
                        elif row_index[start_location[0]] - row_index[end_location[0]] == self._size - 1:
                            ship_cells = [self.ship_grid.GetKey()[index - i] + start_location[1] for i in range(self._size)]
                            print(f"This is the location of the ship: {ship_cells}")
                            if self.ValidPlacement():
                                if self.ShipOccupied(ship_cells):
                                    for ship in ship_cells:
                                        x = row_index[ship[0]]
                                        y = int(ship[1])
                                        self.ship_grid.GetShipGrid()[x][y] = self.GetInstance()
                                    running = False
                                    self.SetLocation(ship_cells)
                    elif start_location[0] == end_location[0]:
                        if int(end_location[1]) - int(start_location[1]) == self._size - 1:
                            ship_cells = [start_location[0] + str(int(start_location[1]) + i) for i in range(self._size)]
                            print(f"This is the location of the ship: {ship_cells}")
                            if self.ValidPlacement():
                                if self.ShipOccupied(ship_cells):
                                    for ship in ship_cells:
                                        x = row_index[ship[0]]
                                        y = int(ship[1])
                                        self.ship_grid.GetShipGrid()[x][y] = self.GetInstance()
                                    running = False
                                    self.SetLocation(ship_cells)
                        elif int(start_location[1]) - int(end_location[1]) == self._size - 1:
                            ship_cells = [start_location[0] + str(int(start_location[1]) - i) for i in range(self._size)]
                            print(f"This is the location of the ship: {ship_cells}")
                            if self.ValidPlacement():
                                if self.ShipOccupied(ship_cells):
                                    for ship in ship_cells:
                                        x = row_index[ship[0]]
                                        y = int(ship[1])
                                        self.ship_grid.GetShipGrid()[x][y] = self.GetInstance()
                                    running = False
                                    self.SetLocation(ship_cells)
                        else:
                            print("Invalid location, try again")
                    else:
                        print("Invalid location, try again")     
                else:
                    print("Not greater than 2, try again") 
            except (ValueError,KeyError,IndexError):
                print("Invalid input, try again") 

    def PlacingRandomShip(self):
        row_index = self.ship_grid.GetRowIndex()
        for ship in self.GetLocation():
            x =  row_index[ship[0]]
            y = int(ship[1])
            value = self.ship_grid.GetShipGrid()[x][y].GetValue()
            self.ship_grid.GetShipGrid()[x][y] = self.GetInstance()
            self.ship_grid.GetShipGrid()[x][y].SetValue(value)

    def PlaceRandomShip(self):
        running = True
        while running:
            x_coord = random.randint(0,9)
            y_coord = random.randint(0,9)
            key = self.ship_grid.GetKey()
            orientation = random.choice(self._orientation)
            if orientation == "Horizontal":
                location1 = [key[x_coord] + str(y_coord + count) for count in range(self.GetSize())]
                location2 = [key[x_coord] + str(y_coord - count) for count in range(self.GetSize())]
                if self.CheckValidShip(location1):
                    self.SetLocation(location1)
                    if self.ship_grid.GetPlayerGrid()[x_coord][y_coord].CellValid(self.GetLocation()):
                        self.PlacingRandomShip()
                        self._ships_placed = True
                        running = False
                elif self.CheckValidShip(location2):
                    self.SetLocation(location2)
                    if self.ship_grid.GetPlayerGrid()[x_coord][y_coord].CellValid(self.GetLocation()):
                        self.PlacingRandomShip()
                        self._ships_placed = True
                        running = False
            else:
                try:
                    location1 = [key[x_coord + count] + str(y_coord) for count in range(self.GetSize())]
                    location2 = [key[x_coord - count] + str(y_coord) for count in range(self.GetSize())]
                    if self.CheckValidShip(location1):
                        self.SetLocation(location1)
                        if self.ship_grid.GetPlayerGrid()[x_coord][y_coord].CellValid(self.GetLocation()):
                            self.PlacingRandomShip()
                            self._ships_placed = True
                            running = False
                    elif self.CheckValidShip(location2):
                        self.SetLocation(location2)
                        if self.ship_grid.GetPlayerGrid()[x_coord][y_coord].CellValid(self.GetLocation()):
                            self.PlacingRandomShip()
                            self._ships_placed = True
                            running = False
                except IndexError:
                    pass

    def CheckValidShip(self,coordinates):
        count = 0
        total_coordinates = self.ship_grid.GetTotalCoordinates()
        for coordinate in coordinates:
            for value in range(len(total_coordinates)):
                if coordinate in total_coordinates[value]:
                    count += 1
        if count == len(coordinates):
            return True
        return False

    def PlaceShip(self,player):
        self.CreateShips()
        os.system("clear")
        player.GetGrids().DisplayGrid()
        print(f"This is the {self._name} location: {self._location}")

class Battleship(Ship):
    def __init__(self,ship_grid):
        super().__init__(ship_grid,name = "Battleship",size = 4)
        self.__battleship = "B"

    def GetInstance(self):
        return Battleship(None)

    def __repr__(self):
        if self._selected:
            return self._hit
        return self.__battleship

class Cruiser(Ship):
    def __init__(self,ship_grid):
        super().__init__(ship_grid, name = "Cruiser", size = 3)
        self.__cruiser = "c"

    def GetInstance(self):
        return Cruiser(None)

    def __repr__(self):
        if self._selected:
            return self._hit
        return self.__cruiser

class Carrier(Ship):
    def __init__(self,ship_grid):
        super().__init__(ship_grid,name = "Carrier",size = 5)
        self.__carrier = "C"

    def GetInstance(self):
        return Carrier(None)

    def __repr__(self):
        if self._selected:
            return self._hit
        return self.__carrier

class Submarine(Ship):
    def __init__(self,ship_grid):
        super().__init__(ship_grid,name = "Submarine",size = 3)
        self.__submarine = "S"

    def GetInstance(self):
        return Submarine(None)

    def __repr__(self):
        if self._selected:
            return self._hit
        return self.__submarine

class Destroyer(Ship):
    def __init__(self,ship_grid):
        super().__init__(ship_grid, name = "Destroyer", size = 2)
        self.__destroyer = "D"

    def GetInstance(self):
        return Destroyer(None)

    def __repr__(self):
        if self._selected:
            return self._hit
        return self.__destroyer
