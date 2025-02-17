"""
Name of Script: Surgeon Control Panel( OPTHALMIC OT )
Date: 17-JAN-2025
Company Name: Microfilt
Developed By: Nonovid Research
Developer: Shubham Shirke
"""

import customtkinter as ctk
from tkcalendar import Calendar
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import os
import time
from datetime import datetime
import math
import random
import serial

##########################################################################################################################################################

# Configure the serial connection to the Arduino
arduino_port = '/dev/ttyACM0'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
##########################################################################################################################################################

# ALL IMAGE DECLARTION, RESIZE, Conversion
logo_image = ctk.CTkImage(Image.open("/home/pi/application/img/logo.webp"), size=(400, 90))
power_icon = ctk.CTkImage(Image.open("/home/pi/application/img/off.png"), size=(60, 60))  
enabled_image = ctk.CTkImage(Image.open("/home/pi/application/img/pofilgre.png"), size=(40,40))
disabled_image= ctk.CTkImage(Image.open("/home/pi/application/img/pofilora.png"), size=(40,40))
start_image = ctk.CTkImage(Image.open("/home/pi/application/img/start.png"), size=(30, 30))  
stop_image = ctk.CTkImage(Image.open("/home/pi/application/img/pause.png"), size=(30, 30))    
restart_image = ctk.CTkImage(Image.open("/home/pi/application/img/restart.png"), size=(30, 30))  
icon_on = ctk.CTkImage(Image.open("/home/pi/application/img/on.png"), size=(60, 60))  
icon_off = ctk.CTkImage(Image.open("/home/pi/application/img/off.png"), size=(60, 60)) 
icon_humi = ctk.CTkImage(Image.open("/home/pi/application/img/humidity.png"), size=(40, 40))  
icon_temp = ctk.CTkImage(Image.open("/home/pi/application/img/temp.png"), size=(40, 40))  

##########################################################################################################################################################

# Function to toggle UV Light
enabled = False
def uv_toggle():
    global enabled
    if enabled:
        uv_toggle_button.configure(image=icon_off)
        command = f"U\n"
        send_command(command)
    else:
        uv_toggle_button.configure(image=icon_on)
        command = f"U\n"
        send_command(command)

    enabled = not enabled  # Toggle state

##########################################################################################################################################################
    
# Function to show the selected DataTime #It set the date and time On RTC Using Command
def show_selected_time():
    selected_hour = hour_var.get()
    selected_minute = minute_var.get()
    selected_second = second_var.get()
    selected_date_str = cal.get_date()
    
    selected_date=datetime.strptime(selected_date_str,"%m/%d/%y")
    selected_day = selected_date.day
    selected_month = selected_date.month
    selected_year = selected_date.year

    # Check if any field is empty
    if selected_hour == "Hour" or selected_minute == "Minute" or selected_second == "Second" or not selected_date:
        result_label.configure(text="Please select hour, minute, second, and a date.")
    else:
        selected_time = f"Time and Date Updated: {selected_hour}:{selected_minute}:{selected_second} on {selected_date}"
        result_label.configure(text=selected_time)
        print(selected_month)
        user_time=f"{selected_year}-{selected_month:02d}-{selected_day:02d} {selected_hour}:{selected_minute}:{selected_second}"
        
        try:
            # Parse user input to validate format
            dt = datetime.strptime(user_time, "%Y-%m-%d %H:%M:%S")
            # Send formatted time to Arduino
            command = f"T{dt.year}:{dt.month}:{dt.day}:{dt.hour}:{dt.minute}:{dt.second}\n"
            send_command(command)
            print("RTC time set:", command)
        except ValueError:
            print("Invalid time format. Use YYYY-MM-DD HH:MM:SS")        
            
##########################################################################################################################################################

# Function to create the popup window For DATE-TIME SELECTOR
def show_popup():
    popup = ctk.CTkToplevel(app)
    popup.title("Time and Date Selector")
    popup.configure(fg_color='#D5D6D8')
    popup.config(cursor="none")
    # Set the size of the popup
    popup_width = 790
    popup_height = 690
    popup.geometry(f"{popup_width}x{popup_height}")   
    popup.resizable(False, False)
    popup.overrideredirect(True)

    # Center the popup on the screen
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = (screen_width // 2) - (popup_width // 2)
    y = (screen_height // 2) - (popup_height // 2)
    popup.geometry(f"+{x}+{y}")

    # Configure the Combobox style
    style = ttk.Style()
    style.theme_use("default")
    style.configure("CustomCombobox.TCombobox", 
                    foreground="black", 
                    background="white", 
                    bordercolor="black",
                    selectbackground="lightgray",
                    selectforeground="black",
                    font=('Helvetica', 30),  
                    padding=(15, 15))  
    style.map("CustomCombobox.TCombobox", 
              fieldbackground=[("readonly", "white")],
              bordercolor=[("focus", "green")])

    # Dropdown for hours
    global hour_var
    hour_var = tk.StringVar(value="00")
    hour_dropdown = ttk.Combobox(popup, textvariable=hour_var, values=[f"{i:02d}" for i in range(24)], style="CustomCombobox.TCombobox", width=20)
    hour_dropdown.grid(row=0, column=0, padx=30, pady=(60,10))
    hour_dropdown.set("Hour")
    
    # Dropdown for minutes
    global minute_var
    minute_var = tk.StringVar(value="00")
    minute_dropdown = ttk.Combobox(popup, textvariable=minute_var, values=[f"{i:02d}" for i in range(60)], style="CustomCombobox.TCombobox", width=20)
    minute_dropdown.grid(row=0, column=1, padx=10, pady=(60,10))
    minute_dropdown.set("Minute")
    
    # Dropdown for seconds
    global second_var
    second_var = tk.StringVar(value="00")
    second_dropdown = ttk.Combobox(popup, textvariable=second_var, values=[f"{i:02d}" for i in range(60)], style="CustomCombobox.TCombobox", width=20)
    second_dropdown.grid(row=0, column=2, padx=10, pady=(60,10))
    second_dropdown.set("Second")
    
    # Calendar for date selection with fill and border adjustments
    global cal
    cal = Calendar(popup, selectmode='day', 
                   background="lightyellow",
                   disabledbackground="lightgray",
                   bordercolor="blue",
                   headersbackground="lightblue",
                   foreground="black",
                   selectbackground="blue", 
                   selectforeground="white",
                    font=('Helvetica', 20))
    cal.grid(row=1, column=0, columnspan=3, padx=30, pady=(40,20))
    
    button_frame = ctk.CTkFrame(popup, fg_color='#D5D6D8')
    button_frame.grid(row=2, column=0, columnspan=3, padx=0, sticky='nsew')
    
    
    select_button = ctk.CTkButton(button_frame, text="Set Date-Time",height=50,fg_color='#28A745', text_color='#FFFFFF',font=("Poppins Light", 16 ,"bold"), command=show_selected_time)
    select_button.pack(side="left", padx=(220,0), pady=30)
    close_button = ctk.CTkButton(button_frame, text="Close",height=50,fg_color='#FF5252', text_color='#FFFFFF',font=("Poppins Light", 20 ,"bold"), command=popup.destroy)
    close_button.pack(side="right", padx=(0,220), pady=30)
    
    # Label to display the Selected DateTime
    global result_label
    result_label = ctk.CTkLabel(popup, text="", text_color="red", font=("Helvetica", 20))
    result_label.grid(row=3, column=0, columnspan=3, pady=20)
    
    
    popup.grab_set()

##########################################################################################################################################################
    
# Function to send commands to Arduino
def send_command(command):
    ser.write(command.encode())
    
##########################################################################################################################################################

#Function on the One Ambient Light
def One_AbLight_ON(slider, button, slider_index,app):
        s=app.nametowidget(slider)
        b=app.nametowidget(button)
        s.configure(state="normal")
        b.configure(image=enabled_image)
        
########################################################################################################################################################## 
 
# Function to handle slider changes for surgery Light
def slider_surgery_callback(value, slider_number):
    command = f"P{slider_number}:{value}\n"
    send_command(command)
    
##########################################################################################################################################################
    
# Function to toggle the slider state and light for surgery Light
def toggle_surgery_slider(slider, button, slider_index):
    if slider.cget("state") == "normal":
        slider.configure(state="disabled")
        slider.set(0) 
        button.configure(image=disabled_image)  # Change button image to disabled
        
        # Call the slider_callback function with the slider index and value 0
        slider_surgery_callback(0, slider_index)  # Pass 0 value and the correct slider number
        command = f"R{slider_index}\n"
        send_command(command)

    else:
        slider.configure(state="normal")
        button.configure(image=enabled_image)  # Change button image to enabled
        command = f"R{slider_index}\n"
        send_command(command)

##########################################################################################################################################################
        
# Function to handle ambient changes for surgery Light
def slider_ambient_callback(value, slider_number):
    command = f"B{slider_number}:{value}\n"
    send_command(command)

##########################################################################################################################################################

# Function to toggle the slider state and light for ambient Light 
def toggle_ambient_slider(slider, button, slider_index):
    if slider.cget("state") == "normal":
        slider.configure(state="disabled")
        slider.set(0) 
        button.configure(image=disabled_image)  # Change button image to disabled
        
        # Call the slider_callback function with the slider index and value 0
        slider_ambient_callback(0, slider_index)  # Pass 0 value and the correct slider number
        
        sliderAmb=slider_index
        command = f"A{sliderAmb}\n"
        send_command(command)

    else:
        slider.configure(state="normal")
        button.configure(image=enabled_image)  # Change button image to enabled
        sliderAmb=slider_index
        command = f"A{sliderAmb}\n"
        send_command(command)
  
##########################################################################################################################################################
# Function to off light when system shutdown
def off_ambient_shutdown(slider, slider_index):
    if slider.cget("state") == "normal":
        command = f"A{slider_index}\n"
        send_command(command)

    else:
        pass

##########################################################################################################################################################
# Function to off light when system shutdown
def off_surgery_shutdown(slider, slider_index):
    if slider.cget("state") == "normal":
        command = f"R{slider_index}\n"
        send_command(command)

    else:
        pass

##########################################################################################################################################################
def uv_toggle_shutdown():
    global enabled
    if enabled:
        uv_toggle_button.configure(image=icon_off)
        command = f"U\n"
        send_command(command)
    else:
        pass

    enabled = not enabled  # Toggle state
##########################################################################################################################################################
    
# Function to shutdown the Raspberry Pi after confirmation
def confirm_shutdown():
    popup = ctk.CTkToplevel()
    popup.title("Confirm Shutdown")
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
    label = ctk.CTkLabel(popup, text="Are you sure you want to shut down?", font=("Poppins Light", 22 ,"bold"), text_color="#3D3C3C")
    label.pack(pady=(40,0))
    
    # Shutdown function
    def shutdown():
        #function call to off ambient, surgery, UV light when system goes two shutdown
        surgerySlider=[".!ctkframe5.!ctkframe.!ctkslider",".!ctkframe5.!ctkframe2.!ctkslider",".!ctkframe5.!ctkframe3.!ctkslider",".!ctkframe5.!ctkframe4.!ctkslider",".!ctkframe5.!ctkframe5.!ctkslider",".!ctkframe5.!ctkframe6.!ctkslider"]
        for slider_sur_index,slider_sur_path in enumerate(surgerySlider):
            slider=app.nametowidget(slider_sur_path)
            off_surgery_shutdown(slider,slider_sur_index)
            
        ambSlider=[".!ctkframe7.!ctkframe.!ctkslider",".!ctkframe7.!ctkframe2.!ctkslider",".!ctkframe7.!ctkframe3.!ctkslider",".!ctkframe7.!ctkframe4.!ctkslider",".!ctkframe7.!ctkframe5.!ctkslider",".!ctkframe7.!ctkframe6.!ctkslider"]
        for slider_amb_index,slider_amb_path in enumerate(ambSlider):
            slider_amb=app.nametowidget(slider_amb_path)
            off_ambient_shutdown(slider_amb,slider_amb_index)
            
        uv_toggle_shutdown()
        
        os.system("sudo shutdown now")
    
    # Buttons to confirm or cancel
    yes_button = ctk.CTkButton(popup, text="Yes,close it!",height=50,fg_color='#28A745', text_color='#FFFFFF',font=("Poppins Light", 18 ,"bold"), command=lambda: [shutdown(), popup.destroy()])
    yes_button.pack(side="left", padx=(150,0), pady=10)
    
    no_button = ctk.CTkButton(popup, text="Cancel", fg_color='#FF5252',height=50, text_color='#FFFFFF',font=("Poppins Light", 22 ,"bold"), command=popup.destroy)
    no_button.pack(side="right", padx=(0,150), pady=10)
    
    popup.grab_set()
    
##########################################################################################################################################################

# Function to create value with a smaller unit
def create_value_with_unit(parent, value, unit):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)

    # Create the value label and unit label
    value_label = ctk.CTkLabel(frame, text=value, font=("Poppins Regular", 45), text_color="#ECB67F")
    value_label.grid(row=0, column=0, padx=0)

    unit_label = ctk.CTkLabel(frame, text=unit, font=("Poppins Medium", 27), text_color="#ECB67F")
    unit_label.grid(row=0, column=1, padx=0, pady=(2, 0), sticky='w')

    return frame, value_label  # Return the frame and value label

##########################################################################################################################################################

# Function to update values randomly
temp_read=0
humidity_read=0
luminal_read=0
positive_read=0
def update_values():
    global timePart
    global datePart
    global temp_read
    global humidity_read
    global luminal_read
    global positive_read
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            data = line.split(",")
            if data[0] == '@':
                temp_read=float(data[1])
                humidity_read=float(data[2])   
                luminal_read = float(data[3])
                positive_read = float(data[4])
                timePart=data[5].split()[1]
                x=data[5]
                datePart=x.split()[0]
    except Exception:
                print("value Error")
                temp_read=0.0
                humidity_read=0.0  
                luminal_read = 0.0
                positive_read = 0.0

    # Schedule the function to be called again after a set interval (e.g., every 2 seconds)
    app.after(400, update_values) 

##########################################################################################################################################################
listTemp=[]
listHum=[]
listLam=[]
listPos=[]
def update_ev():
    global temp_read
    global humidity_read
    global luminal_read
    global positive_read
    global listTemp
    global listHum
    global listLam
    global listPos
     
     
    temp_cal=(temp_read-175)*0.07973
    if temp_cal > 0:  
        temp_value=int(temp_cal)
    elif temp_cal > 50:
        temp_value=50
    else:
        temp_value=0
        
    listTemp.append(temp_value)
     
     
    humidity_cal=(humidity_read-175)*0.158470
    if humidity_cal > 0:  
        humidity_value=int(humidity_cal)
    elif humidity_cal > 100:
        humidity_value=100
    else:
        humidity_value=0
        
    listHum.append(humidity_value)
      
      
    luminal_cal=(luminal_read-508)*1.4727
    if luminal_cal > 0:  
        luminal_value=int(luminal_cal)
    else:
        luminal_value=0
        
    listLam.append(luminal_value)           
       
       
    positive_cal=positive_read-508
    if positive_cal > 0:  
        positive_value=int(positive_cal)
    else:
        positive_value=0
        
    listPos.append(positive_value)
    
    if len(listTemp)==10:
        TempAvg=round(sum(listTemp)/len(listTemp))  
        HumAvg=round(sum(listHum)/len(listHum))
        LamAvg=round(sum(listLam)/len(listLam))
        if LamAvg <= 8:
            LamAvg=0         
        PosAvg=round(sum(listPos)/len(listPos))
        if PosAvg <= 8:
            PosAvg=0  
        listTemp.clear()
        listHum.clear()
        listLam.clear()
        listPos.clear()
        
        temp_value_label.configure(text=TempAvg)  # Update temperature value
        humidity_value_label.configure(text=HumAvg)  # Update humidity value
        luminal_value_label.configure(text=LamAvg)  # Update luminal pressure value
        positive_value_label.configure(text=PosAvg)  # Update positive pressure value    
 
    # Update the labels every minute
    app.after(450, update_ev)

##########################################################################################################################################################
    
# Function to draw the hands of the clock
timePart="00:00:00"
def update_analog_clock():
    global timePart
    hours,minutes,seconds=map(int,timePart.split(":"))
    # Calculate angles for the clock hands
    hour_angle = (hours + minutes / 60) * 30  # 30 degrees per hour
    minute_angle = (minutes + seconds / 60) * 6  # 6 degrees per minute

    second_angle = seconds * 6  # 6 degrees per second

    # Calculate coordinates for each hand
    second_x = center_x + second_hand_length * math.sin(math.radians(second_angle))
    second_y = center_y - second_hand_length * math.cos(math.radians(second_angle))
    
    minute_x = center_x + minute_hand_length * math.sin(math.radians(minute_angle))
    minute_y = center_y - minute_hand_length * math.cos(math.radians(minute_angle))
    
    hour_x = center_x + hour_hand_length * math.sin(math.radians(hour_angle))
    hour_y = center_y - hour_hand_length * math.cos(math.radians(hour_angle))

    # Update the clock hands
    canvas.coords(second_hand, center_x, center_y, second_x, second_y)
    canvas.coords(minute_hand, center_x, center_y, minute_x, minute_y)
    canvas.coords(hour_hand, center_x, center_y, hour_x, hour_y)

    # Update every 1000 milliseconds (1 second)
    canvas.after(1000, update_analog_clock)

##########################################################################################################################################################
    
# Function to update the date
datePart="2025/01/01"
def update_date():
    global datePart
    try:
        year,month,day=map(int,datePart.split("/"))
    except Exception as e:
        year,month,day=2025,1,1
        print("wrong date format come")
    now=datetime(year,month,day)
    current_day = now.strftime('%a')
    current_date =  now.strftime('%d - %b')
    date_label.configure(text=current_date)
    day_label.configure(text=current_day)
    # Update the labels every minute
    app.after(10000, update_date)

# Function to draw the clock numbers (1 to 12)
def draw_clock_numbers():
    for i in range(1, 13):
        angle = math.radians(i * 30)  # 30 degrees between each number
        # Calculate x and y positions for each number
        x = center_x + (radius - 20) * math.sin(angle)  # Subtract some padding for digits
        y = center_y - (radius - 20) * math.cos(angle)
        canvas.create_text(x, y, text=str(i), font=("Helvetica", 14), fill="WHITE")


##########################################################################################################################################################

# Function to handle the stopwatch functionality
running = False
start_time = 0
elapsed_time = 0

def toggle():
    """Function to start or stop the stopwatch."""
    global running, start_time, elapsed_time
    if running:
        elapsed_time += time.time() - start_time
        stop_resume_button.configure(image=start_image)  # Switch to Resume image
        running = False
    else:
        start_time = time.time()
        stop_resume_button.configure(image=stop_image)  # Switch to Stop image
        running = True
        
##########################################################################################################################################################
        
def reset_timer():
    """Function to reset the stopwatch."""
    global running,start_time, elapsed_time
    running = False
    elapsed_time = 0
    start_time=0
    time_label.configure(text="00:00:00")
    stop_resume_button.configure(image=start_image)  # Reset to Resume image

##########################################################################################################################################################
    
def update_timer():
    """Function to update the time display."""
    if running:
        current_time = time.time() - start_time + elapsed_time
        minutes, seconds = divmod(current_time, 60)
        hours, minutes = divmod(minutes, 60)
        time_label.configure(text=f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}")
    app.after(100, update_timer)



##########################################################################################################################################################
#*************************************************************UI USING Customtkinter**********************************************************************
##########################################################################################################################################################
#Initialize the CustomTkinter app
app = ctk.CTk() 
app.title("Surgeon Control Panel")
app.config(cursor="none")
app.attributes("-fullscreen", True)
app.configure(fg_color='#FFFFFF')

# Configure the grid to ensure equal width for all frames
app.grid_columnconfigure(0, minsize=220, weight=1)  
app.grid_columnconfigure(1, minsize=220, weight=1)  
app.grid_columnconfigure(2, minsize=220, weight=1) 


############################################################ Frame Creation Row 0####################################################################

# Create a frame for each cell of ROW 0
logo_frame = ctk.CTkFrame(app, fg_color='#FFFFFF')
logo_frame.grid(row=0, column=0, padx=0, pady=10, sticky='nsew')

website_frame = ctk.CTkFrame(app, fg_color='#FFFFFF')  
website_frame.grid(row=0, column=1, pady=10, sticky='nsew')

power_frame = ctk.CTkFrame(app, fg_color='#FFFFFF')
power_frame.grid(row=0, column=2, pady=10, sticky='nsew')


############################################################ Add Content To Row 0####################################################################

#First cell: logo
logo_label = ctk.CTkLabel(logo_frame, image=logo_image, text="")
logo_label.pack(pady=10)  

# Second cell: Website name
website_label = ctk.CTkLabel(website_frame, text="www.microfilt.com", font=("Poppins Light", 20), text_color="#3D3C3C", fg_color='#FFFFFF')
website_label.pack(pady=(30,20))

# Third cell: Power button
power_button = ctk.CTkButton(
    power_frame,
    text="", 
    image=power_icon,
    command=confirm_shutdown,
    fg_color='#FFFFFF',  
    hover_color='#F3F1F1' 
)
power_button.pack(padx=20, pady=10)  


############################################################Create A Row and Add Content To Row 1 for Dashboard Tittle########################################

dashtitle = ctk.CTkFrame(app, fg_color='#E7E7E7')
dashtitle.grid(row=1, column=0, columnspan=3, padx=60, pady=(0,10), sticky='ew')

titleLabel = ctk.CTkLabel(dashtitle, text="Surgeon Control Panel", font=("Poppins SemiBold", 36,"bold"), text_color="#3D3C3C", fg_color='#E7E7E7')
titleLabel.pack(pady=15)


######################################################### FRAME creation Row 2 with 3 Column ###############################################################

surgery_lighting = ctk.CTkFrame(app, fg_color='#F3F1F1')
surgery_lighting.grid(row=2, column=0, padx=(60,0), pady=10, sticky='nsew')

OTime = ctk.CTkFrame(app, fg_color='#FFFFFF')
OTime.grid(row=2, column=1, pady=10, sticky='nsew')

ambient_lighting = ctk.CTkFrame(app, fg_color='#F3F1F1')
ambient_lighting.grid(row=2, column=2, pady=10,padx=(0,60), sticky='nsew')


######################################################### SUB FRAME creation for OTTime Frame ###############################################################

top_frame = ctk.CTkFrame(OTime, corner_radius=8, fg_color="#F3F1F1")
top_frame.pack(pady=(0,10)) 

bottom_frame = ctk.CTkFrame(OTime, corner_radius=8, fg_color="#FFFFFF")
bottom_frame.pack(pady=10) 

center_frame21 = ctk.CTkFrame(top_frame, fg_color='#F3F1F1')
center_frame21.pack(pady=10,padx=113)

center_frame22 = ctk.CTkFrame(top_frame, fg_color='#F3F1F1')
center_frame22.pack(pady=10)

# Create two vertical frames (left and right) inside the main frame
left_frame = ctk.CTkFrame(bottom_frame,fg_color="#F3F1F1")
left_frame.grid(row=0, column=0,padx=(20,30), pady=20) 

right_frame = ctk.CTkFrame(bottom_frame,fg_color="#ECB67F")
right_frame.grid(row=0, column=1,padx=(10,30), pady=20) 


######################################################### SURGERY LIGHTING Frame Content Added ###############################################################

# Create Heading Label
sg_label = ctk.CTkLabel(surgery_lighting, text="SURGERY LIGHTING", font=("Poppins Medium", 25), text_color="#3D3C3C")
sg_label.pack(pady=(33,23))

# Create subSurframesArr 
subSurframesArr = []
num_frames = 6  # Number of subSurframesArr to create

# Create Frames and add them to a list
for i in range(num_frames):
    SubSurgeryframe = ctk.CTkFrame(surgery_lighting, fg_color='#F3F1F1')
    SubSurgeryframe.pack(pady=12)
    subSurframesArr.append(SubSurgeryframe)

# Create toggle buttons and sliders for each frame
for index, frame in enumerate(subSurframesArr):

    # Toggle button with images
    sur_toggle_button = ctk.CTkButton(frame, text="", image=disabled_image,  
                                   border_width=0, width=40, height=40,  
                                   fg_color="#F3F1F1", hover_color="#F3F1F1")
    sur_toggle_button.pack(side='left', padx=(0, 20))  

    #slider with custom width and color, initialized to disabled
    surLightSlider = ctk.CTkSlider(frame, from_=0, to=255, 
                                   width=280, 
                                   height=32,
                                   button_color="#ffffff",  
                                   progress_color="#409A94",  
                                   button_hover_color="#ffffff",
                                   fg_color='#ECB67F',
                                   state="disabled",  # Set initial state to disabled
                                   command=lambda value, index=index: slider_surgery_callback(value, index)  # Capture index correctly
                                  )
    surLightSlider.pack(side='left')  
    surLightSlider.set(0)  

    # Set the command for the toggle button after it has been created
    sur_toggle_button.configure(command=lambda s=surLightSlider, b=sur_toggle_button, idx=index: toggle_surgery_slider(s, b, idx))
    

######################################################### OPERATION TIME Frame Content Added ###############################################################
    

OP_label = ctk.CTkLabel(center_frame21, text="OPERATION TIME", font=("Poppins Medium", 25), text_color="#3D3C3C")
OP_label.pack(pady=(20,10))

# Create time display label
time_label = ctk.CTkLabel(center_frame21, text="00:00:00", font=("Arial", 90),text_color="#ECB67F")
time_label.pack(pady=(0,10))

# Create stop/resume button with image, dark background color to match appearance
stop_resume_button = ctk.CTkButton(center_frame22, image=start_image, fg_color="#F3F1F1", text="", width=40, height=40,
                                             border_color="#65B09A", border_width=2,  hover_color="#F3F1F1",command=toggle)
stop_resume_button.pack(side='left',padx=(0,20),pady=(0,10))  # Arranged in a grid

# Create restart button with image, dark background color
restart_button = ctk.CTkButton(center_frame22, image=restart_image, fg_color="#F3F1F1", text="", width=40, height=40,
                                            border_color="#65B09A", border_width=2, hover_color="#F3F1F1", command=reset_timer)
restart_button.pack(side='left',padx=(20,0),pady=(0,10))  # Arranged in a grid

update_timer()

###############################################################################################################################################################

# Create a canvas for the analog clock
canvas = tk.Canvas(left_frame, width=230, height=230, bg="#FFFFFF", highlightthickness=0)
canvas.grid(row=0, column=0)

# Clock center, radius, and hand lengths
center_x, center_y = 115, 115  # Adjusted center for larger canvas
radius = 110
second_hand_length = 60
minute_hand_length = 70
hour_hand_length = 60

# Draw the clock face with a background color
canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="WHITE", width=5, fill="#ECB67F")

# Draw the clock numbers (1 to 12)
draw_clock_numbers()

# Create the hands of the clock
second_hand = canvas.create_line(center_x, center_y, center_x, center_y - second_hand_length,smooth=True, fill="red", width=1)
minute_hand = canvas.create_line(center_x, center_y, center_x, center_y - minute_hand_length, fill="black", width=3)
hour_hand = canvas.create_line(center_x, center_y, center_x, center_y - hour_hand_length, smooth=True, fill="black", width=5)
canvas.create_oval(113, 113, 117, 117, outline="white", width=2, fill="white") 

# Bind the click event to the canvas
canvas.bind("<Button-1>", lambda event: show_popup())

# Create and configure the first label
day_label = ctk.CTkLabel(right_frame, text="", font=("Poppins SemiBold", 40), text_color="WHITE")
day_label.grid(row=0, column=0, padx=25, pady=(15, 0), sticky="nsew")  # Top label

# Create and configure the second label
date_label = ctk.CTkLabel(right_frame, text="", font=("Poppins SemiBold", 40), text_color="WHITE")
date_label.grid(row=1, column=0, padx=25, pady=(0, 15), sticky="nsew")  # Bottom label


#################################################################################################################################################


amb_label = ctk.CTkLabel(ambient_lighting, text="AMBIENT LIGHTING", font=("Poppins Medium", 25), text_color="#3D3C3C")
amb_label.pack(pady=(33,23))

subAmbframesArr = []
num_frames = 6  # Number of frames to create

# Create frames and add them to a list
for i in range(num_frames):
    SubAmbientframe = ctk.CTkFrame(ambient_lighting, fg_color='#F3F1F1')
    SubAmbientframe.pack(pady=12)
    subAmbframesArr.append(SubAmbientframe)

# Create toggle buttons and sliders for each frame
for index, frame in enumerate(subAmbframesArr):
    # Toggle button with images
    amb_toggle_button = ctk.CTkButton(frame, text="", image=disabled_image,  
                                   border_width=0, width=40, height=40,
                                   fg_color="#F3F1F1", hover_color="#F3F1F1")
    amb_toggle_button.pack(side='left', padx=(0, 20))  # Pack to the left

    #slider with custom width and color, initialized to disabled
    amb_light_slider = ctk.CTkSlider(frame, from_=0, to=255, 
                                   width=280, 
                                   height=32,
                                   button_color="#ffffff",  
                                   progress_color="#409A94",  
                                   button_hover_color="#ffffff",
                                   fg_color='#ECB67F',
                                   state="disabled",  # Set initial state to disabled
                                   command=lambda value, index=index: slider_ambient_callback(value, index)  # Capture index correctly
                                  )
    amb_light_slider.pack(side='left')  # Pack to the left
    amb_light_slider.set(0)  # Initialize the slider to zero position

    # Set the command for the toggle button after it has been created
    amb_toggle_button.configure(command=lambda s=amb_light_slider, b=amb_toggle_button, idx=index: toggle_ambient_slider(s, b, idx))


##################################################################Create Frame and Five Subframe For EV of OT #################################################################


main3row = ctk.CTkFrame(app, fg_color='#F3F1F1')
main3row.grid(row=4, column=0, columnspan=3, padx=(60,60), pady=15, sticky='nsew')


# Create a frame to center the content
center_frame31 = ctk.CTkFrame(main3row, fg_color='#FFFFFF')
center_frame31.grid(row=1,column=0,pady=13,padx=28)
# Create a frame to center the content
center_frame32 = ctk.CTkFrame(main3row, fg_color='#FFFFFF')
center_frame32.grid(row=1,column=1,pady=13,padx=28)
# Create a frame to center the content
center_frame33 = ctk.CTkFrame(main3row, fg_color='#FFFFFF')
center_frame33.grid(row=1,column=2,pady=13,padx=28)
# Create a frame to center the content
center_frame34 = ctk.CTkFrame(main3row, fg_color='#FFFFFF')
center_frame34.grid(row=1,column=3,pady=13,padx=28)
# Create a frame to center the content
center_frame35 = ctk.CTkFrame(main3row, fg_color='#FFFFFF')
center_frame35.grid(row=1,column=4,pady=13,padx=28)


########################################################################################################################################################################################

# Add header label for Operation Theater Environment
header_label = ctk.CTkLabel(main3row, text="OPERATION THEATER ENVIRONMENT", font=("Poppins SemiBold", 25), text_color="#2b2b2b")
header_label.grid(row=0, column=0, padx=23, pady=(17,8), columnspan=5)

##########################################################################################################################################################

first_line_frame = ctk.CTkFrame(center_frame31,fg_color='#FFFFFF')
first_line_frame.pack(padx=60, pady=(25,5))

# Create the icon label
icon_label_temp = ctk.CTkLabel(first_line_frame, text="", image=icon_temp)
icon_label_temp.pack(side='left',padx=(0,10))  # Add padding to the right of the icon

# Create the temperature label
temp_label = ctk.CTkLabel(first_line_frame, text="Temperature", font=("Poppins Medium",21), text_color="#3D3C3C")
temp_label.pack(side='left',padx=(10,0))  # Add padding to the left of the temp label

# Create a frame for the second line (temperature value label)
second_line_frame = ctk.CTkFrame(center_frame31,fg_color='#FFFFFF')
second_line_frame.pack(padx=0, pady=(0,10))

# Create the temperature value label with unit
temp_value_with_unit, temp_value_label = create_value_with_unit(second_line_frame, "0", " °C")
temp_value_with_unit.pack(padx=10, pady=10)

######################################################################################################################################################

first_line_frame = ctk.CTkFrame(center_frame32,fg_color='#FFFFFF')
first_line_frame.pack(padx=80, pady=(20,5))

# Create the icon label
icon_label_temp = ctk.CTkLabel(first_line_frame, text="", image=icon_humi)
icon_label_temp.pack(side='left',padx=(0,10))  # Add padding to the right of the icon

# Create the temperature label
humidity_label = ctk.CTkLabel(first_line_frame, text="Humidity", font=("Poppins Medium",21), text_color="#3D3C3C")
humidity_label.pack(side='left',padx=(10,0))  # Add padding to the left of the temp label

# Create a frame for the second line (temperature value label)
second_line_frame = ctk.CTkFrame(center_frame32,fg_color='#FFFFFF')
second_line_frame.pack(padx=0, pady=(0,10))

# Create the temperature value label with unit
humidity_value_with_unit, humidity_value_label = create_value_with_unit(second_line_frame, "0", " %")
humidity_value_with_unit.pack(padx=10, pady=15)

#########################################################################################################################################################

first_line_frame = ctk.CTkFrame(center_frame33,fg_color='#FFFFFF')
first_line_frame.pack(padx=80, pady=22)

# Create the temperature label
uv_label = ctk.CTkLabel(first_line_frame, text="UV Light", font=("Poppins Medium", 21), text_color="#3D3C3C")
uv_label.pack( ) # Add padding to the left of the temp label

# Create a frame for the second line (temperature value label)
second_line_frame = ctk.CTkFrame(center_frame33,fg_color='#FFFFFF')
second_line_frame.pack(padx=0, pady=(0,23))



uv_toggle_button = ctk.CTkButton(second_line_frame, text="", image=icon_off, 
                               border_width=0, width=30, height=30,
                               fg_color="#FFFFFF", hover_color="#FFFFFF", command=uv_toggle)
uv_toggle_button.pack(padx=20) 



#########################################################################################################################################################

first_line_frame = ctk.CTkFrame(center_frame34,fg_color='#FFFFFF')
first_line_frame.pack(padx=60, pady=(25,5))

# Create the icon label
icon_label_temp = ctk.CTkLabel(first_line_frame, text="")
icon_label_temp.pack(side='left',padx=(0,10),pady=(5,0))  # Add padding to the right of the icon

# Create the temperature label
luminal_label = ctk.CTkLabel(first_line_frame, text="Laminar Pressure", font=("Poppins Medium", 21), text_color="#3D3C3C")
luminal_label.pack(side='left',padx=(10,0))  # Add padding to the left of the temp label

# Create a frame for the second line (temperature value label)
second_line_frame = ctk.CTkFrame(center_frame34,fg_color='#FFFFFF')
second_line_frame.pack(padx=0, pady=(0,10))

# Create the temperature value label with unit
luminal_value_with_unit, luminal_value_label = create_value_with_unit(second_line_frame, "0", " Pa")
luminal_value_with_unit.pack(padx=10, pady=(10,15))

#########################################################################################################################################################

first_line_frame = ctk.CTkFrame(center_frame35,fg_color='#FFFFFF')
first_line_frame.pack(padx=60, pady=(25,5))

# Create the icon label
icon_label_temp = ctk.CTkLabel(first_line_frame, text="")
icon_label_temp.pack(side='left',padx=(0,10),pady=(5,0))  # Add padding to the right of the icon

# Create the temperature label
positive_label = ctk.CTkLabel(first_line_frame, text="Positive Pressure", font=("Poppins Medium", 21), text_color="#3D3C3C")
positive_label.pack(side='left',padx=(10,0))  # Add padding to the left of the temp label

# Create a frame for the second line (temperature value label) 
second_line_frame = ctk.CTkFrame(center_frame35,fg_color='#FFFFFF')
second_line_frame.pack(padx=0, pady=(0,10))

# Create the temperature value label with unit
positive_value_with_unit, positive_value_label = create_value_with_unit(second_line_frame, "0", " Pa")
positive_value_with_unit.pack(padx=10, pady=(10,15))

######################################################################################################################################################
#********************************************************Start Running Application********************************************************************
######################################################################################################################################################
update_values()
update_ev()
update_analog_clock()
update_date()
One_AbLight_ON(".!ctkframe7.!ctkframe.!ctkslider",".!ctkframe7.!ctkframe.!ctkbutton",0,app)
app.mainloop() #Run User InterFace in loop

ser.close()