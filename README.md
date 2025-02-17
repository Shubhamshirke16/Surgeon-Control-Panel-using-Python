# Surgeon-Control-Panel-using-Python

1) Install Poppines Font on system

2) Install Python (Pre-Installed on raspberry PI)
    a) pi@raspberrypi:~/Downloads $ python --version
        Python 3.9.2
    b) pi@raspberrypi:~/Downloads $ which python
        /usr/bin/python

3) install required Packages of python
    a) pi@raspberrypi:~ $ pip install customtkinter
    b) pi@raspberrypi:~ $ pip install tkcalendar
   
4) Install the ArduinoCLI on raspberry PI use the steps in zip 

5) Run splash.py in application folder( It initialize Arduino Program To arduino)

6) Run main.py in application folder
    
7) Run using terminal
    a) pi@raspberrypi:~ $ /usr/bin/python  /home/pi/application/main.py
    b) pi@raspberrypi:~ $ /usr/bin/python  /home/pi/application/splash.py
 

8) Create two service to run splash.py and main.py Automatically when start Rasberry PI
    I)mainApp.service
    
    a) sudo nano /etc/systemd/system/mainApp.service
    b) copy the following code in service file
*****************************************************************************************************************************************************
[Unit]
Description=Application
After=network.target

[Service]
ExecStart=/usr/bin/python  /home/pi/application/main.py
WorkingDirectory=/home/pi/application
Restart=on-failure
User=pi
Group=pi
Environment=DISPLAY=:0 "XAUTHORITY=/home/pi/.Xauthority"

[Install]
WantedBy=multi-user.target
*****************************************************************************************************************************************************

    c) pi@raspberrypi:~ $ sudo systemctl daemon-reload
    d) pi@raspberrypi:~ $ sudo systemctl enable mainApp.service
        Created symlink /etc/systemd/system/multi-user.target.wants/mainApp.service → /etc/systemd/system/mainApp.service.
    e) pi@raspberrypi:~ $ sudo systemctl start mainApp.service
        (after above cmd output is shown) 



    II)mainApp.service
    
    a) sudo nano /etc/systemd/system/splashApp.service
    b) copy the following code in service file
    
*****************************************************************************************************************************************************    
[Install]
WantedBy=multi-user.target


[Unit]
Description=Application
After=network.target

[Service]
ExecStart=/usr/bin/python  /home/pi/application/splash.py
WorkingDirectory=/home/pi/application
Restart=on-failure
User=pi
Group=pi
Environment=DISPLAY=:0 "XAUTHORITY=/home/pi/.Xauthority"

[Install]
WantedBy=multi-user.target

*****************************************************************************************************************************************************

    c) pi@raspberrypi:~ $ sudo systemctl daemon-reload
    d) pi@raspberrypi:~ $ sudo systemctl enable splashApp.service
        Created symlink /etc/systemd/system/multi-user.target.wants/mainApp.service → /etc/systemd/system/mainApp.service.
    e) pi@raspberrypi:~ $ sudo systemctl start splashApp.service
        (after above cmd output is shown) 


9) Disable Screen blacking and Power Saving(Sleep mode)
     i) sudo nano /etc/lightdm/lightdm.conf
    ii) add following cmd below [Seat:*]

           xserver-command=X -s 0 -dpms
           
10) Disable Notification
    a) Right click on taskbar, go to panel setting
    b) go to second tab, untick show notification
    
           
10) Restart Computer






























































pi@raspberrypi:~ $ pip install customtkinter
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting customtkinter
  Downloading https://www.piwheels.org/simple/customtkinter/customtkinter-5.2.2-py3-none-any.whl (296 kB)
     |████████████████████████████████| 296 kB 206 kB/s 
Collecting darkdetect
  Downloading https://www.piwheels.org/simple/darkdetect/darkdetect-0.8.0-py3-none-any.whl (9.0 kB)
Collecting packaging
  Downloading https://www.piwheels.org/simple/packaging/packaging-24.2-py3-none-any.whl (65 kB)
     |████████████████████████████████| 65 kB 162 kB/s 
Installing collected packages: packaging, darkdetect, customtkinter
Successfully installed customtkinter-5.2.2 darkdetect-0.8.0 packaging-24.2
pi@raspberrypi:~ $ pip install tkcalendar
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Collecting tkcalendar
  Downloading https://www.piwheels.org/simple/tkcalendar/tkcalendar-1.6.1-py3-none-any.whl (40 kB)
     |████████████████████████████████| 40 kB 104 kB/s 
Collecting babel
  Downloading https://www.piwheels.org/simple/babel/babel-2.16.0-py3-none-any.whl (9.6 MB)
     |████████████████████████████████| 9.6 MB 36 kB/s 
Installing collected packages: babel, tkcalendar
  WARNING: The script pybabel is installed in '/home/pi/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
Successfully installed babel-2.16.0 tkcalendar-1.6.1
pi@raspberrypi:~ $ cd ~/Downloads
pi@raspberrypi:~/Downloads $ unzip Poppins.zip
Archive:  Poppins.zip
 extracting: OFL.txt                 
 extracting: Poppins-Thin.ttf        
 extracting: Poppins-ThinItalic.ttf  
 extracting: Poppins-ExtraLight.ttf  
 extracting: Poppins-ExtraLightItalic.ttf  
 extracting: Poppins-Light.ttf       
 extracting: Poppins-LightItalic.ttf  
 extracting: Poppins-Regular.ttf     
 extracting: Poppins-Italic.ttf      
 extracting: Poppins-Medium.ttf      
 extracting: Poppins-MediumItalic.ttf  
 extracting: Poppins-SemiBold.ttf    
 extracting: Poppins-SemiBoldItalic.ttf  
 extracting: Poppins-Bold.ttf        
 extracting: Poppins-BoldItalic.ttf  
 extracting: Poppins-ExtraBold.ttf   
 extracting: Poppins-ExtraBoldItalic.ttf  
 extracting: Poppins-Black.ttf       
 extracting: Poppins-BlackItalic.ttf  
pi@raspberrypi:~/Downloads $ sudo mkdir /usr/share/fonts/truetype/poppins
pi@raspberrypi:~/Downloads $ sudo mv ~/Downloads/*.ttf /usr/share/fonts/truetype/poppins/
pi@raspberrypi:~/Downloads $ sudo fc-cache -fv
/usr/share/fonts: caching, new cache contents: 0 fonts, 6 dirs
/usr/share/fonts/X11: caching, new cache contents: 0 fonts, 3 dirs
/usr/share/fonts/X11/100dpi: caching, new cache contents: 358 fonts, 0 dirs
/usr/share/fonts/X11/encodings: caching, new cache contents: 0 fonts, 1 dirs
/usr/share/fonts/X11/encodings/large: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/X11/util: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cMap: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cmap: caching, new cache contents: 0 fonts, 5 dirs
/usr/share/fonts/cmap/adobe-cns1: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cmap/adobe-gb1: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cmap/adobe-japan1: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cmap/adobe-japan2: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/cmap/adobe-korea1: caching, new cache contents: 0 fonts, 0 dirs
/usr/share/fonts/opentype: caching, new cache contents: 0 fonts, 4 dirs
/usr/share/fonts/opentype/cantarell: caching, new cache contents: 5 fonts, 0 dirs
/usr/share/fonts/opentype/font-awesome: caching, new cache contents: 1 fonts, 0 dirs
/usr/share/fonts/opentype/linux-libertine: caching, new cache contents: 13 fonts, 0 dirs
/usr/share/fonts/opentype/urw-base35: caching, new cache contents: 35 fonts, 0 dirs
/usr/share/fonts/truetype: caching, new cache contents: 0 fonts, 18 dirs
/usr/share/fonts/truetype/crosextra: caching, new cache contents: 8 fonts, 0 dirs
/usr/share/fonts/truetype/dejavu: caching, new cache contents: 22 fonts, 0 dirs
/usr/share/fonts/truetype/droid: caching, new cache contents: 1 fonts, 0 dirs
/usr/share/fonts/truetype/font-awesome: caching, new cache contents: 1 fonts, 0 dirs
/usr/share/fonts/truetype/freefont: caching, new cache contents: 12 fonts, 0 dirs
/usr/share/fonts/truetype/gentium: caching, new cache contents: 4 fonts, 0 dirs
/usr/share/fonts/truetype/gentium-basic: caching, new cache contents: 8 fonts, 0 dirs
/usr/share/fonts/truetype/inconsolata: caching, new cache contents: 1 fonts, 0 dirs
/usr/share/fonts/truetype/lato: caching, new cache contents: 18 fonts, 0 dirs
/usr/share/fonts/truetype/liberation: caching, new cache contents: 16 fonts, 0 dirs
/usr/share/fonts/truetype/liberation2: caching, new cache contents: 12 fonts, 0 dirs
/usr/share/fonts/truetype/libreoffice: caching, new cache contents: 1 fonts, 0 dirs
/usr/share/fonts/truetype/lyx: caching, new cache contents: 12 fonts, 0 dirs
/usr/share/fonts/truetype/noto: caching, new cache contents: 1847 fonts, 0 dirs
/usr/share/fonts/truetype/piboto: caching, new cache contents: 16 fonts, 0 dirs
/usr/share/fonts/truetype/poppins: caching, new cache contents: 18 fonts, 0 dirs
/usr/share/fonts/truetype/quicksand: caching, new cache contents: 4 fonts, 0 dirs
/usr/share/fonts/truetype/ttf-bitstream-vera: caching, new cache contents: 10 fonts, 0 dirs
/usr/share/fonts/type1: caching, new cache contents: 0 fonts, 1 dirs
/usr/share/fonts/type1/urw-base35: caching, new cache contents: 35 fonts, 0 dirs
/usr/local/share/fonts: caching, new cache contents: 0 fonts, 0 dirs
/root/.local/share/fonts: skipping, no such directory
/root/.fonts: skipping, no such directory
/usr/share/fonts/X11: skipping, looped directory detected
/usr/share/fonts/cMap: skipping, looped directory detected
/usr/share/fonts/cmap: skipping, looped directory detected
/usr/share/fonts/opentype: skipping, looped directory detected
/usr/share/fonts/truetype: skipping, looped directory detected
/usr/share/fonts/type1: skipping, looped directory detected
/usr/share/fonts/X11/100dpi: skipping, looped directory detected
/usr/share/fonts/X11/encodings: skipping, looped directory detected
/usr/share/fonts/X11/util: skipping, looped directory detected
/usr/share/fonts/cmap/adobe-cns1: skipping, looped directory detected
/usr/share/fonts/cmap/adobe-gb1: skipping, looped directory detected
/usr/share/fonts/cmap/adobe-japan1: skipping, looped directory detected
/usr/share/fonts/cmap/adobe-japan2: skipping, looped directory detected
/usr/share/fonts/cmap/adobe-korea1: skipping, looped directory detected
/usr/share/fonts/opentype/cantarell: skipping, looped directory detected
/usr/share/fonts/opentype/font-awesome: skipping, looped directory detected
/usr/share/fonts/opentype/linux-libertine: skipping, looped directory detected
/usr/share/fonts/opentype/urw-base35: skipping, looped directory detected
/usr/share/fonts/truetype/crosextra: skipping, looped directory detected
/usr/share/fonts/truetype/dejavu: skipping, looped directory detected
/usr/share/fonts/truetype/droid: skipping, looped directory detected
/usr/share/fonts/truetype/font-awesome: skipping, looped directory detected
/usr/share/fonts/truetype/freefont: skipping, looped directory detected
/usr/share/fonts/truetype/gentium: skipping, looped directory detected
/usr/share/fonts/truetype/gentium-basic: skipping, looped directory detected
/usr/share/fonts/truetype/inconsolata: skipping, looped directory detected
/usr/share/fonts/truetype/lato: skipping, looped directory detected
/usr/share/fonts/truetype/liberation: skipping, looped directory detected
/usr/share/fonts/truetype/liberation2: skipping, looped directory detected
/usr/share/fonts/truetype/libreoffice: skipping, looped directory detected
/usr/share/fonts/truetype/lyx: skipping, looped directory detected
/usr/share/fonts/truetype/noto: skipping, looped directory detected
/usr/share/fonts/truetype/piboto: skipping, looped directory detected
/usr/share/fonts/truetype/poppins: skipping, looped directory detected
/usr/share/fonts/truetype/quicksand: skipping, looped directory detected
/usr/share/fonts/truetype/ttf-bitstream-vera: skipping, looped directory detected
/usr/share/fonts/type1/urw-base35: skipping, looped directory detected
/usr/share/fonts/X11/encodings/large: skipping, looped directory detected
/var/cache/fontconfig: cleaning cache directory
/root/.cache/fontconfig: not cleaning non-existent cache directory
/root/.fontconfig: not cleaning non-existent cache directory
fc-cache: succeeded
pi@raspberrypi:~/Downloads $ python --version
Python 3.9.2
pi@raspberrypi:~/Downloads $ python which
python: can't open file '/home/pi/Downloads/which': [Errno 2] No such file or directory
pi@raspberrypi:~/Downloads $ which python
/usr/bin/python
pi@raspberrypi:~/Downloads $ uname -m
armv7l
pi@raspberrypi:~/Downloads $ sudo mv bin/arduino-cli /usr/local/bin/
mv: cannot stat 'bin/arduino-cli': No such file or directory
pi@raspberrypi:~/Downloads $ sudo mv bin/arduino-cli /usr/local/bin/
mv: cannot stat 'bin/arduino-cli': No such file or directory
pi@raspberrypi:~/Downloads $ sudo mv arduino-cli /usr/local/bin/
mv: cannot stat 'arduino-cli': No such file or directory
pi@raspberrypi:~/Downloads $ sudo mv arduino-cli /usr/local/bin/
mv: cannot stat 'arduino-cli': No such file or directory
pi@raspberrypi:~/Downloads $ sudo mv /home/pi/arduino-cli /usr/local/bin/
pi@raspberrypi:~/Downloads $ cd ..
pi@raspberrypi:~ $ arduino-cli config ini~
Arduino configuration commands.

Usage:
  arduino-cli config [command]

Examples:
  arduino-cli config init

Available Commands:
  add         Adds one or more values to a setting.
  delete      Deletes a settings key and all its sub keys.
  dump        Prints the current configuration
  get         Gets a settings key value.
  init        Writes current configuration to a configuration file.
  remove      Removes one or more values from a setting.
  set         Sets a setting value.

Flags:
  -h, --help   help for config

Global Flags:
      --additional-urls strings   Comma-separated list of additional URLs for the Boards Manager.
      --config-dir string         Sets the default data directory (Arduino CLI will look for configuration file in this directory).
      --config-file string        The custom config file (if not specified the default will be used).
      --json                      Print the output in JSON format.
      --log                       Print the logs on the standard output.
      --log-file string           Path to the file where logs will be written.
      --log-format string         The output format for the logs, can be: text, json (default "text")
      --log-level string          Messages with this level and above will be logged. Valid levels are: trace, debug, info, warn, error, fatal, panic (default "info")
      --no-color                  Disable colored output.

Use "arduino-cli config [command] --help" for more information about a command.
pi@raspberrypi:~ $ arduino-cli config init
Config file written to: /home/pi/.arduino15/arduino-cli.yaml
pi@raspberrypi:~ $ arduino-cli core update-index
Downloading index: library_index.tar.bz2 downloaded                                                                                                                                                                                           
Downloading index: package_index.tar.bz2 downloaded                                                                                                                                                                                           
Downloading missing tool builtin:serial-discovery@1.4.1...
builtin:serial-discovery@1.4.1 downloaded                                                                                                                                                                                                     
Installing builtin:serial-discovery@1.4.1...
Skipping tool configuration....
builtin:serial-discovery@1.4.1 installed
Downloading missing tool builtin:serial-monitor@0.14.1...
builtin:serial-monitor@0.14.1 downloaded                                                                                                                                                                                                      
Installing builtin:serial-monitor@0.14.1...
Skipping tool configuration....
builtin:serial-monitor@0.14.1 installed
Downloading missing tool builtin:ctags@5.8-arduino11...
builtin:ctags@5.8-arduino11 downloaded                                                                                                                                                                                                        
Installing builtin:ctags@5.8-arduino11...
Skipping tool configuration....
builtin:ctags@5.8-arduino11 installed
Downloading missing tool builtin:dfu-discovery@0.1.2...
builtin:dfu-discovery@0.1.2 downloaded                                                                                                                                                                                                        
Installing builtin:dfu-discovery@0.1.2...
Skipping tool configuration....
builtin:dfu-discovery@0.1.2 installed
Downloading missing tool builtin:mdns-discovery@1.0.9...
builtin:mdns-discovery@1.0.9 downloaded                                                                                                                                                                                                       
Installing builtin:mdns-discovery@1.0.9...
Skipping tool configuration....
builtin:mdns-discovery@1.0.9 installed
Downloading index: package_index.tar.bz2 downloaded                                                                                                                                                                                           
pi@raspberrypi:~ $ arduino-cli core install arduino:avr
Downloading packages...
arduino:arduinoOTA@1.3.0 downloaded                                                                                                                                                                                                           
arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7 downloaded                                                                                                                                                                                          
arduino:avrdude@6.3.0-arduino17 downloaded                                                                                                                                                                                                    
arduino:avr@1.8.6 downloaded                                                                                                                                                                                                                  
Installing arduino:arduinoOTA@1.3.0...
Configuring tool....
arduino:arduinoOTA@1.3.0 installed
Installing arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7...
Configuring tool....
arduino:avr-gcc@7.3.0-atmel3.6.1-arduino7 installed
Installing arduino:avrdude@6.3.0-arduino17...
Configuring tool....
arduino:avrdude@6.3.0-arduino17 installed
Installing platform arduino:avr@1.8.6...
Configuring platform....
Platform arduino:avr@1.8.6 installed
pi@raspberrypi:~ $ arduino-cli board list
Port         Protocol Type              Board Name                FQBN             Core
/dev/ttyACM0 serial   Serial Port (USB) Arduino Mega or Mega 2560 arduino:avr:mega arduino:avr
/dev/ttyAMA0 serial   Serial Port       Unknown

pi@raspberrypi:~ $ arduino-cli lib install "RTClib"
Downloading Adafruit BusIO@1.17.0...
Adafruit BusIO@1.17.0 downloaded                                                                                                                                                                                                              
Installing Adafruit BusIO@1.17.0...
Installed Adafruit BusIO@1.17.0
Downloading RTClib@2.1.4...
RTClib@2.1.4 downloaded                                                                                                                                                                                                                       
Installing RTClib@2.1.4...
Installed RTClib@2.1.4
pi@raspberrypi:~ $ pip3 install pyserial
Looking in indexes: https://pypi.org/simple, https://www.piwheels.org/simple
Requirement already satisfied: pyserial in /usr/lib/python3/dist-packages (3.5b0)
pi@raspberrypi:~ $ 


