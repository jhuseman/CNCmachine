#%% import modules
import copy
import numpy as np
import threading

from matplotlib import pyplot as plt


#%% define class

#TODO: create a class which can receive "pushed" status items from an active movement_step and continually shows the current status in graph form

class status_store(object):
	def __init__(self):
		self.cur_status = {}
		self.status_history = []
	
	def update(self, status, timestamp):
		self.cur_status = status
		self.status_history.append(
			{
				'timestamp':timestamp,
				'data':copy.deepcopy(status),
			}
		)
	
	def get_cur_status(self):
		return self.cur_status
	
	def get_status_history(self):
		return self.status_history
	
	@staticmethod
	def extract_coords(stat, axes=['x','y','z'], param='position'):
		ret = []
		for axis in axes:
			this_axis = stat['axes'][axis]
			ret.append(this_axis[param])
		return ret
	
	@staticmethod
	def flatten_history(hist, key='data'):
		return [s[key] for s in hist]
	
	@staticmethod
	def transpose(samples):
		ret = []
		for i in samples[0]:
			ret.append([])
		for i in samples:
			for j in range(len(i)):
				ret[j].append(i[j])
		return ret

	def get_cur_coords(self, **extract_kwargs):
		stat = self.get_cur_status()
		return status_store.extract_coords(stat, **extract_kwargs)

	def get_coords_history(self, **extract_kwargs):
		ret = []
		stat_hist = self.get_status_history()
		for stat in stat_hist:
			ret.append(
				{
					'timestamp':stat['timestamp'],
					'data':status_store.extract_coords(stat['data'], **extract_kwargs),
				}
			)
		return ret








#%% display data



def anim_func(func, mint=0, maxt=None, tstep=0.01, window=((0,2),(-2,2))):
	if maxt is None:
		frame_count = None
		real_tstep = tstep
	else:
		frame_count = int((maxt-mint)/tstep)
		real_tstep = float(maxt-mint)/frame_count
	# First set up the figure, the axis, and the plot element we want to animate
	plot_fig, plot_ax = plt.subplots()

	if not window is None:
		plot_ax.set_xlim(window[0])
		plot_ax.set_ylim(window[1])

	plot_plot, = plot_ax.plot([], [], lw=2)
	# initialization function: plot the background of each frame
	def init_plot():
		plot_plot.set_data([], [])
		return (plot_plot,)
	# animation function. This is called sequentially
	def animate_plot(i, func=func, mint=mint, tstep=real_tstep):
		t = mint + tstep*i
		x, y = func(t)
		plot_plot.set_data(x, y)
		redraw_figure()
		return (plot_plot,)
	def redraw_figure(tstep=real_tstep):
		plt.draw() #TODO: find cause of error here!
		plt.pause(tstep)
	init_plot()
	i = 0
	while (frame_count is None) or (i < frame_count):
		animate_plot(i)
		i = i + 1
	return plot_fig


class status_display_handler(object):
	def __init__(self, stat_store, anim_function=anim_func, get_all=True):
		self.stat_store = stat_store
		self.anim_function = anim_function
		self.plot = None
		self.get_all = get_all
	
	def get_frame(self, t):
		ch = self.stat_store.get_coords_history(axes=['x','y'])
		if self.get_all:
			num_items = len(ch)
		else:
			ts = status_store.flatten_history(ch, key='timestamp')
			tsn = np.array(ts)
			num_items = len(tsn[tsn < t])
		return status_store.transpose(status_store.flatten_history(ch[:num_items]))


	def run(self):
		return self.anim_function(self.get_frame)
	
	def run_async(self):
		threading.Thread(target=self.run).start()
		


# import time
# from matplotlib import pyplot as plt
# import numpy as np

# def live_update_demo():

# 	#plt.subplot(2, 1, 1)
# 	#h1 = plt.imshow(np.random.randn(30, 30))
# 	#redraw_figure()
# 	#plt.subplot(2, 1, 2)
# 	h2, = plt.plot(np.random.randn(50))
# 	redraw_figure()

# 	t_start = time.time()
# 	for i in xrange(1000):
# 		#h1.set_data(np.random.randn(30, 30))
# 		#redraw_figure()
# 		h2.set_ydata(np.random.randn(50))
# 		redraw_figure()
# 		print 'Mean Frame Rate: %.3gFPS' % ((i+1) / (time.time() - t_start))

# def redraw_figure():
# 	plt.draw()
# 	plt.pause(0.00001)

# #live_update_demo()
