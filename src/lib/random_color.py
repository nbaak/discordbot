import random
from PIL import Image


def random_color_picker(alpha=255):
    while True:
        # Generate random values for red, green, and blue channels
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        # Define a threshold for light grey exclusion
        grey_threshold = 200

        # Ensure the color is neither white nor light grey
        if (r, g, b) != (255, 255, 255) and (r, g, b) != (grey_threshold, grey_threshold, grey_threshold):
            return (r, g, b, alpha)


def generate_color_image(color):
    # Create a new image with the specified color
    image = Image.new('RGBA', (100, 100), color)

    # Save or display the image
    image.show()  # Open the image with the default image viewer
    # image.save('random_color_image.png')  # Save the image to a file


def test():
    # Example usage
    random_rgba_color = random_color_picker()
    print(random_rgba_color)

    generate_color_image(random_rgba_color)


if __name__ == "__main__":
    test()
