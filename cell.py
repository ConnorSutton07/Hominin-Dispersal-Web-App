import numpy as np
from random import random
from PIL import Image

p_col = 0.20
noise_constant = 0.03

class Cell:
    def __init__(self, i, j, active, veg_P_ext, elv_P_ext, density_P_ext):
        self.x = int(i / 5)
        self.y = int(j / 5)
        self.active = active # ignored in simulation 
        self.occupied = False # initalize all cells to unoccupied
        self.veg_P_ext = veg_P_ext + np.random.normal(0, noise_constant) # probability of extinction based on vegetation
        self.elv_P_ext = elv_P_ext + np.random.normal(0, noise_constant) # probability of extinction based on elevation
        self.density_P_ext = density_P_ext # probability of extinction based on population sensity
        self.P_ext = self.veg_P_ext + self.elv_P_ext + self.density_P_ext # total probability of extinction
        
    def becomeOccupied(self):
        self.occupied = True
        
    def becomeExtinct(self):
        self.occupied = False
        
    def getValidNeighboringCells(self, e):
        d = [] # empty directions array
        i = self.x
        j = self.y
        if (e.cells[i-1][j].active and not e.cells[i-1][j].occupied):
            d.append('u')
        if (e.cells[i+1][j].active and not e.cells[i+1][j].occupied):
            d.append('d')
        if (e.cells[i][j-1].active and not e.cells[i][j-1].occupied):
            d.append('l')
        if (e.cells[i][j+1].active and not e.cells[i][j+1].occupied):
            d.append('r')
        return d
    
    def checkPopulationDensity(self, e): # search cells in a 5x5 grid for neighbors
        neighbors = 0
        i, j = self.x, self.y
        for k in range(5):
            for l in range(5):
                if (e.cells[i-2][j-2].occupied): 
                    neighbors += 1
        return (neighbors / 96) + np.random.normal(0, noise_constant)
    
        
    def colonizeNeighbor(self, direction, e): 
        i = self.x
        j = self.y
        if (direction == 'u'):
            e.cells[i-1][j].becomeOccupied()
            #print("cell at", i, ", ", j, "is colonizing up.")
        elif (direction == 'd'):
            e.cells[i+1][j].becomeOccupied()
            #print("cell at", i, ", ", j, "is colonizing down.")
        elif (direction == 'l'):
            e.cells[i][j-1].becomeOccupied()
            #print("cell at", i, ", ", j, "is colonizing left.")
        elif (direction == 'r'):
            e.cells[i][j+1].becomeOccupied()
            #print("cell at", i, ", ", j, "is colonizing right.")
            
    
    def update(self, e): # called each time step if cell is active and populated
        self.P_density_ext = self.checkPopulationDensity(e) 
        self.P_ext = self.veg_P_ext + self.elv_P_ext + self.density_P_ext # update probability of extinction
        #e.cells[self.x][self.y].P_ext = self.P_ext
        if (self.active and self.occupied):
            if (random() < p_col):
                potential_directions = self.getValidNeighboringCells(e)
                if (len(potential_directions) > 0):
                    direction = potential_directions[int(random() * len(potential_directions))]
                    self.colonizeNeighbor(direction, e)
            if (random() < self.P_ext):
                self.becomeExtinct()
                
        
        
            
def setup_cells(rows, cols):
    cells = [[0 for i in range(cols)] for j in range(rows)] # initialize cell array
    veg_im = Image.open("images/vegetation_map.png")
    elv_im = Image.open("images/elevation_map.png")

    #for i in range(0, 1150, 5):
    #    for j in range(0, 850, 5):
    for i in range(0, rows * 5, 5):
        for j in range(0, cols * 5, 5):
            pix = veg_im.getpixel((i,j))
            elv_pix = elv_im.getpixel((i, j))
            if (not(pix[0] == pix[1] == pix[2] == 255)): # if not an all-white pixel
                P_ext = 1.0
                elv_P_ext = 0.0
                if (pix[0] == 7 and pix[1] == 120 and pix[2] == 11): # Temperate Forest
                    P_ext = 0.12
                elif (pix[0] == 255 and pix[1] == 128 and pix[2] == 0): # Grassland
                    P_ext = 0.12
                elif (pix[0] == 255 and pix[1] == 242 and pix[2] == 0): # Desert
                    P_ext = 0.17
                elif (pix[0] == 0 and pix[1] == 79 and pix[2] == 0): # Tropical Forest
                    P_ext = 0.12
                elif (pix[0] == 22 and pix[1] == 204 and pix[2] == 250): # Tundra
                    P_ext = 1.0
                elif (pix[0] == 164 and pix[1] == 252 and pix[2] == 67): # Warm-temperate Forest
                    P_ext = 0.18
                elif (pix[0] == 128 and pix[1] == 128 and pix[2] == 255): # Boreal Forest
                    P_ext = 1.0
                elif (pix[0] == 132 and pix[1] == 97 and pix[2] == 37): # Savanna
                    P_ext = 0.08
                elif (pix[0] == pix[1] == pix[2] == 200):
                    P_ext = 1.0
                else:
                    P_ext = 1.0
                
                if (elv_pix[0] == 203 and elv_pix[1] == 131 and elv_pix[2] == 7):
                    elv_P_ext = 0.05
                elif (elv_pix[0] == 203 and elv_pix[1] == 41 and elv_pix[2] == 21):
                    elv_P_ext = 0.10
                elif (elv_pix[0] == 112 and elv_pix[1] == 6 and elv_pix[2] == 6):
                    elv_P_ext = 0.22
                    
                cells[int(i/5)][int(j/5)] = Cell(i, j, True, P_ext, elv_P_ext, 0.0) #active cell with parameters based on vegetation, elevation
            else:
                cells[int(i/5)][int(j/5)] = Cell(i, j, False, 1.0, 1.0, 1.0) # inactive cell
                
                
    # cells in East Africa to start with
    cells[84][91].becomeOccupied()
    cells[85][92].becomeOccupied()
    cells[85][96].becomeOccupied()
    cells[86][90].becomeOccupied()
    cells[87][94].becomeOccupied()
    cells[88][93].becomeOccupied()
    # Dmanisi : 79, 46
    return cells