def convert_unit(val, val_unit, to_unit):
	unit_conversions = {
		'm':1.0,
		'dm':0.1,
		'cm':0.01,
		'mm':0.001,
		'um':0.000001,
		'in':0.0254,
		'ft':0.3048,
		'yd':0.9144,
	}
	normalized_val = float(val)*unit_conversions[val_unit]
	output_val = normalized_val/float(unit_conversions[to_unit])
	return output_val

def convert_to_pulses(val, calibration, unit):
	default_calib = {
		'unit':'m',
		'dist':0.1,
		'pulses':200*64,
	}
	full_calib = default_calib
	full_calib.update(calibration)
	val_calib_unit = convert_unit(val, unit, full_calib['unit'])
	calib_pulses_per_unit = float(full_calib['pulses'])/full_calib['dist']
	corrected_val_pulses = val_calib_unit*calib_pulses_per_unit
	return int(corrected_val_pulses)