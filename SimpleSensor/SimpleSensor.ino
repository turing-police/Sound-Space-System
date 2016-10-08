/*
 * Simple program to get data from a sound sensor and print it over the serial port.
 */

#include "CurieTimerOne.h"

// Microphone Pin
#define MIC_PIN A0

// Audio sample rate in Hz
#define SAMPLE_RATE 5000

#define SAMPLE_PERIOD 1000000 / SAMPLE_RATE

// Audio buffer size
#define BUFFER_SIZE 2048
uint8_t buff[BUFFER_SIZE];
int buffStart;
int buffEnd;

void readSampleIsr() {
  buff[buffEnd] = analogRead(MIC_PIN);
  buffEnd++;
  if (buffEnd >= BUFFER_SIZE) {
    buffEnd = 0;
  }
}

void setup() {
  int buffStart = 0;
  int buffEnd = 0;

  analogReadResolution(8);

  Serial.begin(250000);
  while (!Serial);

  CurieTimerOne.start(SAMPLE_PERIOD, &readSampleIsr);
}

void loop() {
  noInterrupts();
  int writeEnd = buffEnd;
  interrupts();
  if (writeEnd < buffStart) {
    writeEnd = BUFFER_SIZE;
  }

  if (buffStart + 100 < writeEnd || writeEnd == BUFFER_SIZE) {
    int bytes = Serial.write(buff + buffStart, writeEnd - buffStart);
    buffStart += bytes;
    if (buffStart >= BUFFER_SIZE) {
      buffStart = 0;
    }
  }
}
