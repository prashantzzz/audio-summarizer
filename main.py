import pyttsx3,logging,os
import tkinter as tk
from tkinter import font as tkFont,filedialog,ttk
import threading,pyperclip
from speech_recognition import Recognizer,AudioFile
from pydub import AudioSegment
from os import path,remove
from transformers import T5Tokenizer, T5ForConditionalGeneration
from PyDictionary import *

dictionary=PyDictionary()

# Configure logging to suppress transformers warnings
logging.getLogger("transformers").setLevel(logging.ERROR)
engine = pyttsx3.init()

on_summary=False #global var to check if already summarized or not when btn is clicked
prev_text="" #saves original text (transcribed text)
current_mode = 0 # Create a variable to track the current mode (0 for dark mode, 1 for light mode)

import os

def audio_to_text():
    global file_extension, on_summary
    on_summary = False
    # Defaults
    audio_file_path = ""
    progress_bar["value"] = 0
    file_label.config(text="X No file selected")
    copy_btn.config(text="Copy")
    summary_btn.config(text="Summarize")
    summary_btn.config(state="disabled")

    # Clear any previous text
    text_display.delete("1.0", tk.END)

    # Open a file dialog to choose an audio file (accepts both MP3 and WAV)
    audio_file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.ogg *.wav")])

    if audio_file_path:
        # Check the file size
        file_size_mb = os.path.getsize(audio_file_path) / (1024 * 1024)  # Convert bytes to MB
        if file_size_mb > 5:
            text_display.insert(tk.END, "Error: Selected audio file is too large (more than 5MB). Please choose a smaller file.")
            return

        progress_bar.start()
        btn.config(state="disabled")
        copy_btn.config(state="disabled")

        text_display.insert(tk.END, "Recognizing...")

        file_label.config(text=path.basename(audio_file_path)[:25] + "...")

        # Determine the file format
        file_extension = audio_file_path.split(".")[-1].lower()
        if file_extension == "mp3":
            # Convert MP3 to WAV
            audio = AudioSegment.from_mp3(audio_file_path)
            wav_file_path = audio_file_path.replace(".mp3", ".wav")
            audio.export(wav_file_path, format="wav")
        elif file_extension == "ogg":
            # Convert OGG to WAV
            audio = AudioSegment.from_ogg(audio_file_path)
            wav_file_path = audio_file_path.replace(".ogg", ".wav")
            audio.export(wav_file_path, format="wav")
        else:
            wav_file_path = audio_file_path

        threading.Thread(target=recognize, args=(wav_file_path,)).start()
        # audio=AudioSegment.from_wav(wav_file_path)
        # audio_duration_ms = len(audio)  # Audio duration in milliseconds
        # current_time_ms = 0
        # while progress_bar["value"] !=100:
        #     progress = (current_time_ms / audio_duration_ms) * 100
        #     progress_bar["value"] = progress
        #     app.update_idletasks()
        #     current_time_ms += 0.5  # Update progress every 1 second
    return

def recognize(wav_file_path):
    # Initialize the recognizer
    global on_summary
    recognizer = Recognizer()
    # Load the WAV audio file
    with AudioFile(wav_file_path) as source:
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)

        # Record the audio data
        audio_data = recognizer.record(source)
        try:
            # Recognize the audio using Google Web Speech API
            text = recognizer.recognize_google(audio_data)
            text_display.delete("1.0", tk.END) #clear 'loading..' text
            text_display.insert(tk.END, text)

            summary_btn.config(state="normal") #summary only works if transcription is sucessful
            on_summary=False
        except:
            text_display.delete("1.0", tk.END) #clear 'loading..' text
            text_display.insert(tk.END, "Error: Couldn't understand the audio!\nCheck you Internet connection")
    progress_bar.stop()
    if file_extension!="wav": remove(wav_file_path)
    btn.config(state="normal")
    copy_btn.config(state="normal")
    return;

def copyit():
    pyperclip.copy(text_display.get("1.0", "end-1c"))
    copy_btn.config(text="Copied!")

def summarize_main(text):
    global on_summary  # Declare on_summary as a global variable
    
    # Load pre-trained T5 model and tokenizer
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    # Tokenize and summarize the text with max_length set to half the original length
    input_ids = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=int(len(text) / 2), truncation=True)
    summary_ids = model.generate(input_ids, max_length=int(len(text) / 2), length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    summary=summary[len(text)+1:] # to remove prev text repitition
    text_display.delete("1.0", tk.END)  # Clear 'summarizing..' text
    text_display.insert(tk.END, summary)
    summary_btn.config(text="Original")
    on_summary = True
    progress_bar.stop()

def summarize():
    global on_summary  # Declare on_summary as a global variable
    global prev_text 
    if not on_summary:
        progress_bar.start()
        prev_text = text_display.get("1.0", "end-1c")
        text_display.delete("1.0", tk.END)  # Clear PREV TEXT text
        text_display.insert(tk.END, "Summarizing...")
        threading.Thread(target=summarize_main, args=(prev_text,)).start()
    elif on_summary:
        text_display.delete("1.0", tk.END)  # Clear prev text text
        text_display.insert(tk.END, prev_text)
        summary_btn.config(text="Summarize")
        on_summary = False

def toggle_mode():
    global current_mode
    if current_mode == 0:
        # Switch to light mode
        app.config(bg="light blue")
        label1.config(bg="light blue", fg="black")
        text_display.config(bg="white", fg="black")
        scrollbar.config(bg="light blue")
        file_label.config(bg="light blue", fg="black")
        btn.config(bg="white", fg="black")
        means_btn.config(bg="white", fg="black")
        copy_btn.config(bg="white", fg="black")
        summary_btn.config(bg="white", fg="black")
        result_label.config(bg="light blue", fg="black")
        toggle_mode_btn.config(bg="white", fg="black")
        save_btn.config(bg="white", fg="black")
        bottom_frame.config(bg="light blue")
        current_mode = 1
    else:
        # Switch to dark mode
        app.config(bg="#1e0847")
        label1.config(bg="#1e0847", fg="white")
        scrollbar.config(bg="#1e0847")
        file_label.config(bg="#1e0847", fg="white")
        
        text_display.config(bg="#332842", fg="white")
        result_label.config(bg="#332842", fg="white")
        save_btn.config(bg="#332842", fg="white")
        btn.config(bg="#332842", fg="white")
        means_btn.config(bg="#332842", fg="white")
        copy_btn.config(bg="#332842", fg="white")
        summary_btn.config(bg="#332842", fg="white")
        toggle_mode_btn.config(bg="#332842", fg="white")
        bottom_frame.config(bg="#332842")
        current_mode = 0

def meaning():
    result_label.config(text="Searching...")
    app.update();
    try: selected_text = text_display.selection_get()
    except: selected_text=''
    if selected_text:
        #meaning = threading.Thread(target=get_meaning, args=(selected_text,)).start()
        meaning=get_meaning(selected_text)
        result_label.config(text=f"Meaning | {meaning}")
    else:
        result_label.config(text="Please select a word.")

def get_meaning(word):
    ans=""
    try: ans="NOUN: "+dictionary.meaning(word)['Noun'][0]
    except: pass
    # try: ans+=" | "+dictionary.meaning(word)['Noun'][1]
    # except: pass
    try: ans+=" VERB: "+dictionary.meaning(word)['Verb'][0]
    except: pass
    # try: ans+=" | "+dictionary.meaning(word)['Verb'][1]
    # except: pass
    if ans: return ans
    return f"Error fetching meaning for {word}!"

def saveit():
    # Ask the user for the file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    # If the user selected a file, save the text to that file
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(text_display.get("1.0", tk.END))

def read_text():
    threading.Thread(target=speak).start()

def speak():
    text_to_read = text_display.get("1.0", tk.END).strip()
    engine.setProperty('rate', 150)  # Speed of speech

    if(text_to_read): engine.say(text_to_read) 
    else: engine.say("Text field is empty.")
    engine.runAndWait()

# Create the main application window
app = tk.Tk()
app.title("Transcriptor and Summarizer")
app.config(bg="light blue")  # Dark grey background color

# Set the icon using the current directory path
current_directory = path.dirname(__file__)
icon_path = path.join(current_directory, "icon.ico")
app.iconbitmap(icon_path)

# Get the screen width and height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate the desired width and height (e.g., 80% of screen width and 60% of screen height)
desired_width = int(screen_width * 0.5) 
desired_height = int(screen_height * 0.55)
# Set the window size and position
app.geometry(f"{desired_width}x{desired_height}+{screen_width//2 - desired_width//2}+{screen_height//2 - desired_height//2}")

custom_font = tkFont.Font(family="Arial", size=12)
bold_font = tkFont.Font(family="Arial", size=12, weight="bold")

# Create a label1 for instructions
label1 = tk.Label(app, bg="light blue", fg="black", text="  Select an audio file (.mp3/ogg/wav) and wait until loading completes!  ", font=bold_font)
label1.pack(pady=15, padx=15)

# Create a frame for 'Save' button and result_label
bottom_frame = tk.Frame(app, bg="lightblue")
bottom_frame.pack(side="bottom", fill="both",padx=10, pady=5)

# Create a 'Save' button
save_btn = tk.Button(bottom_frame,font=custom_font, command=saveit, text="Save", bg="white", fg="black")
save_btn.pack(side="right", padx=5)

# Create meaning label
result_label = tk.Label(bottom_frame, wraplength=desired_width-50, bg="lightblue", fg="black", height=2, justify="left", text="Select word and click 'means'")
result_label.pack(padx=5, fill="both", side="left", anchor="e")


# Create a Text widget with word wrap and vertical scrollbar
text_display = tk.Text(app, font=custom_font, wrap="word", bg="white", fg="black")
text_display.pack(pady=10, padx=15, fill="both", expand=True, side="bottom")
# Create a vertical scrollbar and associate it with the Text widget
scrollbar = tk.Scrollbar(text_display, bg="light blue")
scrollbar.pack(side="right", fill="y")
text_display.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_display.yview, troughcolor="#2C2F30",background="light blue")

# Create a progress bar 
custom_style = ttk.Style()
custom_style.configure("blue.Horizontal.TProgressbar", troughcolor="#2C2F30", background="blue")
progress_bar = ttk.Progressbar(app, mode="indeterminate", length=desired_width, style="blue.Horizontal.TProgressbar")
progress_bar.pack(pady=10, padx=15, side="bottom")

# Create a button to choose the audio file
btn = tk.Button(app, text="Choose Audio File", command=audio_to_text, font=custom_font, bg="white", fg="black")
btn.pack(side="left", padx=15)

# Label for audio file name
file_label = tk.Label(app, text="X No file selected", bg="light blue", fg="black")
file_label.pack(pady=5, side="left")

# Button to copy the text
copy_btn = tk.Button(app, text="Copy", command=copyit, font=custom_font, relief="flat", bg="white", fg="black")
copy_btn.pack(anchor="e", pady=10, padx=10, side="right")

# Button to summarize the text
summary_btn = tk.Button(app, text="Summarize", command=summarize, font=custom_font, relief="flat", bg="white", fg="black", state="disabled")
summary_btn.pack(anchor="e", pady=10, side="right")

# Create a button to toggle between dark and light modes
toggle_mode_btn = tk.Button(app, text="Theme", command=toggle_mode, font=custom_font, relief="flat", bg="white", fg="black")
toggle_mode_btn.pack(anchor="e", pady=10, padx=10, side="right")

# Button to find word meanings
means_btn = tk.Button(app, text="Means", command=meaning, font=custom_font, relief="flat", bg="white", fg="black")
means_btn.pack(anchor="e", pady=10, side="right")

read_btn = tk.Button(app, text="Read", command=read_text, font=custom_font, relief="flat", bg="white", fg="black")
read_btn.pack(anchor="e", pady=10, padx=10, side="right")

# Switch to light mode
current_mode = 1

# Start the GUI main loop
app.mainloop()