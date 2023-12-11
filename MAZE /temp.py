import tkinter as tk

window = tk.Tk()

canvas = tk.Canvas(window)
canvas.pack()

#Tkinter has an arrow option in the create_line method. tk.Last specifies the position at which 
#the arrow is placed, in this case the last coordinate set of the line, hence "LAST".
canvas.create_line(0, 0, 200, 100, arrow=tk.LAST)  

window.mainloop()