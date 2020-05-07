import tkinter

def print_value(val):
    print(val)

root = tkinter.Tk()

scale = tkinter.Scale(orient='horizontal', from_=0, to=255, command=print_value,resolution=3)
scale.pack()

root.mainloop()