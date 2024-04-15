import os
import pyautogui
import time
import pyperclip

for i in range(5,0,-1):
    print("Test starting in",i,">")
    time.sleep(1)

def sleep(n):
    print("waiting for " + str(n) + " secs")
    time.sleep(n)

def click_image(image_path, message):
    try:
        image_pos = pyautogui.locateCenterOnScreen(image_path)
        if image_pos:
            pyautogui.click(image_pos)
            printit(message + " found and clicked ✔")
        else:
            printit(message + " not found! X")
    except pyautogui.ImageNotFoundException:
        printit("X Could not locate: " + os.path.basename(image_path))

def printit(text):
    with open("test_report.txt", "a", encoding="utf-8") as f:
        print(text, file=f)
    print(text)

# Get current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Clear existing content in the test report file
open("test_report.txt", "w").close()

# Click on the "Choose Audio File" button
click_image(os.path.join(current_dir, "choose_audio_button.png"), "Choose Audio button")

# Path to your audio file
file_path = os.path.join(current_dir, "sample-speech.mp3")
time.sleep(1)
pyautogui.write(file_path)
pyautogui.press('enter')
sleep(12)

# Click on the "Copy" button
click_image(os.path.join(current_dir, "copy_button.png"), "Copy button")

# Verify that the text has been copied to the clipboard
copied_text = pyperclip.paste()
if copied_text.strip() != "":
    printit("Text copied successfully: " + copied_text)
else:
    printit("Failed to copy text.")

# Click on the "Means" button
click_image(os.path.join(current_dir, "means_button.png"), "Meaning button")
sleep(10)

# Click on the "Read" button
click_image(os.path.join(current_dir, "read_button.png"), "Read button")
sleep(12)

# Click on the "Summarize" button
click_image(os.path.join(current_dir, "summarize_button.png"), "Summarize button")
sleep(12)

# Click on the "Toggle Mode" button
click_image(os.path.join(current_dir, "theme.png"), "Toggle theme button")
time.sleep(2)

# Print test report saved
print("Test report saved!")
