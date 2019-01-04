#! /usr/bin/env python

#%% import modules
import sys
import json
import time

import gen_stream
import movement_step
import gcode_split
import time_calculations
import status_display

#%% define class
class GcodeInterpreter(object):
	def __init__(self, in_code_stream, out_arduino_stream, arduino_feedback_in_stream='out', error_stream=sys.stderr, calibration_info={}, init_state={}, time_manager=time, stat_store=None):
		if arduino_feedback_in_stream=='out':
			arduino_feedback_in_stream = out_arduino_stream
		self.in_code_stream = in_code_stream
		self.out_arduino_stream = out_arduino_stream
		self.arduino_feedback_in_stream = arduino_feedback_in_stream
		self.error_stream = error_stream
		self.calibration_info = calibration_info
		self.state = {
			'Xpos':0,
			'Ypos':0,
			'Zpos':0,
			'speed':0,
			'travel_speed':0,
			'relative':False,
			'units':'m',
		}
		self.state.update(init_state)
		self.time_manager = time_manager
		self.stat_store = stat_store
	
	def interpret_line(self, line):
		if len(line)==0:
			# blank line - do nothing
			return []
		while line[-1]=='\n': # remove trailing newline
			line = line[:-1]
		line_start = line[0]
		if line_start=='G':
			# G command - interpret as MovementStep
			ret,state = movement_step.MovementStep.list_from_gcode(*gcode_split.gcode2dict(line), current_state=self.state, err_stream=self.error_stream, calibration_info=self.calibration_info)
			self.state = state
			return ret
		elif line_start in [';','(']:
			# comment - do nothing
			return []
		else:
			self.error_stream.write("WARNING: unrecognized Gcode line: {}\n".format(line))
			return []
	
	def interpret_continuously(self):
		continuing = True
		while continuing:
			line = self.in_code_stream.readline()
			self.error_stream.write(line) #DEBUG - output current line
			if line=='':
				continuing = False
			else:
				result = self.interpret_line(line)
				for step in result:
					step.run(out_stream=self.out_arduino_stream, in_stream=self.arduino_feedback_in_stream, time_manager=self.time_manager, stat_store=self.stat_store)


#%% main run function
def run(in_code=('linuxcnc.gcode', 'r'), out_stream=('COM5',{'baudrate':115200}), out_feedback_stream='out', err_stream='STDERR', calib=('calibration.json', 'r'), init_param=('defaults.json', 'r'), time_manager=time, stat_store = None):
	with gen_stream.gen_stream(calib) as calib_file:
		calib_data = json.load(calib_file)
	with gen_stream.gen_stream(init_param) as init_file:
		init_data = json.load(init_file)
	
	streams = []
	out_arduino_stream = gen_stream.gen_stream(out_stream)
	streams.append(out_arduino_stream)
	if out_feedback_stream is None:
		arduino_feedback_in_stream = None
	elif out_feedback_stream=='out':
		arduino_feedback_in_stream = out_arduino_stream
	else:
		arduino_feedback_in_stream = gen_stream.gen_stream(out_feedback_stream)
		streams.append(arduino_feedback_in_stream)
	in_code_stream = gen_stream.gen_stream(in_code)
	streams.append(in_code_stream)
	error_stream = gen_stream.gen_stream(err_stream)
	streams.append(error_stream)

	interpreter = GcodeInterpreter(in_code_stream, out_arduino_stream, arduino_feedback_in_stream=arduino_feedback_in_stream, error_stream=error_stream, calibration_info=calib_data, init_state=init_data, time_manager=time_manager, stat_store=stat_store)
	interpreter.interpret_continuously()

	for stream in streams:
		stream.close()

#%% friendlier run function
def run_friendly(preset=['default','dry_run'][0], *args_override, **kwargs_override):
	default_vals = {
		'default':{'args':[],'kwargs':{},},
		'dry_run':{
			'args':[],
			'kwargs':{
				'out_stream':'STDIO',
				'out_feedback_stream':None,
			},
		},
		'dry_run_fast':{
			'args':[],
			'kwargs':{
				'out_stream':'STDIO',
				'out_feedback_stream':None,
				'time_manager':time_calculations.TimeCalculator(),
			},
		},
	}
	args = default_vals[preset]['args']
	kwargs = default_vals[preset]['kwargs']
	args = args + list(args_override)
	kwargs.update(kwargs_override)
	run(*args, **kwargs)

#%% run code
if __name__=="__main__":
	stat_store = status_display.status_store()
	# disp = status_display.status_display_handler(stat_store)
	# disp.run_async()
	# run_friendly('dry_run_fast', stat_store=stat_store)
	run_friendly('default', stat_store=stat_store)

