#%% Import dependencies
import numpy as np
import math

from jupyter_animate import anim_func

#%%
def deg2rad(d):
	return d * 2 * math.pi / 360.0
def seq2segments(seq):
	seg = []
	prev = seq[0]
	for it in seq[1:]:
		if prev!=it:
			seg.append((prev, it))
		prev = it
	return seg
def seq2xy(seq):
	x = []
	y = []
	for it in seq:
		x.append(it[0])
		y.append(it[1])
	return x, y
def xy2seq(x,y):
	return zip(x,y)
def gen_rack_tooth(h=0.25,w=0.5,angle_d=60):
	angle_rad = deg2rad(angle_d)
	angle_width = h/math.tan(angle_rad)
	horiz_width = (w/2.0) - angle_width
	points = [
		(0, 				0), 
		(horiz_width, 		0), 
		(w/2, 				h),
		(w - angle_width, 	h),
		(w, 				0),
	]
	return points
def translate(pt, dx=0, dy=0):
	return (pt[0]+dx, pt[1]+dy)
def translate_seq(seq, dx=0, dy=0):
	def tmp_translate(pt, dx=dx, dy=dy):
		return translate(pt, dx=dx, dy=dy)
	return map(tmp_translate, seq)
def check_intersect(seg1, seg2):
	def check_intersect_noendlimit(seg1, seg2):
		seg1_dx = seg1[0][0] - seg1[1][0]
		seg1_dy = seg1[0][1] - seg1[1][1]
		seg2_dx = seg2[0][0] - seg2[1][0]
		seg2_dy = seg2[0][1] - seg2[1][1]
		if seg1_dx==0 and seg2_dy==0:
			return (seg1[0][0], seg2[0][1])
		if seg1_dx==0 or seg2_dx==0:
			inv = check_intersect_noendlimit(
				((seg1[0][1],seg1[0][0]), (seg1[1][1],seg1[1][0])),
				((seg2[0][1],seg2[0][0]), (seg2[1][1],seg2[1][0]))
			)
			if inv is None:
				return None
			return (inv[1], inv[0])
		seg1_m = seg1_dy/seg1_dx
		seg2_m = seg2_dy/seg2_dx
		if seg1_m == seg2_m:
			return None
		x = ((seg2[0][1] - seg2_m * seg2[0][0]) - (seg1[0][1] - seg1_m * seg1[0][0])) / (seg1_m - seg2_m)
		y = seg1_m * (x - seg1[0][0]) + seg1[0][1]
		return (x, y)
	
	def in_boundbox(box, pt):
		def in_range(rng, val):
			if rng[0] > rng[1]:
				return in_range((rng[1],rng[0]), val)
			return rng[0] <= val and val <= rng[1]
		return in_range((box[0][0], box[1][0]), pt[0]) and in_range((box[0][1], box[1][1]), pt[1])
	
	inters = check_intersect_noendlimit(seg1, seg2)
	if inters is None:
		return None
	if in_boundbox(seg1, inters):
		if in_boundbox(seg2, inters):
			return inters
	return None
def seg_len(seg):
	dx = seg[0][0] - seg[1][0]
	dy = seg[0][1] - seg[1][1]
	return math.sqrt(dx*dx + dy*dy)
def gen_gear(rad=1,trad=0.25,angle_d=60,n_teeth=10,rot_res=100,rad_res=100):
	tooth_angle = 2 * math.pi / float(n_teeth)
	outer_rad = rad + trad
	tooth_outer_width = outer_rad * tooth_angle
	rack = gen_rack_tooth(h=trad, w=tooth_outer_width, angle_d=angle_d)
	rack_lowered = translate_seq(rack, dy=-1*outer_rad)
	rack_extended = translate_seq(rack_lowered, dx=-1*tooth_outer_width) + rack_lowered + translate_seq(rack_lowered, dx=tooth_outer_width)
	rack_segments = seq2segments(rack_extended)
	rot_positions = np.linspace(-1*tooth_angle/2.0, tooth_angle/2.0, rot_res)
	rad_positions = np.linspace(0, tooth_angle, rad_res+1)[:-1]
	radii = []
	infin = float("inf")
	for rad_pos in rad_positions:
		best_rad = infin
		this_center_x = outer_rad * rad_pos
		for rot_pos in rot_positions:
			this_x_pos = this_center_x + (outer_rad * rot_pos)
			vect_out_d = (math.tan(-1*rot_pos),-1)
			vect_out_len_mult = 2 * outer_rad # make sure this is long enough to guarantee intersection
			vect_out_d = (vect_out_d[0]*vect_out_len_mult, vect_out_d[1]*vect_out_len_mult)
			vect_out_end = (vect_out_d[0] + this_x_pos, vect_out_d[1])
			this_cent_pos = (this_x_pos, 0)
			vect_out_seg = (this_cent_pos, vect_out_end)
			rad = outer_rad
			for seg in rack_segments:
				intersect = check_intersect(vect_out_seg, seg)
				if not intersect is None:
					int_rad = seg_len( (this_cent_pos, intersect) )
					if int_rad < rad:
						rad = int_rad
			if rad < best_rad:
				best_rad = rad
		radii.append(best_rad)
	out_rad_pos = []
	out_radii = []
	for n in np.linspace(0,2*math.pi,n_teeth+1)[:-1]:
		out_rad_pos = out_rad_pos + list(rad_positions + n)
		out_radii = out_radii + radii
	return xy2seq(out_radii, out_rad_pos)

def cart2rad(x,y):
	r = math.sqrt(x*x + y*y)
	if x == 0:
		theta = math.pi/2
	else:
		theta = math.atan(y/x)
	if x < 0:
		theta = theta + math.pi
	while theta < 0:
		theta = theta + 2*math.pi
	while theta >= math.pi:
		theta = theta - 2*math.pi
	return r,theta

def cart2rad_seq(seq):
	def tmp_cart2rad(tpl):
		return cart2rad(*tpl)
	return map(tmp_cart2rad, seq)

def rad2cart(r,theta):
	x = r*math.cos(theta)
	y = r*math.sin(theta)
	return x,y

def rad2cart_seq(seq):
	def tmp_rad2cart(tpl):
		return rad2cart(*tpl)
	return map(tmp_rad2cart, seq)

def rotate(seq, cent=(0,0), angle=0):
	cent_neg = (-1*cent[0], -1*cent[1])
	tr = translate_seq(seq, *cent_neg)
	rad = cart2rad_seq(tr)
	rad_r, rad_th = seq2xy(rad)
	def rot_pt(th,angle=angle):
		return angle + th
	rad_rot = xy2seq(rad_r, map(rot_pt,rad_th))
	rot = rad2cart_seq(rad_rot)
	return translate_seq(rot, *cent)

#%%
def gen_rack_pinion(inner_rad = 1, tooth_rad = 0.25, angle_d = 60, n_teeth=10, rot_res=100, rad_res=100):
	tooth_angle = 2 * math.pi / float(n_teeth)
	outer_rad = inner_rad + tooth_rad
	tooth_outer_width = outer_rad * tooth_angle
	gear_seq = rotate(rad2cart_seq(gen_gear(rad=inner_rad,trad=tooth_rad,angle_d=angle_d,n_teeth=n_teeth,rot_res=rot_res,rad_res=rad_res)), angle=1.5*math.pi)
	teeth_seq_single = translate_seq(gen_rack_tooth(h=tooth_rad,w=tooth_outer_width,angle_d=angle_d),dx=-0.0*tooth_outer_width,dy=-1*outer_rad)
	teeth_seq = []
	for i in np.linspace(-1*n_teeth,n_teeth,2*n_teeth+1):
		teeth_seq = teeth_seq + translate_seq(teeth_seq_single, dx=i*tooth_outer_width)
	return {
		'pinion': 		gear_seq,
		'rack': 		teeth_seq,
		'properties': 	{
			'inner_rad': 			inner_rad,
			'tooth_rad': 			tooth_rad,
			'angle_d': 				angle_d,
			'n_teeth': 				n_teeth,
			'rot_res': 				rot_res,
			'rad_res': 				rad_res,
			'tooth_angle': 			tooth_angle,
			'outer_rad': 			outer_rad,
			'tooth_outer_width': 	tooth_outer_width,
		}
	}

#%%
def anim_rack_pinion(rack_pinion_res, anim_res = 100):
	gear_seq = rack_pinion_res['pinion']
	rack_seq = rack_pinion_res['rack']
	tooth_angle = 		rack_pinion_res['properties']['tooth_angle']
	tooth_outer_width = rack_pinion_res['properties']['tooth_outer_width']
	outer_rad = 		rack_pinion_res['properties']['outer_rad']
	n_teeth = 			rack_pinion_res['properties']['n_teeth']
	def anim_gear(t):
		gear_rot = rotate(gear_seq, angle=(t-int(n_teeth/2))*tooth_angle)
		rack_transl = translate_seq(rack_seq, dx=t*tooth_outer_width)
		return seq2xy(gear_rot + rack_transl)
	return anim_func(anim_gear, mint=0, maxt=1, tstep=1.0/anim_res, window=((-1.25*outer_rad,1.25*outer_rad),(-1.25*outer_rad,1.25*outer_rad)))

#%%
rack_pinion_def = gen_rack_pinion()
#%%
anim_rack_pinion(rack_pinion_def, 50)

