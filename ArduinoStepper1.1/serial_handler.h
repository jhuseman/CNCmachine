#ifndef SERIAL_HANDLER_H
#define SERIAL_HANDLER_H
#include <Arduino.h>

#include "axis_list.h"

class SerialHandler {
	private:
		int command_in_buffer_maxlen;
		char *command_in_buffer;
		int command_in_buffer_pos;

		AxisList *axis_list;
		HardwareSerial *command_stream;
	public:
		SerialHandler(int command_in_buffer_maxlen_val, AxisList *axis_list_ref, HardwareSerial *command_stream_ref);
		void run();
};
#endif