#include "serial_handler.h"

SerialHandler::SerialHandler(int command_in_buffer_maxlen_val, AxisList *axis_list_ref, HardwareSerial *command_stream_ref) {
	axis_list = axis_list_ref;
	command_stream = command_stream_ref;

	command_handler = new CommandHandler(command_stream, axis_list);
	// set command input buffer to an empty string
	command_in_buffer_maxlen = command_in_buffer_maxlen_val;
	command_in_buffer = (char*)malloc(command_in_buffer_maxlen_val*sizeof(char));
	command_in_buffer[0] = '\0';
	command_in_buffer_pos = 0;
}
void SerialHandler::run() {
	// read data from serial port, if available
	if(command_stream->available()) {
		char current_inbyte = char(command_stream->read());
		if(current_inbyte=='\n') {
			// handle the command
			command_handler->handle_command(command_in_buffer);
			// clear the buffer
			command_in_buffer[0] = '\0';
			command_in_buffer_pos = 0;
		} else {
			// save the received byte in the buffer
			command_in_buffer[command_in_buffer_pos] = current_inbyte;
			// increment position variable and null-terminate the string
			command_in_buffer_pos++;
			// check to make sure string isn't too long
			while(command_in_buffer_pos>=command_in_buffer_maxlen) {
				command_in_buffer_pos--;
			}
			// null-terminate string
			command_in_buffer[command_in_buffer_pos] = '\0';
		}
	}
}
