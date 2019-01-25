#ifndef COMMAND_HANDLER_H
#define COMMAND_HANDLER_H
#include <Arduino.h>

#include "axis_list.h"

class CommandHandler {
	private:
		HardwareSerial *out_stream;
		AxisList *axis_list;
	public:
		CommandHandler(HardwareSerial *out_stream_ref, AxisList *axis_list_ref);
		void handle_command(char *command);
};
#endif
