#%% define class
class TimeCalculator(object):
	def __init__(self, start_time=0.0, simulated_overhead=0.000001):
		self.cur_time = start_time
		self.simulated_overhead = simulated_overhead
	
	def sleep(self, dur):
		self.cur_time = self.cur_time + dur + self.simulated_overhead
	
	def clock(self):
		return self.cur_time
