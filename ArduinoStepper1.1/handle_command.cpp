#include "handle_command.h"
#include "Axis.h"
#include "cstr2number.h"

void handle_command(char *command, HardwareSerial *out_stream, AxisList *axis_list) {
	char axis_id = 	command[0];
	char action = 	command[1];
	Axis * axis = NULL;
	iter_axes(axis_list, [axis_id, &axis] (Axis *this_axis) {
		if(axis_id==this_axis->get_label()) {
			axis = this_axis;
		}
	});
	if(axis==NULL) { // specified axis is not recognized
		return;
	}
	long val; // used by 's', 'm', 'g', and 'w'
	switch(action) {
		case 's':
			// set speed
			val = cstr2number(&command[2]);
			if(val>=0) {
				axis->set_speed(val);
			}
			break;
		case 'm':
			// move distance
			val = cstr2number(&command[2]);
			axis->add_to_target(val);
			break;
		case 'g':
			// goto location
			val = cstr2number(&command[2]);
			axis->set_target(val);
			break;
		case 'w':
			// set pulse width (duration)
			val = cstr2number(&command[2]);
			if(val>=0) {
				axis->set_pulse_width(val);
			}
			break;
		case 'r':
			// reset position to 0
			axis->reset_pos();
			break;
		case 'q':
			// query information
			out_stream->print("{\"axis\":\""+String(axis_id)+"\",\"params\":");
			axis->output_info(out_stream);
			out_stream->println("}");
			break;
		default:
			// unknown command - ignore
			break;
	}
}
