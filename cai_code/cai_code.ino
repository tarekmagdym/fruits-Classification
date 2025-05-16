#include <Servo.h>

Servo base;    // القاعدة
Servo arm;     // الذراع
Servo gripper; // الجريبر

String command = ""; // لتخزين الأوامر المستلمة

void setup() {
  Serial.begin(9600); // بدء الاتصال بالسيريال
  base.attach(9);     // توصيل السيرفو الخاص بالقاعدة بالمنفذ 9
  arm.attach(10);     // توصيل السيرفو الخاص بالذراع بالمنفذ 10
  gripper.attach(11); // توصيل السيرفو الخاص بالجريبر بالمنفذ 11

  // الوضع الابتدائي
  arm.write(90);    // الذراع للأعلى
  gripper.write(0); // الجريبر مغلق
  base.write(90);   // القاعدة في المنتصف
}

void loop() {
  // قراءة الأوامر من السيريال
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') { // عند استقبال السطر بالكامل
      handleCommand(command); // تنفيذ الأمر
      command = "";           // إعادة تعيين النص
    } else {
      command += c; // إضافة الحروف إلى النص
    }
  }
}

void handleCommand(String cmd) {
  if (cmd == "RED") {
    // اللون الأحمر
    base.write(0);      // القاعدة إلى 0°
    arm.write(0);       // الذراع للأسفل
    gripper.write(180); // الجريبر مفتوح
    delay(1000);
  } else if (cmd == "YELLOW") {
    // اللون الأصفر
    base.write(180);    // القاعدة إلى 180°
    arm.write(0);       // الذراع للأسفل
    gripper.write(180); // الجريبر مفتوح
    delay(1000);
  }else if (cmd == "PURPLE") {
    // اللون الأصفر
    base.write(135);    // القاعدة إلى 180°
    arm.write(0);       // الذراع للأسفل
    gripper.write(180); // الجريبر مفتوح
    delay(1000);
  }
  
  else {
    Serial.println("Unknown command"); // طباعة رسالة إذا كان الأمر غير معروف
  }
}
