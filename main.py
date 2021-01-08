import streamlit as st
import time
import numpy as np
from cell import Cell, setup_cells
from PIL import Image
import copy

# 1. Create initial cell array with active/inactive cells depending on whether or not they are on land
# 2. Give active cells probabilities of extinction based on their vegetation class and altitude level
# 3. Populate a few cells in East Africa; these are the starting populations

rows, cols = (205, 155)
cells = setup_cells(rows, cols)
st.cache(func=setup_cells)

# Defines Ensemble class which is responsible for carrying out a run of the simulation for comparison with other ensembles
class Ensemble:
    def __init__(self):
        self.cells = copy.deepcopy(cells)
    def update(self):
        for row in self.cells:
            for cell in row:
                if (cell.occupied):
                    cell.update(self)


# add a title to the page
st.title("Pleistocene Hominin Dispersal")
st.subheader("A Simulation using Cellular Automata")
for i in range(5):
    st.write("")

# add slider for number of ensembles
num_ensembles = st.sidebar.slider("Number of ensembles", min_value=1, max_value=30, step=1, value=3)
ensembles = [Ensemble() for i in range(num_ensembles)]

# add slider for number of time steps
steps = st.sidebar.slider("Number of 250-year time steps", min_value=100, max_value=2000, step=100, value=1000)


# background image upon opening page
image = Image.open("images/afroeurasia.png")
# put background image to page
stImage = st.image(image, use_column_width=True)

st.markdown('[Learn More](https://github.com/ConnorSutton07/Simulating-H.-Erectus-Dispersal-with-Cellular-Automata)')

ageText = st.sidebar.text("Current Time: 2,000,000 years ago")

# add progress bar to sidebar
progressBar = st.sidebar.progress(0)

def run():
    age = 2000000 # starting age
    for a in range(steps):
        for ensemble in ensembles:
            ensemble.update()
        im = image.copy()
        for i in range(rows):
            for j in range(cols):
                num_occupied = 0
                for ensemble in ensembles:
                    if (ensemble.cells[i][j].occupied):
                        num_occupied+=1
                if (num_occupied > 0):
                    c = int(255 - ((num_occupied / len(ensembles)) * 255))
                    for x in range(5):
                        for y in range(5):
                            im.putpixel((int(i * 5 + (x - 2)), int(j * 5 + (y - 2))), (c, c, c))
        age -= 250
        strAge = str(age)
        strAge = strAge[:1] + "," + strAge[1:4] + "," + strAge[4:]
        progressBar.progress(a / (steps - 1))
        ageText.text("Current Time: " + strAge + " years ago")
        stImage.image(im, output_format="JPEG", use_column_width=True) 

if st.sidebar.button('Run Simulation'):
    run()
