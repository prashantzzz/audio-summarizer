#run using:
#python -u "c:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\tester.py"

import pyautogui
import time
import pyperclip

for i in range(5):
    print("Testing starting in {}".format(i),end=" > ")
    time.sleep(1)
print()

# Click on the "Choose Audio File" button
choose_audio_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\choose_audio_button.png")  # Replace 'choose_audio_button.png' with the actual image of the button
if choose_audio_btn_pos:
    pyautogui.click(choose_audio_btn_pos)
    print("Choose Audio button found, clicked.")
else: print("Button not found!")
time.sleep(2)


file_path = r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\sample-speech.mp3"  # Path to your audio file
pyautogui.write(file_path)
pyautogui.press('enter')
time.sleep(12)


# Click on the "Summarize" button
# summarize_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\summarize_button.png")  # Replace 'summarize_button.png' with the actual image of the button
# if summarize_btn_pos:
#     pyautogui.click(summarize_btn_pos)
#     print("Choose Audio button found, clicked.")
# else:
#     print("Button not found!")
# time.sleep(12)


# Click on the "Copy" button
copy_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\copy_button.png")  # Replace 'copy_button.png' with the actual image of the button
if copy_btn_pos:
    pyautogui.click(copy_btn_pos)
    print("Choose Audio button found, clicked.")
else:
    print("Choose audio Button not found!")

# Verify that the text has been copied to the clipboard
copied_text = pyperclip.paste()
if copied_text.strip() != "":
    print("Text copied successfully!")
else:
    print("Failed to copy text.")

# Click on the "Means" button
means_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\means_button.png")  # Replace 'means_button.png' with the actual image of the button
if means_btn_pos:
    pyautogui.click(means_btn_pos)
    print("meaning button found, clicked.")
else:
    print("meaning Button not found!")
time.sleep(10)

# Click on the "Read" button
read_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\read_button.png")  # Replace 'read_button.png' with the actual image of the button
if read_btn_pos:
    pyautogui.click(read_btn_pos)
    print("read button found, clicked.")
else:
    print("read Button not found!")
time.sleep(12)

# Click on the "Toggle Mode" button
toggle_mode_btn_pos = pyautogui.locateCenterOnScreen(r"C:\Users\asus\Documents\01-Prashant\Prashant coder\tkinter(pk)\Transcriptor V2.0\toggle_mode_button.png")  # Replace 'toggle_mode_button.png' with the actual image of the button
if toggle_mode_btn_pos:
    pyautogui.click(toggle_mode_btn_pos)
    print("Toggle theme button found, clicked.")
else:
    print("Toggle theme Button not found!")
time.sleep(2)

# Capture screenshot for documentation
pyautogui.screenshot('gui_test_screenshot.png')
