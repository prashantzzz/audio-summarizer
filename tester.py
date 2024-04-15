import pyautogui
import time
import pyperclip

print("Testing starting in",end="")
for i in range(5):
    print(i,end=" > ")
    time.sleep(1)
print()

def sleep(n):
    print("waiting for",n,"secs")
    time.sleep(n)
def click_image(image_path, message):
    try:
        image_pos = pyautogui.locateCenterOnScreen(image_path)
        if image_pos:
            pyautogui.click(image_pos)
            print(message + " found and clicked.")
        else:
            print(message + " not found!")
    except pyautogui.ImageNotFoundException:
        print("Error: Could not locate the button:",image_path)

# Click on the "Choose Audio File" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\choose_audio_button.png", "Choose Audio button")

# Path to your audio file
file_path = r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\sample-speech.mp3"
time.sleep(1)
pyautogui.write(file_path)
pyautogui.press('enter')
sleep(12)

# Click on the "Copy" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\copy_button.png", "Copy button")

# Verify that the text has been copied to the clipboard
copied_text = pyperclip.paste()
if copied_text.strip() != "":
    print("Text copied successfully:",copied_text)
else:
    print("Failed to copy text.")

# Click on the "Means" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\means_button.png", "Meaning button")
sleep(10)

# Click on the "Read" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\read_button.png", "Read button")
sleep(12)

# Click on the "Summarize" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\summarize_button.png", "Summarize button")
sleep(12)

# Click on the "Toggle Mode" button
click_image(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\theme.png", "Toggle theme button")
time.sleep(2)

# Capture screenshot for documentation
pyautogui.screenshot('gui_test_report.png')
