#! /usr/bin/env python

#%% import modules
import sys
import time
import json
import math

import gcode_split
import units

#%% define class
class MovementStep(object):
	def __init__(self, speed=None, x=None, y=None, z=None, relative=False, units='m', action='move', prev_status={}, calibration_info={}):
		self.speed = speed
		self.x = x
		self.y = y
		self.z = z
		self.relative = relative
		self.units = units
		self.action = action # an "action" to perform in the command - currently unused, but can be utilized later to do special commands like pulse width adjustment, resetting position counters, or forcing a status dump
		self.prev_status = prev_status.copy()
		self.calibration_info = calibration_info
		# calculate relative position
		if self.relative:
			self.dx = self.x
			self.dy = self.y
			self.dz = self.z
		else:
			self.dx = self.x - self.prev_status['Xpos']
			self.dy = self.y - self.prev_status['Ypos']
			self.dz = self.z - self.prev_status['Zpos']

		# parameters used by query_status when having to estimate the position from elapsed time
		self.start_clock_time = None
		self.duration = None
	
	def run(self, out_stream=sys.stdout, in_stream=None, time_manager=time, stat_store=None):
		commands = []
		move_dist = math.sqrt(self.dx*self.dx + self.dy*self.dy + self.dz*self.dz)
		xpulses = units.convert_to_pulses(self.dx, self.calibration_info['x'], self.units)
		ypulses = units.convert_to_pulses(self.dy, self.calibration_info['y'], self.units)
		zpulses = units.convert_to_pulses(self.dz, self.calibration_info['z'], self.units)
		if self.speed==0 or move_dist==0:
			self.duration = 0
			xspeed = 0
			yspeed = 0
			zspeed = 0
		else:
			self.duration = move_dist/float(self.speed)
			xspeed = abs(int(xpulses/self.duration))
			yspeed = abs(int(ypulses/self.duration))
			zspeed = abs(int(zpulses/self.duration))
		if xpulses!=0:
			commands.append('xs{}'.format(xspeed))
		if ypulses!=0:
			commands.append('ys{}'.format(yspeed))
		if zpulses!=0:
			commands.append('zs{}'.format(zspeed))
		if xpulses!=0:
			commands.append('xm{}'.format(xpulses))
		if ypulses!=0:
			commands.append('ym{}'.format(ypulses))
		if zpulses!=0:
			commands.append('zm{}'.format(zpulses))
		for com in commands:
			print(com) #DEBUG
			out_stream.write(com)
			out_stream.write('\n')
		out_stream.flush()
		self.start_clock_time = time_manager.clock()
		# wait for command to finish
		max_delay = 0.05
		delay_needed = 0.001
		while delay_needed > 0:
			status = self.query_status(out_stream=out_stream, in_stream=in_stream, time_manager=time_manager)
			if not stat_store is None:
				stat_store.update(status, time_manager.clock())
			min_prog = status['min_progress']
			delay_needed = (1-min_prog)*self.duration
			delay_needed = delay_needed*0.95 # shorten delay slightly
			if delay_needed > max_delay:
				delay_needed = max_delay
			if delay_needed>0:
				time_manager.sleep(delay_needed)
	
	def query_status(self, out_stream=sys.stdout, in_stream=None, time_manager=time):
		if in_stream is None:
			cur_time = time_manager.clock()
			dur_so_far = cur_time - self.start_clock_time
			fraction = float(dur_so_far)/self.duration
			ret = {
				'axes': {},
				'max_progress':fraction,
				'min_progress':fraction,
				'avg_progress':fraction,
			}
			for axis in ['x','y','z']:
				start_pos = self.prev_status['{}pos'.format(axis.upper())]
				tot_change = getattr(self,'d{}'.format(axis))
				target_pos = start_pos + tot_change
				cur_position = start_pos + tot_change*fraction
				tot_pulses = units.convert_to_pulses(tot_change, self.calibration_info[axis], self.units)
				pulses_so_far = tot_pulses*fraction
				if tot_pulses==0:
					pulse_spacing = 0
					cur_pulse_progress = 1
				else:
					pulse_spacing = self.duration/tot_pulses
					cur_pulse_progress = dur_so_far%pulse_spacing
				next_pulse = cur_time+pulse_spacing*(1-cur_pulse_progress)
				pulse_width = 0.0001

				ret['axes'][axis] = {
					"pulse_pin":None,
					"dir_pin":None,
					"reverse_direction":None,
					"current_output_value":None,
					"position":units.convert_to_pulses(cur_position, self.calibration_info[axis], self.units),
					"target_pos":units.convert_to_pulses(target_pos, self.calibration_info[axis], self.units),
					"direction":{False:0,True:1}[(tot_change<0)],
					"pulse_spacing":pulse_spacing*1000000,
					"next_pulse":next_pulse*1000000,
					"end_pulse_time":(next_pulse-pulse_spacing+pulse_width)*1000000,
					"pulse_width":pulse_width*1000000,
					"catchup_threshold":None,
					"pulse_error":0,
					"pulse_error_acc":0,
					"speed":units.convert_to_pulses(self.speed, self.calibration_info[axis], self.units),
					"cur_time":cur_time*1000000,
					'pulses_left':int(tot_pulses-pulses_so_far),
					'cur_pulse_progress':cur_pulse_progress,
					'progress':fraction,
				}
			return ret
		else:
			out_stream.write('xq\nyq\nzq\n')
			out_stream.flush()
			axes = {}
			for _ in range(3): #TODO: make this less dependent on returning exactly 3 lines in JSON format
				line = in_stream.readline()
				axis_data = json.loads(line)
				axes[axis_data['axis']] = axis_data['params']
			diff_axes = {
				'x':self.dx,
				'y':self.dy,
				'z':self.dz,
			}
			all_progress = []
			for axis_label in axes:
				axis = axes[axis_label]

				tot_pulses = abs(units.convert_to_pulses(diff_axes[axis_label], self.calibration_info[axis_label], self.units))
				pulses_left = abs(axis['target_pos']-axis['position'])
				if axis['pulse_spacing']==0:
					cur_pulse_progress = 1.0
				else:
					cur_pulse_progress = (axis['next_pulse'] - axis['cur_time'])/float(axis['pulse_spacing'])
				if tot_pulses > 0:
					progress = ((tot_pulses - pulses_left) + cur_pulse_progress) / float(tot_pulses)
				else:
					progress = 1.0
				if pulses_left==0:
					progress = 1.0
				
				axis['pulses_left'] = pulses_left
				axis['cur_pulse_progress'] = cur_pulse_progress
				axis['progress'] = progress

				all_progress.append(progress)
			return {
				'axes':axes,
				'max_progress':max(all_progress),
				'min_progress':min(all_progress),
				'avg_progress':sum(all_progress)/float(len(all_progress)),
			}
	
	@staticmethod
	def from_relative(dx,dy,dz, speed, units='m', calibration_info={}):
		return MovementStep(speed=speed, x=dx,y=dy,z=dz, relative=True, units=units, calibration_info=calibration_info)
	
	@staticmethod
	def from_target(x,y,z, speed, prev_status, units='m', calibration_info={}):
		return MovementStep(speed=speed, x=x,y=y,z=z, relative=False, units=units, prev_status=prev_status, calibration_info=calibration_info)
	
	@staticmethod
	def list_from_gcode(gcode_tokens, token_order, current_state={}, err_stream = sys.stderr, calibration_info={}):
		state = {
			'Xpos':0,
			'Ypos':0,
			'Zpos':0,
			'speed':0,
			'travel_speed':0,
			'relative':False,
			'units':'m',
		}
		state.update(current_state)
		ret = []
		if token_order[0]=='G':
			if gcode_tokens['G']==1:
				vals = {
					'X':{True:0,False:state['Xpos']}[state['relative']],
					'Y':{True:0,False:state['Ypos']}[state['relative']],
					'Z':{True:0,False:state['Zpos']}[state['relative']],
					'S':state['speed'],
				}
				vals.update(gcode_tokens)
				ret = [MovementStep(speed=vals['S'], x=vals['X'],y=vals['Y'],z=vals['Z'], relative=state['relative'], units=state['units'], prev_status=state, calibration_info=calibration_info)]
				state['speed'] = vals['S']
				if state['relative']:
					state['Xpos'] = state['Xpos'] + vals['X']
					state['Ypos'] = state['Ypos'] + vals['Y']
					state['Zpos'] = state['Zpos'] + vals['Z']
				else:
					state['Xpos'] = vals['X']
					state['Ypos'] = vals['Y']
					state['Zpos'] = vals['Z']
			elif gcode_tokens['G']==0:
				vals = {
					'X':{True:0,False:state['Xpos']}[state['relative']],
					'Y':{True:0,False:state['Ypos']}[state['relative']],
					'Z':{True:0,False:state['Zpos']}[state['relative']],
					'S':state['travel_speed'],
				}
				vals.update(gcode_tokens)
				ret = [MovementStep(speed=vals['S'], x=vals['X'],y=vals['Y'],z=vals['Z'], relative=state['relative'], units=state['units'], prev_status=state, calibration_info=calibration_info)]
				state['travel_speed'] = vals['S']
				if state['relative']:
					state['Xpos'] = state['Xpos'] + vals['X']
					state['Ypos'] = state['Ypos'] + vals['Y']
					state['Zpos'] = state['Zpos'] + vals['Z']
				else:
					state['Xpos'] = vals['X']
					state['Ypos'] = vals['Y']
					state['Zpos'] = vals['Z']
			else:
				err_stream.write("WARNING: unrecognized G code: {}\n".format(gcode_split.dict2gcode(gcode_tokens, token_order)))
		else:
			err_stream.write("WARNING: unrecognized Gcode command: {}\n".format(gcode_split.dict2gcode(gcode_tokens, token_order)))
		return (ret, state)


#%% test code
if __name__=='__main__':
	ret,state = MovementStep.list_from_gcode(*gcode_split.gcode2dict("G1 X85.768 Y49.268 Z-4.000"))
	print(ret, state)
	ret,state = MovementStep.list_from_gcode(*gcode_split.gcode2dict("G1 X85.768 Y49.268 Z-4.000"), current_state=state)
	print(ret, state)
	ret,state = MovementStep.list_from_gcode(*gcode_split.gcode2dict("G1 X-85.768 Y-49.268 Z4.000"), current_state=state)
	print(ret, state)
	ret,state = MovementStep.list_from_gcode(*gcode_split.gcode2dict("G1 X-85.768 Y-49.268 Z4.000"), current_state=state)
	print(ret, state)
