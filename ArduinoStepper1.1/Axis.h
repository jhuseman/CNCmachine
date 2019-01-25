#ifndef AXIS_H
#define AXIS_H
#include <Arduino.h>
const float catchup_delay_threshold = 0.125; // how far behind (fraction of period) the timer can get before skipping a tick (under-speed)
const unsigned long pulse_width_default = 100; // pulse width to set as the default on boot - can be changed over serial port

class Axis {
	private:
		char label;
		// used to determine how to output a pulse
		int pulse_pin, dir_pin, ena_pin, rev_dir_pin;
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
		unsigned long delay_needed;
		// used to keep track of how much rounding error there is from the specified speed
		unsigned long pulse_error;
		unsigned long pulse_error_acc;
		unsigned long speed;

		void init(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, int rev_dir_pinid, bool reverse_direction_value);

		void start_pulse();
		void end_pulse();
		void calc_next(unsigned long cur_time);
	public:
		Axis(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, bool reverse_direction_value);
		Axis(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, int rev_dir_pinid, bool reverse_direction_value);
		char get_label();
		unsigned long update(unsigned long cur_time);
		unsigned long get_delay_needed();
		bool at_target();
		void reset_time();
		void reset_pos();
		void set_speed(unsigned long new_speed);
		void set_target(long new_target_pos);
		void add_to_target(long target_diff);
		void set_pulse_width(long new_pulse_width);
		void output_info(HardwareSerial *output_stream);
};
#endif