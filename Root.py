from tkinter import *
from Menu import Menu


master = Tk()
master.geometry("1920x1024")
# master.resizable(width=False, height=False)  # locks resizability of window
master.configure(background="green")
master.minsize(1920, 1024)

# Add title and welcome message
master.title("Memory Card Game in Python")


main_menu = Menu(master)

master.mainloop()
