import time
import random
import tkinter as tk
from PIL import Image, ImageTk


def is_grey(color):
    # Check if the color is a shade of grey
    return color[0] == color[1] == color[2]


def random_color_picker(alpha:int=255) -> tuple:
    while True:
        # Generate random values for red, green, and blue channels
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Combine the values into a color tuple
        color = (r, g, b, alpha)

        # Ensure the color is not a shade of grey
        if not is_grey(color):
            return color


def generate_color_image(color:tuple):
    # Create a new image with the specified color
    image = Image.new('RGBA', (100, 100), color)

    # Save or display the image
    image.show()  # Open the image with the default image viewer
    # image.save('random_color_image.png')  # Save the image to a file


def test_single():
    random_rgba_color = random_color_picker()
    print(random_rgba_color)
    generate_color_image(random_rgba_color)


def test():

    class ColorDisplayApp:

        def __init__(self, root):
            self.root = root
            self.root.title("Color Display App")
            self.root.geometry("200x200")

            self.canvas = tk.Canvas(self.root, width=200, height=200)
            self.canvas.pack()

            # Initialize PhotoImage as an instance variable
            self.photo = None

            self.show_random_color()

        def show_random_color(self):
            random_rgba_color = random_color_picker()
            print(random_rgba_color)

            # Create a PhotoImage and keep a reference to it
            self.photo = ImageTk.PhotoImage(Image.new('RGBA', (200, 200), random_rgba_color))

            # Get the dimensions of the Canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            # Create image coordinates to span the entire Canvas
            x0, y0, x1, y1 = 0, 0, canvas_width, canvas_height

            self.canvas.delete("all")
            self.canvas.create_image(x0, y0, anchor="nw", image=self.photo)

            # Close the old color image after 1 second
            self.root.after(1000, self.show_random_color)

    root = tk.Tk()
    app = ColorDisplayApp(root)
    root.mainloop()


if __name__ == "__main__":
    test()
