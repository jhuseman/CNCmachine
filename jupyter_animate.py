#%% Import dependencies
import matplotlib.pyplot as plt

from matplotlib import animation
from IPython.display import HTML

#%%

def anim_func(func, mint=0, maxt=1, tstep=0.01, window=((0,2),(-2,2))):
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
		return (plot_plot,)
	# call the animator. blit=True means only re-draw the parts that have changed.
	anim = animation.FuncAnimation(plot_fig, animate_plot, init_func=init_plot, frames=frame_count, interval=20, blit=True)
	return HTML(anim.to_jshtml())

