#%%
import math

#%%
def calc_torque(gear_rad_in=1, steps=200, torque_N_m=2, speed_rpm=900):
	m_p_in = 0.0254
	lb_p_N = 0.224808943
	speed_torque_N_m=torque_N_m # assume full torque at this speed
	gear_circ_in = gear_rad_in*2*math.pi
	step_dist_in = gear_circ_in/float(steps)
	step_dist_m = step_dist_in * m_p_in
	step_dist_mm = step_dist_m * 1000
	gear_rad_m = gear_rad_in * m_p_in
	force_N = float(speed_torque_N_m)/gear_rad_m
	force_lb = force_N * lb_p_N
	force_oz = force_lb * 16
	speed_in_p_min = gear_circ_in*speed_rpm
	speed_in_p_s = float(speed_in_p_min)/60
	speed_mps = speed_in_p_s * m_p_in
	return {
		'speed':{
			'in/min':speed_in_p_min,
			'in/s':  speed_in_p_s,
			'm/s':   speed_mps,
		},
		'force':{
			'N': force_N,
			'lb':force_lb,
			'oz':force_oz,
		},
		'step_dist':{
			'in':step_dist_in,
			'm': step_dist_m,
			'mm':step_dist_mm,
		},
	}

#%%
def m2in(m):
	m_p_in = 0.0254
	return m/m_p_in

#%%
def tps2rpm(tps, steps):
	rps = float(tps)/(steps)
	rpm = rps*60
	return rpm

#%%
steps = 200*32
rad_in = m2in(0.1)/(math.pi*2)
speed_rpm = tps2rpm(100000, steps)
print(steps)
print(rad_in)
print(speed_rpm)
params = {
	'gear_rad_in':rad_in,
	'steps':steps,
	'torque_N_m':0.59,
	'speed_rpm':speed_rpm,
}
calc_torque(**params)

#%%
