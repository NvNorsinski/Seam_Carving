import tkinter as tk
import seam_carving
from PIL import Image, ImageTk

class Window(tk.Tk):
    def __init__(self, picture_path):
        tk.Tk.__init__(self)
        # first time checking window with result in a wrong value. For this reason the first measurement must be ignored
        self.initial_state = False
        self.P = seam_carving.seamCarving(picture_path)
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.P.cutImage))
        self.panel = tk.Label(self, image=self.img)
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.update_window()

    def update_window(self):
        self.original_width = self.winfo_reqwidth()
        # calculates the amounth of pixels, the image is croped in x- direction, when scaling the window
        diff = self.winfo_width() - self.original_width
        print(diff)
        if diff == 0: self.initial_state = True
        if diff < 0 and self.initial_state == True:
            self.P.deleteNSeams(abs(diff))
            print(abs(diff))



            self.img = ImageTk.PhotoImage(image=Image.fromarray(self.P.cutImage))
            self.panel = tk.Label(self, image=self.img)
            self.panel.pack(side="bottom", fill="both", expand="yes")

        self.after(100, self.update_window)

if __name__== "__main__":
    picture_path = '20150521_115436.jpg'
    app = Window(picture_path)
    app.mainloop()