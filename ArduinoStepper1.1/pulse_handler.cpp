#include "pulse_handler.h"

PulseHandler::PulseHandler(AxisList *axis_list_ref) {
	axis_list = axis_list_ref;
	
	max_delay_time = 10000;
	min_delay_time = 100;
}

void PulseHandler::run() {
	unsigned long cur_time = micros(); // currently sending the same time to all axes, to hopefully make them slightly more synchronous with one another
	unsigned long shortest_delay = max_delay_time;
	iter_axes(axis_list, [cur_time, &shortest_delay] (Axis *this_axis) {
		unsigned long this_delay = this_axis->update(cur_time);
		if(this_delay < shortest_delay) {
			shortest_delay = this_delay;
		}
	});
	// if(shortest_delay < min_delay_time) {
	// 	shortest_delay = min_delay_time;
	// }
	unsigned long new_cur_time = micros();
	unsigned long calc_time = new_cur_time - cur_time;
	unsigned long delay_needed = shortest_delay - calc_time;
	if(calc_time > shortest_delay) {
		// delay_needed wrapped around, and we have already waited long enough, so don't delay at all
		delay_needed = 0;
	}
	if(delay_needed > min_delay_time) { // TESTING! Was > 0
		if(delay_needed > 10000) { // if too big of number (greater than 16383), delayMicroseconds is inaccurate, so split to normal delay
			delay(delay_needed/1000);
			// delayMicroseconds(delay_needed%1000);
		} else {
			delayMicroseconds(delay_needed);
		}
	}
}
