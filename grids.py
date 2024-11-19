class Cell:
    def __init__(self,value,grid):
        self.__cell = "_"
        self.__value = value
        self.__grid = grid
        self.__next_value = self.Generate()
        self.__occupied = False
        self.__selected = False
        self.__hit = "X"
        self.__miss = "O"
        self.__reward =  -1

    def __repr__(self):
        if self.__selected:
            return self.__miss
        return self.__cell

    def GetReward(self):
        return self.__reward

    def GetOccupied(self):
        return self.__occupied

    def GetSelected(self):
        return self.__selected

    def SetSelected(self):
        self.__selected = True

    def GetValue(self):
        return self.__value

    def GetNextValue(self):
        return self.__next_value

    def CellFound(self,value):
        total_coordinates = self.__grid.GetTotalCoordinates()
        for i in range(len(total_coordinates)):
            for j in range(len(total_coordinates)):
                if total_coordinates[i][j] == value:
                    return True
        return False

    def Generate(self):
        values = []
        next_values = []
        key = self.__grid.GetKey()
        index = (key).index(self.__value[0])
        try:
            left = self.__value[0] + str(int(self.__value[1]) - 1)
            if self.CellFound(left):
                next_values.append(left)
            else:
                next_values.append(" ")
            right = self.__value[0] + str(int(self.__value[1]) + 1)
            if self.CellFound(right):
                next_values.append(right)
            else:
                next_values.append(" ")
            if index - 1 >= 0:
                up = key[index - 1] + self.__value[1]
                if self.CellFound(up):
                    next_values.append(up)
            else:
                next_values.append(" ")
            down = key[index + 1] + self.__value[1]
            if self.CellFound(down):
                next_values.append(down)

        except IndexError:
            next_values.append(" ")
        return next_values

    def CellValid(self,ships):
        for ship in ships:
            x_coord = self.__grid.GetKey().index(ship[0])
            y_coord = int(ship[1])
            if self.__grid.GetShipGrid()[x_coord][y_coord].GetOccupied() == True:
                return False
        return True

class Grid:
    def __init__(self):
        self.__GRID_SIZE = 10
        self.__row_index = {"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G":6,"H":7,"I":8,"J":9}
        self.__key = list(self.__row_index.keys())
        self.__value = list(self.__row_index.values())
        self.__total_coordinates = self.GenerateTotalCoordinates()
        self.__player_grid = [[Cell(self.__total_coordinates[j][i],self) for i in range(self.__GRID_SIZE)] for j in range(self.__GRID_SIZE)]
        self.__ship_grid = [[Cell(self.__total_coordinates[j][i],self) for i in range(self.__GRID_SIZE)] for j in range(self.__GRID_SIZE)]
        self.__graph = self.GenerateGraph()

    def GetKey(self):
        return self.__key

    def GetRowIndex(self):
        return self.__row_index

    def GetPlayerGrid(self):
        return self.__player_grid

    def GetShipGrid(self):
        return self.__ship_grid

    def GetTotalCoordinates(self):
        return self.__total_coordinates

    def GetGraph(self):
        return self.__graph

    def GenerateTotalCoordinates(self):
        total_coordinates = []
        for i in range(len(self.__key)):
            coordinates = []
            for j in range(len(self.__value)):
                coordinates.append(self.__key[i] + str(self.__value[j]))
            total_coordinates.append(coordinates)
        return total_coordinates

    def DisplayGrid(self):
        print("Attack grid",end = " ")
        print("                      ",end = " ")
        print("Ship grid\n")
        # print()
        print("\x1B[4m" + "X| 0 1 2 3 4 5 6 7 8 9" + "\x1B[0m",end = " ")
        print("           ",end = " ")
        print("\x1B[4m" + "X| 0 1 2 3 4 5 6 7 8 9" + "\x1B[0m")
        for row in range(self.__GRID_SIZE):
            print(self.__key[row] + "|"," ".join(str(cell) for cell in self.__player_grid[row]),end = " ")
            print("           ",end = " ")
            print(self.__key[row] + "|"," ".join(str(cell) for cell in self.__ship_grid[row]))
        print()



















    
    def GenerateGraph(self):
        graph = {}
        for i in range(len(self.__player_grid)):
            for j in range(len(self.__player_grid)):
                graph.update({self.__player_grid[i][j].GetValue():self.__player_grid[i][j].GetNextValue()})
        return graph
