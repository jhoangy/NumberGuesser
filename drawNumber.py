import sys, os
import pygame
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
import shutil
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import cv2


class pixel(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (0,0,0)
        self.neighbors = []

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.x + self.width, self.y + self.height))

    def getNeighbors(self, g):
        # Get the neighbours of each pixel in the grid, this is used for drawing thicker lines
        j = self.x // 20 # the var i is responsible for denoting the current col value in the grid
        i = self.y // 20 # the var j is responsible for denoting thr current row value in the grid
        rows = 28
        cols = 28

        # Horizontal and vertical neighbors
        if i < cols - 1:  # Right
            self.neighbors.append(g.pixels[i + 1][j])
        if i > 0:  # Left
            self.neighbors.append(g.pixels[i - 1][j])
        if j < rows - 1:  # Up
            self.neighbors.append(g.pixels[i][j + 1])
        if j > 0:  # Down
            self.neighbors.append(g.pixels[i][j - 1])

        # Diagonal neighbors
        if j > 0 and i > 0:  # Top Left
            self.neighbors.append(g.pixels[i - 1][j - 1])

        if j + 1 < rows and i > -1 and i - 1 > 0:  # Bottom Left
            self.neighbors.append(g.pixels[i - 1][j + 1])

        if j - 1 < rows and i < cols - 1 and j - 1 > 0:  # Top Right
            self.neighbors.append(g.pixels[i + 1][j - 1])

        if j < rows - 1 and i < cols - 1:  # Bottom Right
            self.neighbors.append(g.pixels[i + 1][j + 1])


class grid(object):
    pixels = []

    def __init__(self, row, col, width, height):
        self.rows = row
        self.cols = col
        self.len = row * col
        self.width = width
        self.height = height
        self.generatePixels()
        pass

    def draw(self, surface):
        for row in self.pixels:
            for col in row:
                col.draw(surface)

    def generatePixels(self):
        x_gap = self.width // self.cols
        y_gap = self.height // self.rows
        self.pixels = []
        for r in range(self.rows):
            self.pixels.append([])
            for c in range(self.cols):
                self.pixels[r].append(pixel(x_gap * c, y_gap * r, x_gap, y_gap))

        for r in range(self.rows):
            for c in range(self.cols):
                self.pixels[r][c].getNeighbors(self)

    def clicked(self, pos): #Return the position in the grid that user clicked on
        try:
            t = pos[0]
            w = pos[1]
            #g1 = int(t) // self.pixels[0][0].width
            g1 = int(t) // self.pixels[0][0].width
            g2 = int(w) // self.pixels[0][0].height

            return self.pixels[g2][g1]
        except:
            pass

    def convert_binary(self):
        li = self.pixels

        newMatrix = [[] for x in range(len(li))]

        for i in range(len(li)):
            for j in range(len(li[i])):
                if li[i][j].color == (0,0,0):
                    newMatrix[i].append(0)
                else:
                    newMatrix[i].append(1)

        np_array = np.array(newMatrix)
        img = Image.fromarray(np.uint8(np_array * 255) , 'L')
        img.save('num.jpg')

def guess():
    model = tf.keras.models.load_model('real.model')
    x = [prepare('num.jpg')]
    predictions = model.predict(x)
    print(predictions[0])
    t = (np.argmax(predictions[0]))
    print("I predict this number is a:", t)
    window = Tk()
    window.withdraw()
    messagebox.showinfo("Prediction", "I predict this number is a: " + str(t))
    window.destroy()
    # Creating object of tk class
    root = Tk()

    # Setting the title and background color
    # disabling the resizing property
    root.geometry("830x120")
    root.title("Copy-Move GUI")
    root.config(background = "black")

    # Creating tkinter variable
    sourceLocation = StringVar()
    destinationLocation = StringVar()

    # Calling the CreateWidgets() function
    CreateWidgets(root,sourceLocation,destinationLocation)

    # Defining infinite loop
    root.mainloop()

# Defining CreateWidgets() function to
# create necessary tkinter widgets
def CreateWidgets(root,sourceLocation,destinationLocation):
    link_Label = Label(root, text ="Select The File To Copy : ",
                       bg = "#E8D579")
    link_Label.grid(row = 1, column = 0,
                    pady = 5, padx = 5)

    root.sourceText = Entry(root, width = 50,
                            textvariable = sourceLocation)
    root.sourceText.grid(row = 1, column = 1,
                         pady = 5, padx = 5,
                         columnspan = 2)

    source_browseButton = Button(root, text ="Browse", command = lambda : SourceBrowse(root), width = 15)
    source_browseButton.grid(row = 1, column = 3, pady = 5, padx = 5)

    destinationLabel = Label(root, text ="Select The Destination  : ", bg ="#E8D579")
    destinationLabel.grid(row = 2, column = 0,pady = 5, padx = 5)

    root.destinationText = Entry(root, width = 50, textvariable = destinationLocation)
    root.destinationText.grid(row = 2, column = 1, pady = 5, padx = 5, columnspan = 2)

    dest_browseButton = Button(root, text ="Browse",command = lambda : DestinationBrowse(root), width = 15)
    dest_browseButton.grid(row = 2, column = 3,pady = 5, padx = 5)

    copyButton = Button(root, text ="Copy File",command = lambda : CopyFile(root,destinationLocation), width = 15)
    copyButton.grid(row = 3, column = 1,pady = 5, padx = 5)

    moveButton = Button(root, text ="Move File", command = MoveFile, width = 15)
    moveButton.grid(row = 3, column = 2,pady = 5, padx = 5)

def SourceBrowse(root):

    # Opening the file-dialog directory prompting
    # the user to select files to copy using
    # filedialog.askopenfilenames() method. Setting
    # initialdir argument is optional Since multiple
    # files may be selected, converting the selection
    # to list using list()
    root.files_list = list(filedialog.askopenfilenames(initialdir =sys.path[0] , filetypes=[("JPG Files", ".jpg")]))

    # Displaying the selected files in the root.sourceText
    # Entry using root.sourceText.insert()
    root.sourceText.insert('1', root.files_list)

def DestinationBrowse(root):
    # Opening the file-dialog directory prompting
    # the user to select destination folder to
    # which files are to be copied using the
    # filedialog.askopendirectory() method.
    # Setting initialdir argument is optional
    destinationdirectory = filedialog.askdirectory(initialdir =sys.path[0])

    # Displaying the selected directory in the
    # root.destinationText Entry using
    # root.destinationText.insert()
    root.destinationText.insert('1', destinationdirectory)

def CopyFile(root,destinationLocation):
    # Retrieving the source file selected by the
    # user in the SourceBrowse() and storing it in a
    # variable named files_list
    files_list = root.files_list

    # Retrieving the destination location from the
    # textvariable using destinationLocation.get() and
    # storing in destination_location
    destination_location = destinationLocation.get()

    # Looping through the files present in the list
    for f in files_list:

        # Copying the file to the destination using
        # the copy() of shutil module copy take the
        # source file and the destination folder as
        # the arguments
        shutil.copy(f, destination_location)

    messagebox.showinfo("SUCCESSFULL")

def MoveFile():

    # Retrieving the source file selected by the
    # user in the SourceBrowse() and storing it in a
    # variable named files_list'''
    files_list = root.files_list

    # Retrieving the destination location from the
    # textvariable using destinationLocation.get() and
    # storing in destination_location
    destination_location = destinationLocation.get()

    # Looping through the files present in the list
    for f in files_list:

        # Moving the file to the destination using
        # the move() of shutil module copy take the
        # source file and the destination folder as
        # the arguments
        shutil.move(f, destination_location)

    messagebox.showinfo("SUCCESSFULL")

def prepare(filepath):
    IMG_SIZE = 28  # 50 in txt-based
    img_array = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                g.convert_binary()
                guess()
                g.generatePixels()
            if pygame.mouse.get_pressed()[0]:

                pos = pygame.mouse.get_pos()
                clicked = g.clicked(pos)
                clicked.color = (255,255,255)
                for n in clicked.neighbors:
                    #if n == 0:
                    n.color = (255,255,255)


            if pygame.mouse.get_pressed()[2]:
                try:
                    pos = pygame.mouse.get_pos()
                    clicked = g.clicked(pos)
                    clicked.color = (0,0,0)
                except:
                    pass

        g.draw(win)
        pygame.display.update()

pygame.init()
width = height = 560
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Number Guesser")
g = grid(28, 28, width, height)
main()


pygame.quit()
quit()
