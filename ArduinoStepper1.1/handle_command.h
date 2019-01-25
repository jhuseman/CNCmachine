#ifndef HANDLE_COMMAND_H
#define HANDLE_COMMAND_H
#include <Arduino.h>

#include "axis_list.h"

void handle_command(char *command, HardwareSerial *out_stream, AxisList *axis_list);
#endif
