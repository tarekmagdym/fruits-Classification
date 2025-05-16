import cv2
import numpy as np
import serial
import time
import pyttsx3  

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  
time.sleep(2)  

engine = pyttsx3.init()

rate = engine.getProperty('rate')
engine.setProperty('rate', 120)  

processing = False

def send_command(command):
    global processing
    command_with_newline = command + '\n'
    arduino.write(command_with_newline.encode())
    print(f"Sent command: {command}")
    processing = True  
    time.sleep(0.1)  

def speak(text):
    engine.say(text)
    engine.runAndWait()

def check_arduino_response():

    global processing
    while arduino.in_waiting:
        response = arduino.readline().decode().strip()
        print(f"Arduino Response: {response}")
        if response == "DONE":  
            processing = False

def detect_objects_by_color(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_orange = np.array([10, 150, 150])   
    upper_orange = np.array([25, 255, 255]) 

    lower_green = np.array([35, 100, 100])  
    upper_green = np.array([85, 255, 255])  

    lower_purple = np.array([120, 100, 100])
    upper_purple = np.array([160, 255, 255])

    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)

    orange_contours, _ = cv2.findContours(orange_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    purple_contours, _ = cv2.findContours(purple_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return orange_contours, green_contours, purple_contours

def main():
    global processing
    cap = cv2.VideoCapture(1)  
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        check_arduino_response()

        if not processing:
            orange_contours, green_contours, purple_contours = detect_objects_by_color(frame)

            if orange_contours:
                largest_orange = max(orange_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_orange) > 1000:  # تجاهل الكائنات الصغيرة
                    x, y, w, h = cv2.boundingRect(largest_orange)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
                    cv2.putText(frame, "Orange Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)

                    send_command("ORANGE")  
                    speak("Orange detected")

            if green_contours:
                largest_green = max(green_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_green) > 1000:  
                    x, y, w, h = cv2.boundingRect(largest_green)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Green Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    send_command("GREEN") 
                    speak("Apple detected")

            if purple_contours:
                largest_purple = max(purple_contours, key=cv2.contourArea)
                if cv2.contourArea(largest_purple) > 1000: 
                    x, y, w, h = cv2.boundingRect(largest_purple)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 0, 128), 2)
                    cv2.putText(frame, "Purple Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 0, 128), 2)

                    send_command("PURPLE")  
                    speak("corrupted object detected") 

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
