import pyautogui
import time

def send_to_cursor(command_string):
    # This is a basic example. You'll likely need to adjust these steps.
    # On macOS, you might need to grant accessibility permissions for pyautogui.

    # 1. Bring Cursor to the front (this is a common challenge for UI automation)
    # This might vary based on your OS and how Cursor registers its window title.
    # You might have to manually click on Cursor to activate it before running.
    # A more robust solution might involve:
    # try:
    #     cursor_window = pyautogui.getWindowsWithTitle('Cursor')[0] # Find by title
    #     if cursor_window:
    #         cursor_window.activate() # Bring to front
    #         time.sleep(0.5)
    # except IndexError:
    #     print("Cursor window not found. Please ensure Cursor is open and visible.")
    #     return

    print("Please make sure Cursor is the active window before proceeding.")
    time.sleep(3) # Give yourself time to switch to Cursor manually

    # 2. Assume the chat input field is already focused, or you can click a known coordinate.
    # If you know the exact coordinates of your chat input box, you could use:
    # pyautogui.click(x=100, y=900) # Example coordinates - YOU WILL NEED TO CHANGE THESE
    # For now, we'll just assume the text field is ready to receive input.

    # 3. Type the command
    pyautogui.write(command_string)

    # 4. Press Enter to send the command
    pyautogui.press('enter')

# Your program's logic to decide the command
command_for_cursor = "Please create a file named 'automated_pyautogui_hello.txt' with the content 'Hello from PyAutoGUI automation!'"

send_to_cursor(command_for_cursor)