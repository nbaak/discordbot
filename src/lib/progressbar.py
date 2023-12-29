from PIL import Image, ImageDraw, ImageFont


class ProgressBar:

    def __init__(self, max_value, bar_length=30):
        """
        Initialize the ProgressBar.

        Parameters:
        - max_value: Maximum value for the progress.
        - bar_length: Length of the progress bar (default is 30).
        """
        self.max_value = max_value
        self.bar_length = bar_length

    def get(self, current_value):
        """
        Get the progress bar as a string.

        Parameters:
        - current_value: Current value for the progress.

        Returns:
        A string representing the progress bar.
        """
        progress = float(current_value) / self.max_value
        num_blocks = int(round(self.bar_length * progress))
        bar = "[" + "=" * num_blocks + " " * (self.bar_length - num_blocks) + "]"
        percentage = round(progress * 100, 2)
        return f"{bar} {percentage}%"

    def image(self, current_value, output_file="progress_bar.png"):
        """
        Render the progress bar as an image.

        Parameters:
        - current_value: Current value for the progress.
        - output_file: File name for the output image (default is "progress_bar.png").
        """
        # Create an image with white background
        image = Image.new("RGB", (400, 50), "white")
        draw = ImageDraw.Draw(image)

        # Calculate the width of the green passed part
        progress = float(current_value) / self.max_value
        passed_width = int((395 - 5) * progress)  # Adjusted width to stop 10px before the end

        # Draw the white upcoming part
        draw.rectangle([(5 + passed_width, 5), (395, 40)], fill="white")

        # Draw the green passed part
        draw.rectangle([(5, 10), (5 + passed_width, 40)], fill="green")

        # Draw black outline for the progress bar
        draw.rectangle([(5, 5), (395, 45)], outline="black")

        # Add text label in the middle
        percentage = round(progress * 100, 2)
        label = f"{current_value}/{self.max_value} {percentage}%"
        font = ImageFont.load_default(size=10)
        font_box = font.getbbox(label)

        _, _, text_width, text_height = font_box

        text_position = ((400 - text_width) // 2, (50 - text_height) // 2)
        draw.text(text_position, label, fill="black")

        # Save the image to a file
        image.save(output_file)


def test():
    # Example usage:
    current_value = 363
    max_value = 365
    progress_bar = ProgressBar(max_value)

    progress_bar.image(0, f"pb-0.png")
    progress_bar.image(8, f"pb-8.png")
    progress_bar.image(180, f"pb-180.png")
    progress_bar.image(365, f"pb-365.png")

    for i in range(max_value + 1):
        progress_bar_str = progress_bar.get(i)
        print(i, progress_bar_str)


if __name__ == "__main__":
    test()
