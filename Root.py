from tkinter import *
from Menu import *

master = Tk()
master.geometry("1280x1024")
master.resizable(width=False, height=False)  # locks resizability of window
master.configure(background="green")

# Add title and welcome message
master.title("Memory Card Game in Python")
welcome_message = Label(master, text="Παιχνίδι Mνήμης με Tράπουλα!",
                        bg="green", fg="red",
                        font="Verdana 36 bold italic", bd=1)
welcome_message.place(relx=.5, rely=.05, anchor="n")


Menu(master)
master.mainloop()
