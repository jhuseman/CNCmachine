#include "Axis.h"
#include "axis_list.h"
#include "serial_handler.h"
#include "pulse_handler.h"

SerialHandler *serial_handler;
PulseHandler *pulse_handler;

void setup() {
	AxisList *axis_list = new AxisList(8);
	axis_list->add(new Axis('x',7,6,A0,A3,false));
	axis_list->add(new Axis('y',5,4,A1,false));
	axis_list->add(new Axis('z',3,2,A2,false));


	// setup command stream to take in from serial port 0 at baud rate 115200
	HardwareSerial *command_stream = &Serial;
	command_stream->begin(115200);

	serial_handler = new SerialHandler(256, axis_list, command_stream);
	pulse_handler = new PulseHandler(axis_list);
}

void loop() {
	pulse_handler->run();
	serial_handler->run();
}