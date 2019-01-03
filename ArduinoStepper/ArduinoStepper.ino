HardwareSerial *command_stream;
const float catchup_delay_threshold = 0.125; // how far behind (fraction of period) the timer can get before skipping a tick (under-speed)
const int command_in_buffer_maxlen = 256; // size of buffer for commands received over serial
const unsigned long pulse_width_default = 100; // pulse width to set as the default on boot - can be changed over serial port
char command_in_buffer[command_in_buffer_maxlen];
int command_in_buffer_pos;

class Axis {
	private:
		// used to determine how to output a pulse
		int pulse_pin, dir_pin;
		bool reverse_direction;
		bool current_output_value;
		// used to keep track of current position
		long position;
		long target_pos;
		bool direction; // true if needs to move backwards (negative direction)
		// used to determine how long to wait until next pulse
		unsigned long pulse_spacing;
		unsigned long next_pulse;
		unsigned long end_pulse_time;
		unsigned long pulse_width;
		unsigned long catchup_threshold;
		// used to keep track of how much rounding error there is from the specified speed
		unsigned long pulse_error;
		unsigned long pulse_error_acc;
		unsigned long speed;


		void start_pulse() {
			digitalWrite(pulse_pin, HIGH);
			current_output_value = true;
		}

		void end_pulse() {
			digitalWrite(pulse_pin, LOW);
			current_output_value = false;
		}

		void calc_next(unsigned long cur_time) {
			unsigned long prev_pulse = next_pulse;
			if((cur_time-prev_pulse) > catchup_threshold) {
				prev_pulse = cur_time;
			}
			next_pulse = prev_pulse + pulse_spacing;
			pulse_error_acc += pulse_error;
			if(pulse_error_acc >= speed) {
				pulse_error_acc-= speed;
				next_pulse += pulse_error;
			}
			if(direction) {
				position--;
			} else {
				position++;
			}
		}
	public:
		Axis(int pulse_pinid, int dir_pinid, bool reverse_direction_value) {
			pulse_pin = pulse_pinid;
			dir_pin = dir_pinid;
			reverse_direction = reverse_direction_value;
			reset_time();
			reset_pos();
			set_speed(0);
			set_pulse_width(pulse_width_default);
			pinMode(pulse_pin, OUTPUT);
			pinMode(dir_pin, OUTPUT);
		}

		unsigned long update(unsigned long cur_time) {
			// returns maximum length of delay to wait until next call to this function, or 0 for ASAP
			if(current_output_value) {
				if(cur_time >= end_pulse_time) {
					end_pulse();
					if(cur_time >= next_pulse) {
						return 0;
					}
				} else {
					return end_pulse_time - cur_time;
				}
			}
			if(pulse_spacing==0 || at_target()) {
				return 1000000L; // default to once per second when at zero speed
			}
			if(cur_time >= next_pulse) {
				start_pulse();
				end_pulse_time = cur_time + pulse_width;
				calc_next(cur_time);
				return 0;
			}
			return next_pulse - cur_time;
		}

		bool at_target() {
			return target_pos==position;
		}

		void reset_time() {
			next_pulse = micros();
		}

		void reset_pos() {
			position = 0;
			target_pos = 0;
			direction = false;
			pulse_error_acc = 0;
			current_output_value = false;
		}

		void set_speed(unsigned long new_speed) {
			speed = new_speed;
			if(speed==0) {
				pulse_spacing = 0;
				pulse_error = 0;
			} else {
				unsigned long prev_pulse = next_pulse - pulse_spacing;
				pulse_spacing = 1000000L / speed;
				pulse_error = 1000000L - (pulse_spacing * speed);
				next_pulse = prev_pulse + pulse_spacing;
			}
			catchup_threshold = catchup_delay_threshold * pulse_spacing;
		}

		void set_target(long new_target_pos) {
			target_pos = new_target_pos;
			direction = (target_pos < position);
			digitalWrite(dir_pin, (direction != reverse_direction));
		}

		void add_to_target(long target_diff) {
			set_target(target_diff+target_pos);
		}

		void set_pulse_width(long new_pulse_width) {
			pulse_width = new_pulse_width;
		}

		void output_info(HardwareSerial *output_stream) {
			output_stream->print("{\"pulse_pin\":"+				String(pulse_pin)+",");
			output_stream->print("\"dir_pin\":"+				String(dir_pin)+",");
			output_stream->print("\"reverse_direction\":"+		String(reverse_direction)+",");
			output_stream->print("\"current_output_value\":"+	String(current_output_value)+",");
			output_stream->print("\"position\":"+				String(position)+",");
			output_stream->print("\"target_pos\":"+				String(target_pos)+",");
			output_stream->print("\"direction\":"+				String(direction)+",");
			output_stream->print("\"pulse_spacing\":"+			String(pulse_spacing)+",");
			output_stream->print("\"next_pulse\":"+				String(next_pulse)+",");
			output_stream->print("\"end_pulse_time\":"+			String(end_pulse_time)+",");
			output_stream->print("\"pulse_width\":"+			String(pulse_width)+",");
			output_stream->print("\"catchup_threshold\":"+		String(catchup_threshold)+",");
			output_stream->print("\"pulse_error\":"+			String(pulse_error)+",");
			output_stream->print("\"pulse_error_acc\":"+		String(pulse_error_acc)+",");
			output_stream->print("\"speed\":"+					String(speed)+",");
			output_stream->print("\"cur_time\":"+				String(micros())+"}");
		}
};

const int num_axes = 3;
Axis *axes[num_axes];
char axes_labels[num_axes];
unsigned long axes_delays[num_axes];

long cstr2number(char *num) {
	switch(num[0]) {
		case '-':
			return -1*cstr2number(&num[1]);
		case '+':
			return cstr2number(&num[1]);
		default:
			return String(num).toInt();
	}
}

void handle_command(char *command) {
	char axis_id = 	command[0];
	char action = 	command[1];
	Axis * axis = NULL;
	for(int i=0;i<num_axes;i++) {
		if(axis_id==axes_labels[i]) {
			axis = axes[i];
		}
	}
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
			command_stream->print("{\"axis\":\""+String(axis_id)+"\",\"params\":");
			axis->output_info(command_stream);
			command_stream->println("}");
			break;
		default:
			// unknown command - ignore
			break;
	}
}

void handle_serial() {
	// read data from serial port, if available
	if(command_stream->available()) {
		char current_inbyte = char(command_stream->read());
		if(current_inbyte=='\n') {
			// handle the command
			handle_command(command_in_buffer);
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

const unsigned long max_delay_time = 10000;
const unsigned long min_delay_time = 100;

void handle_pulses() {
	unsigned long cur_time = micros(); // currently sending the same time to all axes, to hopefully make them slightly more synchronous with one another
	unsigned long shortest_delay = max_delay_time;
	for(int i=0; i<num_axes; i++) {
		unsigned long this_delay = axes[i]->update(cur_time);
		axes_delays[i] = this_delay;
		if(this_delay < shortest_delay) {
			shortest_delay = this_delay;
		}
	}
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

void setup() {
	// setup command stream to take in from serial port 0 at baud rate 115200
	command_stream = &Serial;
	command_stream->begin(115200);
	// set command input buffer to an empty string
	command_in_buffer[0] = '\0';
	command_in_buffer_pos = 0;

	axes_labels[0] = 	'x';
	axes[0] = 			new Axis(13,12,false);
	axes_labels[1] = 	'y';
	axes[1] = 			new Axis(11,10,false);
	axes_labels[2] = 	'z';
	axes[2] = 			new Axis(9,8,false);
	for(int i=0; i<num_axes; i++) {
		axes_delays[i] = 0;
	}
}

void loop() {
	handle_pulses();
	handle_serial();
}