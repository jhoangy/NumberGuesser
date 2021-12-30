# Importing necessary packages
import shutil
import tkinter
from tkinter import *
from tkinter import messagebox, filedialog


# Defining CreateWidgets() function to
# create necessary tkinter widgets
def CreateWidgets():

    root = Tk()

    # Setting the title and background color
    # disabling the resizing property
    root.geometry("830x120")
    root.title("Copy-Move GUI")
    root.config(background = "black")

    # Creating tkinter variable
    sourceLocation = StringVar()
    destinationLocation = StringVar()

    link_Label = Label(root, text ="Select The File To Copy : ",
                       bg = "#E8D579")
    link_Label.grid(row = 1, column = 0,
                    pady = 5, padx = 5)

    root.sourceText = Entry(root, width = 50,
                            textvariable = sourceLocation)
    root.sourceText.grid(row = 1, column = 1,
                         pady = 5, padx = 5,
                         columnspan = 2)

    source_browseButton = Button(root, text ="Browse",
                                 command = lambda: SourceBrowse(root), width = 15)
    source_browseButton.grid(row = 1, column = 3,
                             pady = 5, padx = 5)

    destinationLabel = Label(root, text ="Select The Destination  : ",
                             bg ="#E8D579")
    destinationLabel.grid(row = 2, column = 0,
                          pady = 5, padx = 5)

    root.destinationText = Entry(root, width = 50,
                                 textvariable = destinationLocation)
    root.destinationText.grid(row = 2, column = 1,
                              pady = 5, padx = 5,
                              columnspan = 2)

    dest_browseButton = Button(root, text ="Browse",
                               command = lambda: DestinationBrowse(root), width = 15)
    dest_browseButton.grid(row = 2, column = 3,
                           pady = 5, padx = 5)

    copyButton = Button(root, text ="Copy File",
                        command = lambda: CopyFile(root,destinationLocation), width = 15)
    copyButton.grid(row = 3, column = 1,
                    pady = 5, padx = 5)

    moveButton = Button(root, text ="Move File",
                        command = lambda: MoveFile(root,destinationLocation), width = 15)
    moveButton.grid(row = 3, column = 2,
                    pady = 5, padx = 5)
    root.mainloop()

def SourceBrowse(root):

    # Opening the file-dialog directory prompting
    # the user to select files to copy using
    # filedialog.askopenfilenames() method. Setting
    # initialdir argument is optional Since multiple
    # files may be selected, converting the selection
    # to list using list()
    root.sourceText.delete(0, 'end')
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
    root.destinationText.delete(0, 'end')
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

def MoveFile(root,destinationLocation):

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



# Calling the CreateWidgets() function
# Creating object of tk class

CreateWidgets()

# Defining infinite loop
