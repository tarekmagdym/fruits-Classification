#include <Servo.h>

Servo base;    
Servo arm;     
Servo gripper;

String command = ""; 

void setup() {
  Serial.begin(9600); 
  base.attach(9);     
  arm.attach(10);    
  gripper.attach(11);

  arm.write(90);    
  gripper.write(0); 
  base.write(90);  
}

void loop() {
  
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { 
      handleCommand(command); 
      command = "";         
    } else {
      command += c; 
    }
  }
}

void handleCommand(String cmd) {
  if (cmd == "RED") {
    base.write(0);     
    arm.write(0);       
    gripper.write(180); 
    delay(1000);
  } else if (cmd == "YELLOW") {
    // اللون الأصفر
    base.write(180);   
    arm.write(0);      
    gripper.write(180); 
    delay(1000);
  }else if (cmd == "PURPLE") {
    base.write(135);   
    arm.write(0);       
    gripper.write(180); 
    delay(1000);
  }
  
  else {
    Serial.println("Unknown command"); 
  }
}
