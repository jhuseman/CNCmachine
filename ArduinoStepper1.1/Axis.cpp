#include "Axis.h"

Axis::Axis(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, bool reverse_direction_value) {
	init(labelid, pulse_pinid, dir_pinid, ena_pinid, -1, reverse_direction_value);
}

Axis::Axis(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, int rev_dir_pinid, bool reverse_direction_value) {
	init(labelid, pulse_pinid, dir_pinid, ena_pinid, rev_dir_pinid, reverse_direction_value);
}

void Axis::init(char labelid, int pulse_pinid, int dir_pinid, int ena_pinid, int rev_dir_pinid, bool reverse_direction_value) {
	label = labelid;
	pulse_pin = pulse_pinid;
	dir_pin = dir_pinid;
	ena_pin = ena_pinid;
	rev_dir_pin = rev_dir_pinid;
	reverse_direction = reverse_direction_value;
	delay_needed = 0;
	reset_time();
	reset_pos();
	set_speed(0);
	set_pulse_width(pulse_width_default);
	pinMode(pulse_pin, OUTPUT);
	pinMode(dir_pin, OUTPUT);
	pinMode(ena_pin, OUTPUT);
	if(rev_dir_pin>=0) {
		pinMode(rev_dir_pin, OUTPUT);
	}
	digitalWrite(ena_pin, LOW);
}

void Axis::start_pulse() {
	digitalWrite(pulse_pin, HIGH);
	current_output_value = true;
}

void Axis::end_pulse() {
	digitalWrite(pulse_pin, LOW);
	current_output_value = false;
}

void Axis::calc_next(unsigned long cur_time) {
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

char Axis::get_label() {
	return label;
}

unsigned long Axis::update(unsigned long cur_time) {
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
	delay_needed = next_pulse - cur_time;
	return delay_needed;
}

unsigned long Axis::get_delay_needed() {
	return delay_needed;
}

bool Axis::at_target() {
	return target_pos==position;
}

void Axis::reset_time() {
	next_pulse = micros();
}

void Axis::reset_pos() {
	position = 0;
	target_pos = 0;
	direction = false;
	pulse_error_acc = 0;
	current_output_value = false;
}

void Axis::set_speed(unsigned long new_speed) {
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

void Axis::set_target(long new_target_pos) {
	target_pos = new_target_pos;
	direction = (target_pos < position);
	digitalWrite(dir_pin, (direction != reverse_direction));
	if(rev_dir_pin>=0) {
		digitalWrite(rev_dir_pin, (direction == reverse_direction));
	}
}

void Axis::add_to_target(long target_diff) {
	set_target(target_diff+target_pos);
}

void Axis::set_pulse_width(long new_pulse_width) {
	pulse_width = new_pulse_width;
}

void Axis::output_info(HardwareSerial *output_stream) {
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
