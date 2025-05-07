import tkinter as tk
from tkinter import messagebox

METADATA = {
    "inputs": {
        "message": "Message to display in the message box",
    }
}

def main(inputs):
    """
    Main function to show a message box with the provided message.

    Args:
        inputs (dict): A dictionary containing the input variables.
            - message (str): The message to display in the message box.

    Returns:
        None
    """


    # Create a simple Tkinter window to use as a parent for the message box
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get the message from inputs
    message = inputs.get("message", "No message provided")

    # Show the message box
    messagebox.showinfo("Message", message)

    # Destroy the root window after showing the message box
    root.destroy()
