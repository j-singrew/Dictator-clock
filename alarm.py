import tkinter as tk
from tkinter import messagebox
import datetime
import time
import threading
from playsound import playsound
import pyttsx3

# ---------------------------
# Global variables
# ---------------------------
alarm_thread = None
alarm_running = False

# ---------------------------
# Text-to-speech function
# ---------------------------
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.say(text)
    engine.runAndWait()

# ---------------------------
# Function to update the live clock
# ---------------------------
def update_clock():
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    clock_label.after(1000, update_clock)  # refresh every second
    update_countdown()  # update countdown as well

# ---------------------------
# Function to check alarm time in background
# ---------------------------
def check_alarm(alarm_time):
    global alarm_running
    while alarm_running:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            speak("Wake up! It's time!")
            try:
                playsound("alarm.mp3")
            except:
                messagebox.showerror("Error", "Could not play alarm sound.")
            messagebox.showinfo("Alarm", "⏰ WAKE UP! It's time!")
            alarm_running = False
            stop_button.config(state="disabled")
            break
        time.sleep(5)

# ---------------------------
# Function to start the alarm
# ---------------------------
def set_alarm():
    global alarm_running, alarm_thread
    alarm_time = entry.get()

    # Validate input
    try:
        datetime.datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        messagebox.showwarning("Format Error", "Please use HH:MM format (24-hour).")
        return

    alarm_running = True
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")
    speak(f"Alarm set for {alarm_time}")
    stop_button.config(state="normal")

    # Start checking in background
    alarm_thread = threading.Thread(target=check_alarm, args=(alarm_time,), daemon=True)
    alarm_thread.start()

# ---------------------------
# Function to stop the alarm
# ---------------------------
def stop_alarm():
    global alarm_running
    alarm_running = False
    stop_button.config(state="disabled")
    speak("Alarm stopped.")
    messagebox.showinfo("Stopped", "Alarm has been stopped.")

# ---------------------------
# Countdown display
# ---------------------------
def update_countdown():
    alarm_time = entry.get()
    try:
        target = datetime.datetime.strptime(alarm_time, "%H:%M").time()
        now = datetime.datetime.now().time()
        # Convert to seconds since midnight
        now_sec = now.hour * 3600 + now.minute * 60 + now.second
        target_sec = target.hour * 3600 + target.minute * 60
        remaining = target_sec - now_sec
        if remaining < 0:
            remaining += 86400  # next day
        hrs = remaining // 3600
        mins = (remaining % 3600) // 60
        secs = remaining % 60
        countdown_label.config(text=f"Time remaining: {hrs:02d}:{mins:02d}:{secs:02d}")
    except:
        countdown_label.config(text="Time remaining: --:--:--")

# ---------------------------
# GUI setup
# ---------------------------
root = tk.Tk()
root.title("Advanced Python Alarm Clock")
root.geometry("400x320")
root.resizable(False, False)
root.configure(bg="#101820")

# Digital clock label
clock_label = tk.Label(root, text="", font=("Arial", 50, "bold"), fg="#FEE715", bg="#101820")
clock_label.pack(pady=15)

# Alarm entry
tk.Label(root, text="Set Alarm (HH:MM, 24-hour format)", font=("Arial", 12), fg="white", bg="#101820").pack()
entry = tk.Entry(root, font=("Arial", 16), justify='center')
entry.pack(pady=10)

# Countdown label
countdown_label = tk.Label(root, text="Time remaining: --:--:--", font=("Arial", 12), fg="#FEE715", bg="#101820")
countdown_label.pack(pady=5)

# Buttons
button_frame = tk.Frame(root, bg="#101820")
button_frame.pack(pady=10)

set_button = tk.Button(button_frame, text="Set Alarm", command=set_alarm,
                       font=("Arial", 12, "bold"), bg="#FEE715", fg="#101820", width=12)
set_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Stop Alarm", command=stop_alarm,
                        font=("Arial", 12, "bold"), bg="#FF4C4C", fg="white", width=12, state="disabled")
stop_button.grid(row=0, column=1, padx=10)

# Start clock
update_clock()

# Main loop
root.mainloop()
