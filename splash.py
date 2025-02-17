"""
Name of Script: Surgeon Control Panel(common)
Aim: Load the code into arduino if arduino not configure and show splash Screen
Date: 17-JAN-2025
Company Name: Microfilt
Developed By: Nonovid Research
Developer: Shubham Shirke
"""

import customtkinter as ctk
import subprocess
import threading
import os
import time
import serial
from PIL import Image, ImageTk

# Stop Arduino to restart Again and Again
os.system("stty -F /dev/ttyACM0 -hupcl")

logo_image = ctk.CTkImage(Image.open("/home/pi/application/img/logo.webp"), size=(800, 180))

ser=""
def portInitalize():
    global ser
    arduino_port = '/dev/ttyACM0' 
    baud_rate = 9600
    try:
        ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    except serial.SerialException as err:
        label.configure(text="Data Collector are Not Connected.. Please Check the Connection..")


# Function to reboot the Raspberry Pi after confirmation
def confirm_reboot():
    # Create a popup confirmation dialog
    popup = ctk.CTkToplevel()
    popup.title("Confirm Reboot")
    popup.config(cursor="none")
    popup_width = 600
    popup_height =200
    popup.geometry("600x200")
    popup.resizable(False, False)
    popup.overrideredirect(True)

    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    popup.geometry(f"+{x}+{y}")
    
    # Confirmation message label
    label = ctk.CTkLabel(popup, text="Are you sure you want to Reboot?", font=("calibri", 25 ,"bold"), text_color="#3D3C3C")
    label.pack(pady=(30,0))
    
    # Shutdown function
    def reboot():
        os.system("sudo reboot")
    
    # Buttons to confirm or cancel
    yes_button = ctk.CTkButton(popup, text="Yes,close it!",height=50,fg_color='#02BE34', text_color='#FFFFFF',font=("calibri", 19 ,"bold"), command=lambda: [shutdown(), popup.destroy()])
    yes_button.pack(side="left", padx=(150,0), pady=10)
    
    no_button = ctk.CTkButton(popup, text="Cancel", fg_color='RED',height=50, text_color='#FFFFFF',font=("calibri", 22 ,"bold"), command=popup.destroy)
    no_button.pack(side="right", padx=(0,150), pady=10)
    
    popup.grab_set()


# Compile the sketch
def compile_sketch():
    sketch_path = "/home/pi/application/arduinoProgram/arduinoProgram.ino"
    
    board_fqbn = "arduino:avr:mega"                   # Fully Qualified Board Name
    port = "/dev/ttyACM0"                             # Serial port for the Arduino

    print("Compiling the sketch...")
    compile_command = [
        "arduino-cli", "compile",
        "--fqbn", board_fqbn,
        sketch_path
    ]
    result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        print("Compilation successful!")
    else:
        print("Compilation failed:")
        print(result.stderr.decode())
        exit(1)


#This Fuction Upload sketch on arduino
def upload_sketch():
    label.configure(text="Initialising System, please wait...")
    board_fqbn = "arduino:avr:mega"                   # Fully Qualified Board Name
    port = "/dev/ttyACM0"                             # Serial port for the Arduino
    compile_sketch()
    sketch_path = "/home/pi/application/arduinoProgram/arduinoProgram.ino"
    print("Uploading the sketch...")
    upload_command = [
        "arduino-cli", "upload",
        "--fqbn", board_fqbn,
        "--port", port,
        sketch_path
    ]
    result = subprocess.run(upload_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode == 0:
        progress_bar.pack_forget()
        label.configure(text="Initialisation Done, Please Reboot System")
        close_button = ctk.CTkButton(loading_screen, text="Reboot",height=40,fg_color='red', text_color='#FFFFFF',font=("calibri", 22 ,"bold"),command=confirm_reboot)
        close_button.pack(pady=20)

    else:
        print("Upload failed:")
        print(result.stderr.decode())
        exit(1)
        

# Function to check the code on arduino or not. according to this call function upload sketch
def checkSerIN():
    portInitalize() #This Function make serial connection with Raspberry PI
    count=0
    global ser  
    try:
            for count in range (0,5):
                time.sleep(1)
                line = ser.readline().decode('utf-8').strip()
                data = line.split(",")      
                if data[0] == '@':
                    print("Data Come right")
                    break
                else:
                    count+=1
                    if count>4:
                        print("Data Not coming accurate in 5 Sec")
                        upload_sketch()
                        break
                    
            #if ser data is right close the application after 10 sec        
            time.sleep(20)
            loading_screen.after(0, loading_screen.destroy)
    except Exception as e:
        pass
        
    #when arduino not conncted close the application after 10 sec
    time.sleep(10)
    loading_screen.after(0, loading_screen.destroy)

#UI for loading screen
loading_screen = ctk.CTk()
loading_screen.geometry("1920x1080")
loading_screen.attributes("-fullscreen", True)
loading_screen.title("Loading")
loading_screen.config(cursor="none")
loading_screen.configure(fg_color='#FFFFFF')

logo_label = ctk.CTkLabel(loading_screen, image=logo_image, text="")
logo_label.pack(pady=(300,20)) 

label = ctk.CTkLabel(loading_screen, text="Loading, please wait...", font=("Poppins Light", 20), text_color="#000000")
label.pack(pady=(10,0))

progress_bar = ctk.CTkProgressBar(loading_screen, mode="indeterminate", width=400, height=15, progress_color="#ECA44F", fg_color="#E0E0E0")

progress_bar.pack(pady=20, padx=20)
progress_bar.start()


thread = threading.Thread(target=checkSerIN)
thread.daemon = True
thread.start()
loading_screen.mainloop()
# run checkSerIN

