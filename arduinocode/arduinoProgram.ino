#include <RTClib.h>

#define LAM A13
#define POS A11
#define TEMP A9
#define HUM A15

const int relayPins[6] = {14, 15, 16, 17, 18, 19}; // Digital pins for relays of surgery light
const int pwmPins[6] = {2, 3, 4, 5, 6, 7,}; // PWM-capable pins for surgery light

const int relayPinsAmb[6] = {44, 46, 41, 43, 45, 47}; // Digital pins for relays of ambient Light
const int pwmPinsAmb[6] = {8, 9, 10, 11, 12 ,13}; // PWM-capable pins for ambient Light
RTC_DS3231 rtc;

//Give delay
unsigned long previousMillis = 0;    
const long interval = 1000;

void setup() {
    Serial.begin(9600);

    pinMode(49, OUTPUT);				//Set for UV Light
    digitalWrite(49, LOW);
    
    pinMode(relayPinsAmb[0], OUTPUT);			// Declare for One Ambient Light start Before on
    digitalWrite(relayPinsAmb[0], HIGH);
    pinMode(pwmPinsAmb[0], OUTPUT); 

    for (int i = 0; i < 6; i++) {			// Declare for surgery Lights relay and PWM
        pinMode(relayPins[i], OUTPUT);
        digitalWrite(relayPins[i], LOW);
        pinMode(pwmPins[i], OUTPUT);
    }
    
    for (int i = 1; i < 6; i++) {			// Declare for ambient Lights relay and PWM
        pinMode(relayPinsAmb[i], OUTPUT);
        digitalWrite(relayPinsAmb[i], LOW);
        pinMode(pwmPinsAmb[i], OUTPUT);
    } 
    

    if (!rtc.begin()) {					// check RTC connected or not
        Serial.println("Couldn't find RTC");
        while (1);
    }
}

void loop() {
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');


        // Relay control
        if (command.startsWith("R")) {
            int relayIndex = command.charAt(1) - '0';
            toggleRelay(relayIndex);
        }

        // PWM control
        else if (command.startsWith("P")) {
            int separatorIndex = command.indexOf(':');
            if (separatorIndex > 0) {
                int pwmIndex = command.charAt(1) - '0';
                int pwmValue = command.substring(separatorIndex + 1).toInt();
                setPWM(pwmIndex, pwmValue);
            }
        }


        else if (command.startsWith("A")) {
            int relayIndex = command.charAt(1) - '0';
            toggleRelayAmb(relayIndex);
        }


        // PWM control
        else if (command.startsWith("B")) {
            int separatorIndex = command.indexOf(':');
            if (separatorIndex > 0) {
                int pwmIndex = command.charAt(1) - '0';
                int pwmValue = command.substring(separatorIndex + 1).toInt();
                setPWMAmb(pwmIndex, pwmValue);
            }
        }

	//Togle UV
        else if (command.startsWith("U")) {
            toggleRelayUV();
        }

        
        // RTC time setting
        else if (command.startsWith("T")) {
            setRTCTime(command);
        }
    }

    unsigned long currentMillis = millis();
    if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;
        sendEnvironmentData();
    }
}


void toggleRelay(int index) {
    if (index >= 0 && index < 6) {
        int state = digitalRead(relayPins[index]);
        digitalWrite(relayPins[index], !state);
    }
}


void setPWM(int index, int value) {
    if (index >= 0 && index < 6) {
        analogWrite(pwmPins[index], value);
    }
}


void toggleRelayAmb(int index) {
    if (index >= 0 && index < 6) {
        int state = digitalRead(relayPinsAmb[index]);
        digitalWrite(relayPinsAmb[index], !state);
    }
}


void setPWMAmb(int index, int value) {
    if (index >= 0 && index < 6) {
        analogWrite(pwmPinsAmb[index], value);
    }
}


void toggleRelayUV() {
        int state = digitalRead(49);
        digitalWrite(49, !state);
}


void sendEnvironmentData() {
    float temp = readTEMP();
    float humidity=readHUM();
    float posPressure = readPOS();
    float laminarPressure = readLAM();
    String rtcTime = readRTC();
    
    Serial.print("@"); Serial.print(",");
    Serial.print(temp); Serial.print(",");
    Serial.print(humidity); Serial.print(",");
    Serial.print(laminarPressure); Serial.print(",");
    Serial.print(posPressure); Serial.print(",");
    Serial.println(rtcTime);
}


float readTEMP() {
    float readValue = analogRead(TEMP);
    if(readValue>0)
    {
      return readValue;
      
    }
    else
    {
      return 0;
    }         
}


float readHUM() {
    float readValue = analogRead(HUM);
    if(readValue>0)
    {
      return readValue;
    }
    else
    {
      return 0;
    }
}


float readPOS() {
    float readValue = analogRead(POS);
    if(readValue>0)
    {
      return readValue;
    }
    else
    {
      return 0;
    }
            
}


float readLAM() {
    float readValue = analogRead(LAM);
    if(readValue>0)
    {
      return readValue;
    }
    else
    {
      return 0;
    }
}



String readRTC() {
    DateTime now = rtc.now();
    return String(now.year()) + "/" + String(now.month()) + "/" + String(now.day()) + " " + String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second());
}


void setRTCTime(String command) {
    int parts[6];
    int start = 1;
    int idx = 0;

    for (int i = 1; i < command.length(); i++) {
        if (command.charAt(i) == ':' || i == command.length() - 1) {
            parts[idx++] = command.substring(start, i + 1).toInt();
            start = i + 1;
        }
    }
    DateTime newTime(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]);
    rtc.adjust(newTime);
}

