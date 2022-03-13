#Craig Methven
#Version 1.5
#21/02/2018

#Import pygame
import pygame, sys

def TheGame():
    #Read in variables from document
    RX,RY,GX,GY,NP,savedColour = readOptionsDoc()
    #Variables
    resolution = []
    resolution.append(int(RX))
    resolution.append(int(RY))
    gridSize = []
    gridSize.append(int(GX))
    gridSize.append(int(GY))
    teams = int(NP)
    teamGoing = 0
    fillGrid = [    ]
    winner = False
    Queue = 0
    EdgeXStart = 0
    EdgeYStart = 0
    EdgeXEnd = 0
    EdgeYStart = 0
    turn = 0
    Queue = []
    teamColour = []
    teamColour.append([255,255,255])
    for counter in range(8):
        teamColour.append(savedColour[counter])
    stop = []
    stop = False
    spacesOwned = []

    #Sizes
    #Swap the resolutions so that the X length is the wider one
    def makingTheResolutionXSideTheLargerOne(resolution):
        if resolution[0] < resolution[1]:
            temp = resolution[0]
            resolution[0] = resolution[1]
            resolution[1] = temp
        return resolution

    #Swap the grid size so that the X length is the wider one
    def makingTheXSideTheLargerOne(gridSize):
        if gridSize[0] < gridSize[1]:
            temp = gridSize[0]
            gridSize[0] = gridSize[1]
            gridSize[1] = temp
        return gridSize

    #Find the size the squares should be
    def FindBoxHW(resolution,gridSize):
        #Width of Box
        BoxW = (resolution[0] / gridSize[0])
        #Height of Box
        BoxH = (resolution[1] / gridSize[1])
        #Box Size
        BoxHW = BoxW
        if BoxW > BoxH:
            BoxHW = BoxH

        return BoxHW

    #Define the grid which the counters will be placed on
    def Create2DArray(gridSize):
        i = 0
        counter = 0
        TempX = gridSize[0]
        TempY = gridSize[1]

    #Define the grid
        grid = []
        grid = [[0 for y in range(TempY)] for x in range(TempX)]

    #Fill grid w/ nothing in the teams slot and 0 in the counters slot
    #grid[x][y] = [colour],[counter]
        for i in range(TempX):
            for counter in range(TempY):
                grid[i][counter] = [0,0]

        return grid

    #Find how far in the grid should be on the screen so that it is centered and where the grid ends
    def StartPoints(resolution,BoxHW):
        #See's if it needs to move on the X or Y axis
        XOverflow = resolution[0] / gridSize[0]
        YOverflow = resolution[1] / gridSize[1]

        #If the resolution is a square just use the whole screen for the grid
        if XOverflow == YOverflow:
            EdgeXStart = 0
            EdgeXEnd = resolution[0]
            EdgeYStart = 0
            EdgeYEnd = resolution[1]
        else:
            EdgeXStart = (resolution[0] - (gridSize[0] * BoxHW))/2
            EdgeXEnd = (gridSize[0] * BoxHW) +EdgeXStart
            EdgeYStart = (resolution[1] - (gridSize[1] * BoxHW))/2
            EdgeYEnd = (gridSize[1] * BoxHW) +EdgeYStart


        return EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd

    #Draws the grid that the user inputs into onto the screen
    def DrawGrid(BoxHW,EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd,Display,teamColour,teamGoing,gridSize,teams):
        teamGoing = teamChecker(teamGoing, teams, grid, gridSize, turn)
        for counter in range (gridSize[0]+1):
            #Draw horizontal lines
            pygame.draw.line(Display, teamColour[teamGoing], [BoxHW * (counter)+ EdgeXStart, EdgeYStart], [BoxHW * (counter)+ EdgeXStart, EdgeYEnd], 5)
        for counter in range(gridSize[1]+1):
            #Draw verticle lines
            pygame.draw.line(Display, teamColour[teamGoing], [EdgeXStart, BoxHW *(counter)+ EdgeYStart], [EdgeXEnd, BoxHW * (counter)+ EdgeYStart], 5)
        pygame.display.update()
        return Display

    #Draw on the counter in the grid square that has been clicked on
    def DrawCircles(number,workingOn,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,teamColour,turn):
        pygame.time.delay(60)
        #Remove previous counters in that box
        pygame.draw.rect(Display,(0,0,0),(((workingOn[0]) * BoxHW)+EdgeXStart+5, (workingOn[1] * BoxHW)+EdgeYStart+5,BoxHW-10,BoxHW-10))
        if number == 1:
        #If one counter in the square draw one circle
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart)), int(BoxHW *(2/9)))
        if number == 2:
        #If two counter in the square draw two circle
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart-BoxHW *(1/7))), int(BoxHW *(2/9)))
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart+BoxHW *(1/7))), int(BoxHW *(2/9)))
        if number == 3:
        #If three counter in the square draw three circle
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart-BoxHW *(1/7)), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart-BoxHW *(1/7))), int(BoxHW *(2/9)))
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart+BoxHW *(1/7)), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart-BoxHW *(1/7))), int(BoxHW *(2/9)))
            pygame.draw.circle(Display, teamColour[teamGoing], (int(((workingOn[0]+0.5) * BoxHW)+EdgeXStart), int(((workingOn[1]+0.5) * BoxHW)+EdgeYStart+BoxHW *(1/7))), int(BoxHW *(2/9)))
        pygame.display.update()

    #If space has been popped remove the counters from the visual grid and the 2D array storing the counters
    def popper(grid,workingOn):
        grid[workingOn[0]][workingOn[1]][0] = 0
        grid[workingOn[0]][workingOn[1]][1] = 0
        pygame.draw.rect(Display,(0,0,0),(((workingOn[0]) * BoxHW)+EdgeXStart+5, (workingOn[1] * BoxHW)+EdgeYStart+5,BoxHW-10,BoxHW-10))

    #Change the team after a turn ends
    def ChangeTeam(teamGoing):
        teamGoing += 1
        #Set the team going back to the first team if over the total number of teams
        if teamGoing > teams:
            teamGoing = 1
        return(teamGoing)

    #Check to see if the team is still in the game and if not go to the next one
    def teamChecker(teamGoing, teams, grid, gridSize, turn):
        there = ()
        #Set the team going back to the first team if over the total number of teams
        if teamGoing > teams:
            teamGoing = 1
        #Check to see if teams alive
        if teams < turn:
            there = False
            for counter in range (gridSize[0]):
                for index in range (gridSize[1]):
                    if teamGoing == grid[counter][index][0]:
                        there = True

        #If team is not alive go to the next team until one is found that can go (using recursion)
        if there == False:
            teamGoing = teamChecker(teamGoing+1, teams, grid, gridSize, turn)
        return(teamGoing)

    #Take the input the user makes and see if that is a valid move for that player
    def InputPos(BoxHW,EdgeXStart,EdgeYStart,grid,teamGoing,gridSize):
        pos = [None,None]
        Loop = True
        while Loop == True:

            #Look for mouse click and save mouse position to temp
            for event in pygame.event.get():
                                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos[0],pos[1] = event.pos
                
                    #Get the x and y cords on the grid
                    xCord = (pos[0]-EdgeXStart) / BoxHW
                    yCord = (pos[1]-EdgeYStart) / BoxHW

                    #Check to see if player has clicked on the grid
                    if xCord < 0 or yCord < 0 or xCord > int(gridSize[0]) or yCord > int(gridSize[1]):
                        print("Please click on the grid")
                    else:
                    #Check to see if user owns the square
                        whatTeam = grid[int(xCord)][int(yCord)][0]
                        if whatTeam == teamGoing or whatTeam == 0:
                            addToQueue = [int(xCord), int(yCord)]
                            Loop = False
                        else:
                            pos[0] = None
                            pos[1] = None

                #Quit Button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
             
        return(addToQueue)

    def QueueAdding(addToQueue,Queue):
    #Add the x and y cord to the queue
        Queue.append(addToQueue)
        return(Queue)
        
    #Start of the visuals and processing inputs
    def ChangeGrid(Queue,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,grid,teamColour,turn,stop):
        pop = []
        temp = []
        addToQueue = []
        addingNumbers = []
    #Check to see if grind is not empty and if so take a input from it into the variable workingOn
        while Queue != 0 or Queue != []:
            workingOn = []
            workingOn = Queue.pop()

    #Set the team going and add one to the square that the variable is in
            grid[workingOn[0]][workingOn[1]][0] = int(teamGoing)
            grid[workingOn[0]][workingOn[1]][1] += 1

    #Drawing Circles corresponging to the square clicked
            if grid[workingOn[0]][workingOn[1]][1] == 1:
                DrawCircles(1,workingOn,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,teamColour,turn)
            if grid[workingOn[0]][workingOn[1]][1] == 2:
                DrawCircles(2,workingOn,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,teamColour,turn)
            if grid[workingOn[0]][workingOn[1]][1] >= 3:
                DrawCircles(3,workingOn,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,teamColour,turn)

    #If infinite loop hasn't been created within the game
            if stop == False:
                
    #Popping mechanic for any where on the board
    #If the counter is 4 or over 4, in the square working on, then add the surrounding squares to the queue
                if grid[workingOn[0]][workingOn[1]][1] >= 4:
                    surroundingSquares = [[workingOn[0]-1, workingOn[1]],[workingOn[0]+1, workingOn[1]],[workingOn[0], workingOn[1]-1],[workingOn[0], workingOn[1]+1]]
                    pop = True
                    for counter in range(4):
                        Queue.append(surroundingSquares.pop())

    #Popping mechanic for the edges of the board
    #If the counter is 3 or over 3, in the square working on, and on a edge then add the surrounding squares to the queue
                if workingOn[0] == 0 and grid[workingOn[0]][workingOn[1]][1] == 3:
                    surroundingSquares = [[workingOn[0]+1, workingOn[1]],[workingOn[0],workingOn[1]+1],[workingOn[0],workingOn[1]-1]]
                    pop = True
                    for counter in range(3):
                        Queue.append(surroundingSquares.pop())
                if workingOn[1] == 0 and grid[workingOn[0]][workingOn[1]][1] == 3:
                    surroundingSquares = [[workingOn[0]+1, workingOn[1]],[workingOn[0]-1,workingOn[1]],[workingOn[0],workingOn[1]+1]]
                    pop = True
                    for counter in range(3):
                        Queue.append(surroundingSquares.pop())
                if workingOn[0] == gridSize[0]-1 and grid[workingOn[0]][workingOn[1]][1] == 3:
                    surroundingSquares = [[workingOn[0]-1, workingOn[1]],[workingOn[0],workingOn[1]+1],[workingOn[0],workingOn[1]-1]]
                    pop = True
                    for counter in range(3):
                        Queue.append(surroundingSquares.pop())
                if workingOn[1] == gridSize[1]-1 and grid[workingOn[0]][workingOn[1]][1] == 3:
                    surroundingSquares = [[workingOn[0]-1, workingOn[1]],[workingOn[0]+1,workingOn[1]],[workingOn[0],workingOn[1]-1]]
                    pop = True
                    for counter in range(3):
                        Queue.append(surroundingSquares.pop())

    #Popping mechanic for the corners
    #If the counter is 2 or over 2, in the square working on, and on a corner then add the surrounding squares to the queue
                if workingOn[0] == 0 and workingOn[1] == 0 and grid[workingOn[0]][workingOn[1]][1] == 2:
                    surroundingSquares = [[workingOn[0]+1, workingOn[1]],[workingOn[0],workingOn[1]+1]]
                    pop = True
                    for counter in range(2):
                        Queue.append(surroundingSquares.pop())
                if workingOn[0] == 0 and workingOn[1] == gridSize[1]-1 and grid[workingOn[0]][workingOn[1]][1] == 2:
                    surroundingSquares = [[workingOn[0]+1,workingOn[1]],[workingOn[0],workingOn[1]-1]]
                    pop = True
                    for counter in range(2):
                        Queue.append(surroundingSquares.pop())
                if workingOn[0] == gridSize[0]-1 and workingOn[1] == 0 and grid[workingOn[0]][workingOn[1]][1] == 2:
                    surroundingSquares = [[workingOn[0]-1,workingOn[1]],[workingOn[0],workingOn[1]+1]]
                    pop = True
                    for counter in range(2):
                        Queue.append(surroundingSquares.pop())
                if workingOn[0] == gridSize[0]-1 and workingOn[1] == gridSize[1]-1 and grid[workingOn[0]][workingOn[1]][1] == 2:
                    surroundingSquares = [[workingOn[0]-1,workingOn[1]],[workingOn[0],workingOn[1]-1]]
                    pop = True
                    for counter in range(2):
                        Queue.append(surroundingSquares.pop())

    #If pop has been found to need to occur do it
            if pop == True:
                grid = popper(grid,workingOn)
            workingOn = []
            return addToQueue

        return None

    #Check to see if someone has won
    def Winner(grid,gridSize,turn,teams,teamGoing):
        lose = []
        winner = False
    #If every player has taken their turn check to see if there is more the team that has just gone on the board
        if turn > teams:
            #Runs for every team
            for i in range (teams):
                #Sets by default that they have lost the game
                lose.append(True)
                #if a counter of that team is found on the board set it so that they haven't lost
                for counter in range (gridSize[0]):
                    for index in range (gridSize[1]):
                        if grid[counter][index][0] == i+1:
                            lose[i] = False

            i = 0
            counter = 0
            #If more than one team hasn't lost they keep winner as false. If only one team is still on set winner to true.
            for i in range(teams):
                if lose[i] == False:
                    counter += 1
            if counter == 1:
                winner = True
                
        return(winner)

    #Calculate the number of counter the winner owns at the end of the game
    def OwnedCounters(gridSize,grid):
        TotalOwned = 0
        spacesOwned = 0
    #Go through every square and add the number of counters in that grid to the running total
        for i in range(gridSize[0]):
            for counter in range(gridSize[1]):
                TotalOwned = TotalOwned + grid[i][counter][1]
                if grid[i][counter][1] != [] and grid[i][counter][1] != 0:
                    spacesOwned += 1

        return TotalOwned,spacesOwned

    #Tells the user who won and collects the winners name
    def winnerInput(teamColour, teamGoing):

        #Initialise pygame fonts and define the screen size and font
        WinScreen = pygame.display.set_mode((500,300))
        pygame.display.set_caption("boop 'em")
        icon= pygame.image.load("icon.png")
        pygame.display.set_icon(icon)
        pygame.font.init()
        myfont = pygame.font.SysFont('tektonproboldext', 70)

        #Compile the message that will say who wins in the colour of who has won
        TextColour= teamColour[teamGoing]
        winningText = "Team " + str(teamGoing) + " Wins"

        #render the winners text and the title image
        titleImage = pygame.image.load('title50W.bmp')
        winnerDisplay = myfont.render(winningText, 0, TextColour, (0,0,0))
        WinScreen.blit(titleImage,(0,0))
        WinScreen.blit(winnerDisplay,(0,25))

        #Define variables including the colours of the input box when it is active or inactive and the rectangle that makes up the input box
        inactiveColour = (25,25,25)
        activeColour = (75,75,75)
        active = False
        done = False
        size = (10,125,470,130)
        input_box = pygame.draw.rect(WinScreen, inactiveColour, size)
        input_box = pygame.Rect(input_box)

        #Change font for the inputted text
        myfont = pygame.font.SysFont('tektonproboldext', 125)
        InputName = ''

        #Loops until the name has been inputted
        while not done:
            #Checks to see if the user has clicked on the box 
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #If they have clicked on the box make the colour of the box the active colour and set active to true
                    if input_box.collidepoint(event.pos):
                        active = True
                        pygame.draw.rect(WinScreen, activeColour, size)
                    else:
                    #If they have clicked off the box make the colour of the box the inactive colour and set active to false
                        active = False
                        pygame.draw.rect(WinScreen, inactiveColour, size)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                #Collects the input   
                if event.type == pygame.KEYDOWN:
                    #Makes sure the length is less than 5
                    if len(InputName) < 6:
                        if active == True:
                            #If the user presses enter make sure that their name is atleast 3 characters long and then returns the value to the main program
                            if event.key == pygame.K_RETURN:
                                if len(InputName) > 1:
                                    return(InputName)
                            #If backspace has been pressed remove a character from the inputted text
                            elif event.key == pygame.K_BACKSPACE:
                                InputName = InputName[:-1]
                            else:
                            #Add the character pressed to the inputted text
                                if len(InputName) < 5:
                                    InputName += event.unicode

                        #Render the inputted text so the user knows what they have inputted      
                        Initials = myfont.render(InputName, 0, TextColour, activeColour)
                        pygame.draw.rect(WinScreen, activeColour, size)
                        WinScreen.blit(Initials,(10,125))
                            
            pygame.display.update()

    #Saving the score and name to the scores file
    def SaveToFile(winningName,spacesOwned):
        #Check to see if the file already exists and if not create it
        try:
            scoreFile = open ("scores.txt", "a")
        except FileNotFoundError:
            scoreFile = open ("scores.txt", "x")
            scoreFile.close()

        #Write the score and name to the end of the file
        scoreFile = open ("scores.txt", "a")
        scoreFile.write(str(winningName) + "," +str(spacesOwned) + "\n")
        scoreFile.close()

    
    #Start running the sub routines
    #Make it so the game is larger horizontally than vertically
    pygame.event.clear()
    resolution = makingTheResolutionXSideTheLargerOne(resolution)
    gridSize = makingTheXSideTheLargerOne(gridSize)

    #Create the pygame screen
    Display = pygame.display.set_mode((resolution[0],resolution[1]))
    pygame.display.set_caption("boop 'em")
    icon= pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    #Get the hight and width of the boxes drawm
    BoxHW = FindBoxHW(resolution,gridSize)
    #Creaing the 2D array saving the information about each square
    grid = Create2DArray(gridSize)
    #Find how far in from each edge the grid needs to be places
    EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd = StartPoints(resolution,BoxHW)
    #Draw the grid so the player can see it
    DrawGrid(BoxHW,EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd,Display,teamColour,teamGoing,gridSize,teams)
    winner
    #Start of the game loop that runs until the game ends
    while winner == False:
        if Queue == 0 or Queue == []:
            counter = 0
            turn += 1
            #Draw the grid so the player can see it
            DrawGrid(BoxHW,EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd,Display,teamColour,teamGoing+1,gridSize,teams)
            #Go to the next player
            teamGoing = ChangeTeam(teamGoing)
            #Check to see if the player going is still in the game and if not move onto the next one
            teamGoing = teamChecker(teamGoing, teams, grid, gridSize, turn)
            #Get the square the user clicked on
            addToQueue = InputPos(BoxHW,EdgeXStart,EdgeYStart,grid,teamGoing,gridSize)
            #Add the square clicked on onto the queue
            Queue = QueueAdding(addToQueue,Queue)
            #Make the counters pop if appropriate
            addToQueue= ChangeGrid(Queue,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,grid,teamColour,turn,stop)
            turnsTaken = 0
        while Queue != [] or addToQueue != []:
            turnsTaken += 1
            #If more pops need to be made make them
            addToQueue= ChangeGrid(Queue,teamGoing,EdgeXStart,EdgeYStart,BoxHW,Display,grid,teamColour,turn,stop)
            #If game has run into a infinite loop stop it from running
            if turnsTaken > gridSize[0] * gridSize[1]*10 or turnsTaken == 500:
               stop = True

        #Check to see if a winner has been found at the end of each round
        winner = Winner(grid,gridSize,turn,teams,teamGoing)

    #Draw the finishing grid and find the items to be saved to the scores file
    DrawGrid(BoxHW,EdgeXStart,EdgeYStart,EdgeXEnd,EdgeYEnd,Display,teamColour,teamGoing,gridSize,teams)
    TotalOwned,spacesOwned = OwnedCounters(gridSize,grid)
    winningName = winnerInput(teamColour, teamGoing)
    #Save the name and the score to the score file
    SaveToFile(winningName,spacesOwned)

def MainMenu():
    #Set up the pygame screen
    Main = pygame.display.set_mode((700,750))
    pygame.display.set_caption("boop 'em")
    icon= pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    #Set up pygame font
    pygame.font.init()
    myfont = pygame.font.SysFont('tektonproboldext', 70)
    TextColour = (0,255,0)

    #Collect the text and images wanted
    titleImage = pygame.image.load('title500W.bmp')
    playGameText = myfont.render("Play Game", 0, TextColour, (0,0,0))
    optionsMenuText = myfont.render("Options Menu", 0, TextColour, (0,0,0))
    instructionsText = myfont.render("How to Play", 0, TextColour, (0,0,0))
    scoresText = myfont.render("Scores", 0, TextColour, (0,0,0))
    Main.blit(titleImage,(100,10))

    #Create the buttons
    playBox = pygame.draw.rect(Main, (0,0,0), (0,290,700,90))
    playBox = pygame.Rect(playBox)
    Main.blit(playGameText,(10,300))
    optionsBox = pygame.draw.rect(Main, (0,0,0), (0,410,700,90))
    optionsBox = pygame.Rect(optionsBox)
    Main.blit(optionsMenuText,(10,420))
    instructionsBox = pygame.draw.rect(Main, (0,0,0), (0,530,700,90))
    instructionsBox = pygame.Rect(instructionsBox)
    Main.blit(instructionsText,(10,540))
    scoresBox = pygame.draw.rect(Main, (0,0,0), (0,650,700,90))
    scoresBox = pygame.Rect(scoresBox)
    Main.blit(scoresText,(10,660))
    pygame.display.update()

    #Check to see what the user clicked on and send that back to the run the required code
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playBox.collidepoint(event.pos):
                    return("PlayGame")
                if optionsBox.collidepoint(event.pos):
                    return("options")
                if instructionsBox.collidepoint(event.pos):
                    return("instructions")
                if scoresBox.collidepoint(event.pos):
                    return("scores")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#The options menu
def Options():

    #Collects the input given once a place to input has been selected
    def collectInput(workingOn,limit):
        #Set workingOn to 0 if it doesn't contain a value
        if workingOn == None or workingOn == "":
            workingOn = 0
        #If enter is pressed and it is a value that is allowed return the value
        if int(workingOn) <= limit:
            if event.key == pygame.K_RETURN:
                if int(workingOn) <= limit:
                    return(workingOn)
            #if backspace is pressed remove the last character of workingOn
            elif event.key == pygame.K_BACKSPACE and len(str(workingOn))!= 0:
                workingOn = str(workingOn)[:-1]
                return(workingOn)
            #Save to workingOn the number that the user inputted
            elif event.key == pygame.K_0 or event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 or event.key == pygame.K_4 or event.key == pygame.K_5 or event.key == pygame.K_6 or event.key == pygame.K_7 or event.key == pygame.K_8 or event.key == pygame.K_9:
                if workingOn == 0:
                    workingOn = ""
                workingOn = str(workingOn)
                workingOn += str(event.unicode)
                if int(workingOn) > limit:
                    workingOn = limit
                return(workingOn)
            
    #Sub routine to write to the appropriate place with the text inputted
    def writing(txtInput,Size,colour):
        if txtInput == None or txtInput == 0:
            txtInput = ""
        textIn = myfont.render(str(txtInput), 0, (0,255,0), colour)
        pygame.draw.rect(optionsScreen, colour, Size)
        optionsScreen.blit(textIn,Size)
        
    savedColour = []
    #Read in the options file so it knows what was previously entered
    RX,RY,GX,GY,NP,savedColour = readOptionsDoc()

    #Create screen                
    resolution = (1000,650)
    TextColour = (0,255,0)
    buttonSize = 90
    textSize = 60
    text = []
    optionsScreen = pygame.display.set_mode(resolution)

    pygame.display.set_caption("boop 'em")
    icon= pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    #Create font and write the title and draw the back button
    myfont = pygame.font.SysFont('tektonproboldext', 80)
    titleText = myfont.render("Options", 0, TextColour, (0,0,0))
    optionsScreen.blit(titleText,(10,10))
    backButtonImage = pygame.image.load('home.png')
    optionsScreen.blit(backButtonImage,(resolution[0]-buttonSize,resolution[1]-buttonSize))

    #define the sub titles
    myfont = pygame.font.SysFont('tektonproboldext', textSize)
    text.append("Resolution:")
    text.append("Grid Size:")
    text.append("No. of Players:")
    text.append("Colour:")

    #write the sub titles
    for counter in range(0,4):
        subtitleText = myfont.render(text[counter], 0, TextColour, (0,0,0))
        optionsScreen.blit(subtitleText,(10,(textSize * counter) + 100))

    #Define a new font size
    textSize = 45
    myfont = pygame.font.SysFont('tektonproboldext', textSize)

    #Write each players name in the colour that their counters are
    for counter in range(8):
        text = str("Player " + str(counter+1)+ ":")
        playersText = myfont.render(text, 0, savedColour[counter], (0,0,0))
        if counter < 4:
            optionsScreen.blit(playersText,(10,(textSize * (counter+1)) + 320))
        else:
            optionsScreen.blit(playersText,(510,(textSize * (counter-3)) + 320))

    #Define the different colours avalible to pick from
    colour = []
    colour.append([0,255,0])
    colour.append([255,0,0])
    colour.append([0,0,255])
    colour.append([255,255,0])
    colour.append([255,0,255])
    colour.append([0,255,255])
    colour.append([255,255,255])
    colour.append([255,127,0])
    colour.append([127,0,127])
    colour.append([0,120,0])

    #Define variables and arrays used for text input
    activeColour = (100,100,100)
    inactiveColour = (50,50,50)
    size = (300,textSize)
    temp = []
    activeRX = False
    activeRY = False
    activeGX = False
    activeGY = False
    activeNP = False

    #Draw in the input boxes for each of the variables that accept any number
    inputBox = pygame.draw.rect(optionsScreen, inactiveColour, (500,(textSize*1)+60,240,textSize+1))
    resolutionX = pygame.Rect(inputBox)
    inputBox = pygame.draw.rect(optionsScreen, inactiveColour, (750,(textSize*1)+60,240,textSize+1))
    resolutionY = pygame.Rect(inputBox)
    inputBox = pygame.draw.rect(optionsScreen, inactiveColour, (500,(textSize*2)+80,240,textSize+1))
    gridSizeX = pygame.Rect(inputBox)
    inputBox = pygame.draw.rect(optionsScreen, inactiveColour, (750,(textSize*2)+80,240,textSize+1))
    gridSizeY = pygame.Rect(inputBox)
    inputBox = pygame.draw.rect(optionsScreen, inactiveColour, (500,(textSize*3)+100,240,textSize+1))
    numberOfPlayers = pygame.Rect(inputBox)

    #Define variables for drawing in the colour selector
    width = 20
    height = textSize * 4

    #Draw the colours in so the users know where to click to select each colour
    for counter in range (10):
        pygame.draw.rect(optionsScreen,colour[counter],(255+((width)*counter), 360,width,height),0)
        pygame.draw.rect(optionsScreen,colour[counter],(755+((width)*counter), 360,width,height),0)

    #Draw lines separating each players colours with lines
    for counter in range(4):
        pygame.draw.line(optionsScreen,(0,0,0),(255,360+textSize*counter),(500,360+textSize*counter),10)
        pygame.draw.line(optionsScreen,(0,0,0),(750,360+textSize*counter),(1000,360+textSize*counter),10)

    #Write in what the numbers currently are for the resolution, grid size and number of players
    writing(RX, (500,(textSize*1)+60,240,textSize-5),inactiveColour)
    writing(RY, (750,(textSize*1)+60,240,textSize-5),inactiveColour)
    writing(GX, (500,(textSize*2)+80,240,textSize-5),inactiveColour)
    writing(GY,(750,(textSize*2)+80,240,textSize-5),inactiveColour)
    writing(NP,(500,(textSize*3)+100,240,textSize-5),inactiveColour)

    #See if a key has been pressed
    pos = [None,None]
    while not done:
        for event in pygame.event.get():
            #See if the screen was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos[0],pos[1] = event.pos
                    
                    #Check to see if player has clicked on the home button
                    if pos[0] > int(resolution[0]) - buttonSize and pos[1] > int(resolution[1]) - buttonSize:
                        #Check to see if the values are below the minimum and if so change them to the minimum
                        if int(RX) < 100:
                            RX = 100
                        if int(RY) < 100:
                            RY = 100
                        if int(GX) < 4:
                            GX = 3
                        if int(GY) < 4:
                            GY = 3
                        if int(NP) < 3:
                            NP = 2
                        #If so write the values to the options document
                        writeOptionsDoc(RX,RY,GX,GY,NP,savedColour)
                        return()
                    
                    #Check to see if they click a colour
                    if pos[0] > 255 and pos[0] < 255 + width*10 and pos[1] > 360 and pos[1] < 360 + textSize*4:
                        #if a colour is clicked find the player it refers to and the colour
                        player = int((pos[1] -360) / textSize)
                        colourNumber = int((pos[0]-255)/width)
                        text = str("Player " + str(player+1)+ ":")
                        #Make the text that refers to the player the colour they selected
                        playersText = myfont.render(text, 0, colour[colourNumber], (0,0,0))
                        optionsScreen.blit(playersText,(10,(textSize * (player+1)) + 320))
                        savedColour[player] = colour[colourNumber]
                    #Do the same for the other 4 players
                    if pos[0] > 755 and pos[0] < 755 + width*10 and pos[1] > 360 and pos[1] < 360 + textSize*4:
                        player = int((pos[1] -360) / textSize)
                        colourNumber = int((pos[0]-755)/width)
                        text = str("Player " + str(player+5)+ ":")
                        playersText = myfont.render(text, 0, colour[colourNumber], (0,0,0))
                        optionsScreen.blit(playersText,(510,(textSize * (player+1)) + 320))
                        savedColour[player+4] = colour[colourNumber]

                    #Start of text input

                    #See if any of the places to input text were clicked and if so highlight that box
                    if resolutionX.collidepoint(event.pos):
                        activeRX = True
                        writing(RX, (500,(textSize*1)+60,240,textSize+1),activeColour)
                        workingOn = resolutionX
                    else:
                        activeRX = False
                        writing(RX, (500,(textSize*1)+60,240,textSize+1),inactiveColour)

                    if resolutionY.collidepoint(event.pos):
                        activeRY = True
                        writing(RY, (750,(textSize*1)+60,240,textSize+1),activeColour)
                        workingOn = resolutionY
                    else:
                        activeRY = False
                        writing(RY, (750,(textSize*1)+60,240,textSize+1),inactiveColour)

                    if gridSizeX.collidepoint(event.pos):
                        activeGX = True
                        writing(GX, (500,(textSize*2)+80,240,textSize+1),activeColour)
                        workingOn = gridSizeX
                    else:
                        activeGX = False
                        writing(GX, (500,(textSize*2)+80,240,textSize+1),inactiveColour)

                    if gridSizeY.collidepoint(event.pos):
                        activeGY = True
                        writing(GY,(750,(textSize*2)+80,240,textSize+1),activeColour)
                        workingOn = gridSizeY
                    else:
                        activeGY = False
                        writing(GY,(750,(textSize*2)+80,240,textSize+1),inactiveColour)

                    if numberOfPlayers.collidepoint(event.pos):
                        activeNP = True
                        writing(NP,(500,(textSize*3)+100,240,textSize+1),activeColour)
                        workingOn = numberOfPlayers
                    else:
                        activeNP = False
                        writing(NP,(500,(textSize*3)+100,240,textSize+1),inactiveColour)

            #Collect text and print it
            if event.type == pygame.KEYDOWN and activeRX == True:
                RX = collectInput(RX,2560)
                writing(RX, (500,(textSize*1)+60,240,textSize+1),activeColour)
            if event.type == pygame.KEYDOWN and activeRY == True:
                RY = collectInput(RY,1440)
                writing(RY, (750,(textSize*1)+60,240,textSize+1),activeColour)
            if event.type == pygame.KEYDOWN and activeGX == True:
                GX = collectInput(GX,12)
                writing(GX, (500,(textSize*2)+80,240,textSize+1),activeColour)
            if event.type == pygame.KEYDOWN and activeGY == True:
                GY = collectInput(GY,12)
                writing(GY,(750,(textSize*2)+80,240,textSize+1),activeColour)
            if event.type == pygame.KEYDOWN and activeNP == True:
                NP = collectInput(NP,8)
                writing(NP,(500,(textSize*3)+100,240,textSize+1),activeColour)
            
            pygame.display.update()
                        
            #Quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#The instructions menu
def Instructions():
    #Define variables and arrays
    resolution = (1000,750)
    buttonSize = 90
    Screen = pygame.display.set_mode(resolution)

    #Create the screen
    pygame.display.set_caption("boop 'em")
    icon= pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    #Post the image that has all the instructions on it and the home button
    instructionsImage = pygame.image.load('instructions.png')
    Screen.blit(instructionsImage,(0,0))
    backButtonImage = pygame.image.load('home.png')
    Screen.blit(backButtonImage,(resolution[0]-buttonSize,resolution[1]-buttonSize))
    pygame.display.update()

    #Check to see if the user clicked the home button and if so open the main menu
    pos = [None,None]
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos[0],pos[1] = event.pos
                #Check to see if player has clicked on the home button
                if pos[0] > int(resolution[0]) - buttonSize and pos[1] > int(resolution[1]) - buttonSize:
                    return()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#Doing the scores screen
def Scores():
    #Define variables and arrays used
    Score = []
    splitter = []
    sorter = []
    sorterSpot = []
    sortedList = []
    counter = True
    fileLength = 0
    scoreFile = open("scores.txt","r")

    #Find the length of the scores file
    while counter == True:
        if scoreFile.readline() != "":
            fileLength += 1
        else:
            counter = False

    scoreFile.close()
    
    #Reopen the scores file to read it from the start
    scoreFile = open("scores.txt","r")

    #Save the file to the array Score
    for i in range (fileLength):
        Score.append(scoreFile.readline())

    scoreFile.close()

    #Split up the array Score after each comma to allow me to look at the name and the number of points individually
    for counter in range (fileLength):
        splitter.append(Score[counter].split(","))

    #Take away the new line from each of the points
    for counter in range(fileLength):
        splitter[counter][1] = splitter[counter][1][:-1]

    #Sub routine to swap two items around
    def swap(item1,item2):
        return(item2,item1)

    #Loop for the length of the list
    for index in range(fileLength):

        #Set the item being sorted the the number in the list equal to that of the number of times the list has been looped
        sortedItem = int(splitter[index][1])
        #Set the sport being looked at to the number of times the list has been looped
        sorterSpot = index

        #Loop while the number before it is less that the item being sorted, and it isn't at the start of the loop
        while int(splitter[sorterSpot-1][1]) < sortedItem and sorterSpot > 0:
            #Swap the 2 items
            splitter[sorterSpot-1],splitter[sorterSpot] = swap(splitter[sorterSpot-1],splitter[sorterSpot])
            #Check to see if it needs swapped again
            sorterSpot -= 1

    #Rename splitter
    sortedList = splitter

    #Create the variables used look of the screen
    myfont = pygame.font.SysFont('tektonproboldext', 70)
    resolution = (700,750)
    buttonSize = 90
    Screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("boop 'em")
    icon= pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    backButtonImage = pygame.image.load('home.png')
    TextColour = (0,255,0)
    titleText = myfont.render("Top 10 Scores", 0, TextColour, (0,0,0))

    #Render the title and the back button
    Screen.blit(titleText,(10,10))
    Screen.blit(backButtonImage,(resolution[0]-buttonSize,resolution[1]-buttonSize))
    pygame.display.update()

    #Shorten the array if needed to only display 10 items
    if fileLength > 10:
        fileLength = 10

    #Render the scores
    myfont = pygame.font.SysFont('tektonproboldext', 50)
    for counter in range(fileLength):
        scoreTextName = myfont.render(sortedList[counter][0], 0, TextColour, (0,0,0))
        Screen.blit(scoreTextName,(10,((counter * 60)+100)))
        scoreTextScore = myfont.render(sortedList[counter][1], 0, TextColour, (0,0,0))
        Screen.blit(scoreTextScore,(300,((counter * 60)+100)))

    pygame.display.update()

    #See if the back button was pressed and if so go back to the main menu
    pos = [None,None]
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                    pos[0],pos[1] = event.pos
                    #Check to see if player has clicked on the home button
                    if pos[0] > int(resolution[0]) - buttonSize and pos[1] > int(resolution[1]) - buttonSize:
                        return()

            #Quit button
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

#Read options file           
def readOptionsDoc():
    #Defining arrays
    temp = []
    tempColour = []
    colour = []
    separated = []
    optionsFile = open("options.txt","r")

    #Read in the file and remove /n at the end of each line
    for counter in range(13):
        temp.append(optionsFile.readline())
        temp[counter] = temp[counter][:-1]

    #Save each value readen to appropriate variables  
    resolutionX = temp[0]
    resolutionY = temp[1]
    gridSizeX = temp[2]
    gridSizeY = temp[3]
    numberOfPlayers = temp[4]
    for counter in range(1,9):
        tempColour.append(temp[counter+4])
    optionsFile.close()

    #Making it so that the colours are read as arrays rather than strings
    for counter in range(8):
        separated.append(tempColour[counter].split(","))
    for counter in range(8):
        separated[counter][0] = int(separated[counter][0].strip("[" or "("))
        separated[counter][1] = int(separated[counter][1])
        separated[counter][2] = int(separated[counter][2][:-1])
        colour.append(separated[counter])

    return(resolutionX,resolutionY,gridSizeX,gridSizeY,numberOfPlayers,colour)

#Writing to the options file with the options given in the options menu
def writeOptionsDoc(RX,RY,GX,GY,NP,colour):
    #If a options menu doesn't exist create one
    try:
        optionsFile = open ("options.txt", "a")
    except FileNotFoundError:
        optionsFile = open ("options.txt", "x")
        optionsFile.close()

    #Write in all the data to the file   
    optionsFile = open ("options.txt", "w")
    optionsFile.write(str(RX) + "\n")
    optionsFile.write(str(RY) + "\n")
    optionsFile.write(str(GX) + "\n")
    optionsFile.write(str(GY) + "\n")
    optionsFile.write(str(NP) + "\n")
    for counter in range(8):
        optionsFile.write(str(colour[counter]) + "\n")
    optionsFile.close()

#Start of running sub routines  
done = False
while not done:
    #Start with by opening the Main Menu
    pick = "MainMenu"    

    #run the main menu
    if pick == "MainMenu":
        pick = MainMenu()
        pygame.time.delay(50)
    #run the game play
    if pick == "PlayGame":
        TheGame()
    #run the options menu
    if pick == "options":
        Options()
    #run the instructions menu
    if pick == "instructions":
        Instructions()
    #run the scores
    if pick == "scores":
        Scores()
