def print_progress_bar(current_value, max_value, bar_length=30):
    """
    Print a progress bar.

    Parameters:
    - current_value: Current value for the progress.
    - max_value: Maximum value for the progress.
    - bar_length: Length of the progress bar (default is 30).
    
    Returns:
    A string representing the progress bar.
    """
    progress = float(current_value) / max_value
    num_blocks = int(round(bar_length * progress))
    bar = "[" + "=" * num_blocks + " " * (bar_length - num_blocks) + "]"
    percentage = round(progress * 100, 2)
    return f"{bar} {percentage}%"


def test():
    # Example usage:
    current_value = 363
    max_value = 365
    
    for i in range(max_value):
        progress_bar_str = print_progress_bar(i, max_value)
        print(i, progress_bar_str)


if __name__ == "__main__":
    test()