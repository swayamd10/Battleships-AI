from agents import *
from players import *

class PlayerQueue:
    def __init__(self):
        self.queue = []

    def PlayerEnqueue(self,player):
        self.queue.append(player)

    def PlayerDequeue(self):
        self.queue.pop(0)

class Game:
    def __init__(self):
        self.game_over = False

    def TwoPlayerTurnTransition(self,Player,Opponent):
        running = True
        while running:
            current_turn  = input("Enter Yes or Y to continue: ").upper()
            if current_turn == "YES" or current_turn == "Y":
                os.system("clear")
                print(f"{Opponent.GetName()} look away")
                confirm_turn = input(f"{Player.GetName()} confirm to begin turn? Yes(Y)").upper()
                if confirm_turn == "YES" or confirm_turn == "Y":
                    running = False
                    os.system("clear")

    def Player1Turn(self):
        self.TwoPlayerTurnTransition(self.player1,self.player2)
        self.player1.DisplayUserGrids()
        if self.player1.GetTurn() == 0:
            print("Would you like to place your own ships, or randomly generate them onto the grid?")
            while True:
                try:
                    option = int(input("Enter 1 to place your own, otherwise enter 2 to randomly place them: "))
                except ValueError:
                    print("Invalid input") 
                else:
                    os.system("clear")
                    if option == 1:
                        self.player1.SpawnShips()
                        break 
                    elif option == 2:
                        for ship in self.player1.GetShips():
                            ship.PlaceRandomShip()
                        self.player1.DisplayUserGrids()
                        break 
                    else:
                        print("invalid input")
        else:
            self.player1.HitGrid(self.player2)
        self.player1.UpdateTurn()

    def Player1AITurn(self):
        if self.player1.GetTurn() == 0:
            print("Would you like to place your own ships, or randomly generate them onto the grid?")
            while True:
                try:
                    option = int(input("Enter 1 to place your own, otherwise enter 2 to randomly place them: "))
                except ValueError:
                    print("Invalid input") 
                else:
                    os.system("clear")
                    if option == 1:
                        self.player1.SpawnShips()
                        break 
                    elif option == 2:
                        for ship in self.player1.GetShips():
                            ship.PlaceRandomShip()

                        self.player1.DisplayUserGrids()
                        break 
                    else:
                        print("invalid input")
        else:
            # print("TOTALSHIPS: ",self.player1.GetTotalShips()) for testing 
            self.player1.HitGrid(self.q_learning_agent)
        self.player1.UpdateTurn()

    def Player2Turn(self):
        self.TwoPlayerTurnTransition(self.player2,self.player1)
        self.player2.DisplayUserGrids()
        if self.player2.GetTurn() == 0:
            print("Would you like to place your own ships, or randomly generate them onto the grid?")
            while True:
                try:
                    option = int(input("Enter 1 to place your own, otherwise enter 2 to randomly place them: "))
                except ValueError:
                    print("Invalid input")
                else:
                    os.system("clear")
                    if option == 1:
                        self.player2.SpawnShips()
                        break 
                    elif option == 2:
                        for ship in self.player2.GetShips():
                            ship.PlaceRandomShip()
                        self.player2.DisplayUserGrids()
                        break 
                    else:
                        print("invalid input")
        else:
            self.player2.HitGrid(self.player1)
        self.player2.UpdateTurn()

    def SetUpTwoPlayer(self):
        player1_name = input("Enter Player 1 name: ")
        self.player1 = Player(player1_name)
        player2_name = input("Enter Player 2 name: ")
        self.player2 = Player(player2_name)

    def TwoPlayerGame(self):
        self.SetUpTwoPlayer()
        Player_Turn = PlayerQueue()
        Player_Turn.PlayerEnqueue(self.Player1Turn)
        Player_Turn.PlayerEnqueue(self.Player2Turn)
        while not self.game_over:
            if self.CheckWinner(self.player1,self.player2):
                Player_Turn.queue[0]()
                Player_Turn.PlayerDequeue()
                Player_Turn.PlayerEnqueue(self.Player1Turn)
            else:
                break 
            if self.CheckWinner(self.player1,self.player2):
                Player_Turn.queue[0]()
                Player_Turn.PlayerDequeue()
                Player_Turn.PlayerEnqueue(self.Player2Turn)
            else:
                self.game_over = False

    def Q_Learning_Agent_Turn(self):
        # print(f"Turn {self.q_learning_agent.GetTurn()}")  for testing 
        if self.q_learning_agent.GetTurn() == 0: 
            self.q_learning_agent.SetUpEnvironmentShips()
        else:
            self.q_learning_agent.HitGrid()
        # print("AI TOTAL SHIPS",self.q_learning_agent.GetTotalShips())  for testing 
        self.q_learning_agent.UpdateTurn()

    def QLearningGame(self):
        player1_name = input("Enter Player 1 name: ")
        self.player1 = Player(player1_name)
        self.q_learning_agent = Q_Learning_Agent("Agent",0.7,0.9,0.9,self.player1)
        Player_Turn = PlayerQueue()
        Player_Turn.PlayerEnqueue(self.Player1AITurn)
        Player_Turn.PlayerEnqueue(self.Q_Learning_Agent_Turn)
        while not self.game_over:
            if self.CheckWinner(self.player1,self.q_learning_agent):
                Player_Turn.queue[0]()
                Player_Turn.PlayerDequeue()
                Player_Turn.PlayerEnqueue(self.Player1AITurn)
            else:
                break
            if self.CheckWinner(self.player1,self.q_learning_agent):
                Player_Turn.queue[0]()
                Player_Turn.PlayerDequeue()
                Player_Turn.PlayerEnqueue(self.Q_Learning_Agent_Turn)
            else:
                self.game_over = False  

    def QuitProgram(self):
        print("\nThank you for playing this game")
        quit()

    def Information(self):
        print("""
        Welcome to battleships

upon starting the program, a menu will be displayed for you with options to either play the AI or 2-player game modes. 

AI game mode: When you start the AI game mode the program will ask you to enter your name and place your ships. Once you have placed your ships down the game can begin, you will have to enter coordinates and attack the opponent’s ships. 

2-player game mode: When you start the 2-player game mode the program will ask both players to enter their names. In between both player’s turns, a screen will confirm the player to shift the turns. 

To place ships you have to enter start and end location coordinates for the ship of appropriate size. For example, the start location of “A0” and the end location of “A3” would be valid because the ship would occupy locations of [“A0”,”A1”,”A2”,”A3”]

The syntax for entering coordinates is a letter then a number, so the first character is a letter between A - and J and the second character will be a number between 0 and 9 

The game will end when either player's ships have been destroyed


        """)
        self.GameMenu()

    def ErrorMessage(self):
        print("Invalid input, try again")

    def CheckWinner(self,player1,player2):
        if player1.GetTotalShips() == 0:
            print(f"{player1.GetName()} is the winner")
            return False
        elif player2.GetTotalShips() == 0:
            print(f"{player2.GetName()} is the winner")
            return False
        return True

    def DisplayMenu(self):
          print("""
Welcome to 2 Player Battleships

Pick an option to proceed the program

1. AI game
2. Two player game
3. Information
4. Quit""")

    def GameMenu(self):
        choice = ""
        while choice != 4:
            self.DisplayMenu()
            try:
                choice = int(input("Enter Choice: "))
            except ValueError:
                os.system("clear")
                self.ErrorMessage()
            else:
                if choice == 1:
                    self.QLearningGame()
                elif choice == 2:
                    self.TwoPlayerGame()
                elif choice == 3:
                    self.Information()
                elif choice == 4:
                    self.QuitProgram()
                else:
                    os.system("clear")
                    self.ErrorMessage()
