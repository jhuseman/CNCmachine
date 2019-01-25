#ifndef PULSE_HANDLER_H
#define PULSE_HANDLER_H
#include <Arduino.h>

#include "axis_list.h"

class PulseHandler {
	private:
		unsigned long max_delay_time;
		unsigned long min_delay_time;

		AxisList *axis_list;
	public:
		PulseHandler(AxisList *axis_list_ref);
		void run();
};

#endif