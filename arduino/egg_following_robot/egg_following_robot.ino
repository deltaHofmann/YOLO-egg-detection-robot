// ==========================================
// HC-SR04
// ==========================================

const int TRIG_PIN = 6;
const int ECHO_PIN = 7;


// ==========================================
// L9110S
// ==========================================

// Linker Motor
const int MOTOR_LEFT_1 = 4;
const int MOTOR_LEFT_2 = 5;

// Rechter Motor
const int MOTOR_RIGHT_1 = 2;
const int MOTOR_RIGHT_2 = 3;


// ==========================================
// Einstellungen
// ==========================================

// Abstand, bei dem der Roboter stoppt
const float STOP_DISTANCE = 4.0;

// Wenn länger als 500 ms kein Befehl
// von Python kommt -> Motoren stoppen
const unsigned long COMMAND_TIMEOUT = 500;


// ==========================================
// Variablen
// ==========================================

char command = 'N';

unsigned long lastCommandTime = 0;


// ==========================================
// Setup
// ==========================================

void setup() {

  Serial.begin(9600);

  // HC-SR04
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  digitalWrite(TRIG_PIN, LOW);

  // Linker Motor
  pinMode(MOTOR_LEFT_1, OUTPUT);
  pinMode(MOTOR_LEFT_2, OUTPUT);

  // Rechter Motor
  pinMode(MOTOR_RIGHT_1, OUTPUT);
  pinMode(MOTOR_RIGHT_2, OUTPUT);

  // Motoren beim Start aus
  stopMotors();

  lastCommandTime = millis();

  Serial.println("Arduino ready");
}


// ==========================================
// Hauptschleife
// ==========================================

void loop() {

  // ========================================
  // Befehl von Python empfangen
  // ========================================

  if (Serial.available() > 0) {

    char incoming = Serial.read();

    if (
      incoming == 'L' ||
      incoming == 'R' ||
      incoming == 'C' ||
      incoming == 'N'
    ) {

      command = incoming;

      lastCommandTime = millis();
    }
  }


  // ========================================
  // Kommunikations-Sicherheitsabschaltung
  // ========================================

  if (
    millis() - lastCommandTime > COMMAND_TIMEOUT
  ) {

    stopMotors();

  }

  else {

    // ======================================
    // Abstand messen
    // ======================================

    float distance = getDistance();


    // ======================================
    // Kein gültiges Echo
    // ======================================

    if (distance <= 0) {

      // Sicherheitshalber stoppen
      stopMotors();

    }


    // ======================================
    // Hindernis zu nah
    // ======================================

    else if (distance < STOP_DISTANCE) {

      stopMotors();

    }


    // ======================================
    // Abstand ist sicher
    // ======================================

    else {

      // ====================================
      // Ei links
      // ====================================

      if (command == 'L') {

        // Rechter Motor fährt
        stopLeftMotor();
        rightMotorForward();

      }


      // ====================================
      // Ei rechts
      // ====================================

      else if (command == 'R') {

        // Linker Motor fährt
        leftMotorForward();
        stopRightMotor();

      }


      // ====================================
      // Ei in der Mitte
      // ====================================

      else if (command == 'C') {

        // Beide Motoren fahren
        leftMotorForward();
        rightMotorForward();

      }


      // ====================================
      // Kein Ei
      // ====================================

      else {

        stopMotors();

      }
    }
  }


  delay(30);
}


// ==========================================
// HC-SR04 Abstand messen
// ==========================================

float getDistance() {

  // Trigger zurücksetzen
  digitalWrite(
    TRIG_PIN,
    LOW
  );

  delayMicroseconds(2);


  // 10 µs Trigger-Puls
  digitalWrite(
    TRIG_PIN,
    HIGH
  );

  delayMicroseconds(10);

  digitalWrite(
    TRIG_PIN,
    LOW
  );


  // Echo messen
  long duration = pulseIn(
    ECHO_PIN,
    HIGH,
    30000
  );


  // Kein Echo
  if (duration == 0) {

    return -1;
  }


  // Umrechnung in cm
  float distance = duration / 58.0;

  return distance;
}


// ==========================================
// Linker Motor vorwärts
// ==========================================

void leftMotorForward() {

  digitalWrite(
    MOTOR_LEFT_1,
    HIGH
  );

  digitalWrite(
    MOTOR_LEFT_2,
    LOW
  );
}


// ==========================================
// Rechter Motor vorwärts
// ==========================================

void rightMotorForward() {

  digitalWrite(
    MOTOR_RIGHT_1,
    HIGH
  );

  digitalWrite(
    MOTOR_RIGHT_2,
    LOW
  );
}


// ==========================================
// Linken Motor stoppen
// ==========================================

void stopLeftMotor() {

  digitalWrite(
    MOTOR_LEFT_1,
    LOW
  );

  digitalWrite(
    MOTOR_LEFT_2,
    LOW
  );
}


// ==========================================
// Rechten Motor stoppen
// ==========================================

void stopRightMotor() {

  digitalWrite(
    MOTOR_RIGHT_1,
    LOW
  );

  digitalWrite(
    MOTOR_RIGHT_2,
    LOW
  );
}


// ==========================================
// Beide Motoren stoppen
// ==========================================

void stopMotors() {

  stopLeftMotor();
  stopRightMotor();
}