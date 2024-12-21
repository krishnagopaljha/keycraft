import tkinter as tk
import os
import time
import sys


def generate_wordlist(min_length, max_length, filename, characters):
    """
    Generate a wordlist with lengths in the specified range using given characters and save it to a file.
    """
    start_time = time.perf_counter()  # Start the timer

    with open(filename, "w") as file:  # Open file to write combinations
        for length in range(min_length, max_length + 1):
            combinations = [0] * length  # Initialize list to track character positions

            while True:
                # Create the current combination
                word = ''.join([characters[i] for i in combinations])
                file.write(word + "\n")

                # Update the combination
                for i in range(length - 1, -1, -1):
                    if combinations[i] < len(characters) - 1:
                        combinations[i] += 1
                        break
                    combinations[i] = 0
                else:
                    # Exit condition: If all combinations are exhausted for this length
                    break

    end_time = time.perf_counter()  # End the timer
    return end_time - start_time


def get_unique_filename(base_name="wordlist", extension=".txt"):
    """
    Generate a unique filename by appending a number if the file already exists.
    """
    counter = 0
    filename = f"{base_name}{extension}"
    while os.path.exists(filename):
        counter += 1
        filename = f"{base_name}{counter}{extension}"
    return filename


def start_generation():
    """
    Handle user input from the GUI and start the wordlist generation process.
    """
    try:
        # Get the word length range
        min_length = int(min_length_entry.get())
        max_length = int(max_length_entry.get())
        if min_length < 1 or max_length < 1:
            raise ValueError("Lengths must be at least 1.")
        if min_length > max_length:
            raise ValueError("Minimum length cannot be greater than maximum length.")

        # Get the selected character sets
        characters = ""
        if lowercase_var.get():
            characters += "abcdefghijklmnopqrstuvwxyz"
        if uppercase_var.get():
            characters += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if numbers_var.get():
            characters += "0123456789"
        if special_var.get():
            characters += "!@#$%^&*"
        custom_chars = custom_entry.get()
        if custom_chars:
            characters += custom_chars

        if not characters:
            status_label.config(text="Error: Please select at least one character set.", fg="red")
            return

        # Generate a unique filename
        filename = get_unique_filename()

        # Generate the wordlist
        status_label.config(text="Generating wordlist, please wait...", fg="blue")
        time_taken = generate_wordlist(min_length, max_length, filename, characters)
        status_label.config(text=f"Wordlist saved as {filename}. Completed in {time_taken:.2f} seconds.", fg="green")

    except ValueError as e:
        status_label.config(text=f"Error: {e}", fg="red")


def on_close():
    """
    Handle application close event.
    """
    sys.exit(0)


# Create the main Tkinter window
root = tk.Tk()
root.title("Ultimate Wordlist Generator")
root.geometry("400x550")
root.resizable(False, False)

# Bind the close event to the custom close function
root.protocol("WM_DELETE_WINDOW", on_close)

# Title Label
title_label = tk.Label(root, text="Ultimate Wordlist Generator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Word Length Range Input
tk.Label(root, text="Enter the range for word length:").pack(pady=5)

length_frame = tk.Frame(root)
length_frame.pack(pady=5)
tk.Label(length_frame, text="Min:").grid(row=0, column=0, padx=5)
min_length_entry = tk.Entry(length_frame, font=("Arial", 12), width=5, justify="center")
min_length_entry.grid(row=0, column=1, padx=5)
tk.Label(length_frame, text="Max:").grid(row=0, column=2, padx=5)
max_length_entry = tk.Entry(length_frame, font=("Arial", 12), width=5, justify="center")
max_length_entry.grid(row=0, column=3, padx=5)

tk.Label(root, text="(e.g., Min: 4, Max: 8)").pack()

# Character Set Options
tk.Label(root, text="Select character sets to include:").pack(pady=10)

lowercase_var = tk.BooleanVar()
uppercase_var = tk.BooleanVar()
numbers_var = tk.BooleanVar()
special_var = tk.BooleanVar()

tk.Checkbutton(root, text="Lowercase letters (a-z)", variable=lowercase_var).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Uppercase letters (A-Z)", variable=uppercase_var).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Numbers (0-9)", variable=numbers_var).pack(anchor="w", padx=20)
tk.Checkbutton(root, text="Special characters (!@#$%^&*)", variable=special_var).pack(anchor="w", padx=20)

# Custom Characters Input
tk.Label(root, text="Enter custom characters (optional):").pack(pady=10)
custom_entry = tk.Entry(root, font=("Arial", 12), justify="center")
custom_entry.pack(pady=5)

# Generate Button
generate_button = tk.Button(root, text="Generate Wordlist", font=("Arial", 14), command=start_generation)
generate_button.pack(pady=20)

# Status Label
status_label = tk.Label(root, text="", font=("Arial", 12))
status_label.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
