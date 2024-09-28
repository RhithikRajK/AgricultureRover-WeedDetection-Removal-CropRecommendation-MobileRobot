#include <DHT11.h>
#include <Servo.h>
#include <SoftwareSerial.h>
Servo myservo1, myservo2, myservo3;
DHT11 dht11(A0);
int data;
int bluepin = 16;
int motor1_1=2;
int motor1_2=3;
int motor2_1=4;
int motor2_2=5;
int motor3_1=6;
int motor3_2=7;
int motor4_1=8;
int motor4_2=9;
int motore1=10;
int motore2=11;
int motore3=12;
int motore4=13;
int pos=0;
int data1=0;
void setup() {
  Serial.begin(9600);
  pinMode(motor1_1,OUTPUT);
  pinMode(motor1_2,OUTPUT);
  pinMode(motor2_1,OUTPUT);
  pinMode(motor2_2,OUTPUT);
  pinMode(motore1,OUTPUT);
  pinMode(motore2,OUTPUT);
  pinMode(motor3_1,OUTPUT);
  pinMode(motor3_2,OUTPUT);
  pinMode(motor4_1,OUTPUT);
  pinMode(motor4_2,OUTPUT);
  pinMode(motore3,OUTPUT);
  pinMode(motore4,OUTPUT);
  digitalWrite(motore1,HIGH);
  digitalWrite(motore2,HIGH);
  digitalWrite(motore3,HIGH);
  digitalWrite(motore4,HIGH);
  digitalWrite(bluepin,HIGH);
  myservo1.attach(A1);
  myservo2.attach(A2);
  myservo3.attach(A3);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available()>0){
    data=Serial.read();
  }
  while(data==1){
    if(Serial.available()>0){
      data=Serial.read();
    }
    digitalWrite(motor1_1,HIGH);
    digitalWrite(motor1_2,LOW);
    digitalWrite(motor2_1,HIGH);
    digitalWrite(motor2_2,LOW);
    digitalWrite(motor3_1,HIGH);
    digitalWrite(motor3_2,LOW);
    digitalWrite(motor4_1,LOW);
    digitalWrite(motor4_2,HIGH);
  }
  while(data==2){
    if(Serial.available()>0){
      data=Serial.read();
    }
    digitalWrite(motor1_1,HIGH);
    digitalWrite(motor1_2,LOW);
    digitalWrite(motor2_1,HIGH);
    digitalWrite(motor2_2,LOW);
    digitalWrite(motor3_1,LOW);
    digitalWrite(motor3_2,HIGH);
    digitalWrite(motor4_1,HIGH);
    digitalWrite(motor4_2,LOW);
  }
  while(data==3){
    if(Serial.available()>0){
      data=Serial.read();
    }
    digitalWrite(motor1_1,LOW);
    digitalWrite(motor1_2,HIGH);
    digitalWrite(motor2_1,LOW);
    digitalWrite(motor2_2,HIGH);
    digitalWrite(motor3_1,HIGH);
    digitalWrite(motor3_2,LOW);
    digitalWrite(motor4_1,LOW);
    digitalWrite(motor4_2,HIGH);
  }
  while(data==4){
    if(Serial.available()>0){
      data=Serial.read();
    }
    digitalWrite(motor1_1,LOW);
    digitalWrite(motor1_2,HIGH);
    digitalWrite(motor2_1,LOW);
    digitalWrite(motor2_2,HIGH);
    digitalWrite(motor3_1,LOW);
    digitalWrite(motor3_2,HIGH);
    digitalWrite(motor4_1,HIGH);
    digitalWrite(motor4_2,LOW);
  }
  while(data==0){
    if(Serial.available()>0){
      data=Serial.read();
    }
    digitalWrite(motor1_1,LOW);
    digitalWrite(motor1_2,LOW);
    digitalWrite(motor2_1,LOW);
    digitalWrite(motor2_2,LOW);
    digitalWrite(motor3_1,LOW);
    digitalWrite(motor3_2,LOW);
    digitalWrite(motor4_1,LOW);
    digitalWrite(motor4_2,LOW);
  }
  while(data==6){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo1.read();
    pos=pos+1;
    if(pos>45){
      pos=45-1;
    }
    myservo1.write(pos);
    delay(20);
  }
  while(data==7){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo1.read();
    pos=pos-1;
    if(pos<=20){
      pos=pos+1;
    }
    myservo1.write(pos);
    delay(20);
  }
  while(data==8){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo2.read();
    pos=pos+1;
    if(pos>180){
      pos=180-2;
    }
    myservo2.write(pos);
    delay(20);
  }
  while(data==9){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo2.read();
    pos=pos-1;
    if(pos<=0){
      pos=pos+1;
    }
    myservo2.write(pos);
    delay(20);
  }
  while(data==10){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo3.read();
    pos=pos+1;
    if(pos>180){
      pos=180-2;
    }
    myservo3.write(pos);
    delay(20);
  }
  while(data==11){
    if(Serial.available()>0){
      data=Serial.read();
    }
    pos=myservo3.read();
    pos=pos-1;
    if(pos<=0){
      pos=pos+1;
    }
    myservo3.write(pos);
    delay(20);
  }
  if(data==5){
    int hum = dht11.readTemperature();
    int temp = dht11.readHumidity();
    Serial.println("Humidity:");
    Serial.print(hum);
    Serial.println("Temperature:");
    Serial.print(temp);
    delay(300);
  }
}
