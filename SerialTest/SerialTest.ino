void setup() {
  Serial.begin(115200);
}
 
void loop() {
  while(Serial.available()) {
   char incoming = Serial.read();
   Serial.print(incoming);
  }
}