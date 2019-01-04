#%% import dependencies
import inspect

import sys
import serial

import stdio

#%% define class
class gen_stream(object):
	def __init__(self, ident):
		args = []
		kwargs = {}
		if type(ident) in [tuple,list]:
			idlist = ident
			for i in range(len(idlist)):
				if i==0:
					ident = idlist[0]
				else:
					if type(idlist[i]) in [dict]:
						kwargs.update(idlist[i])
					elif type(idlist[i]) in [tuple,list]:
						args = args + list(idlist[i])
					else:
						args.append(idlist[i])
		if ident[:3]=='COM' or ident[:8]=='/dev/tty':
			self.fobj = serial.Serial(ident, *args, **kwargs)
		elif ident=='STDIO':
			self.fobj = stdio.stdio()
		elif ident=='STDERR':
			self.fobj = sys.stderr
		else:
			self.fobj = open(ident, *args, **kwargs)
		self.extend_methods()
	
	def extend_methods(self):
		def gen_temp_func(method_name):
			def temp_run_method(*args, **kwargs):
				method = getattr(self.fobj, method_name, None)
				if inspect.isroutine(method):
					return method(*args, **kwargs)
			return temp_run_method
		for member in inspect.getmembers(self.fobj, predicate=inspect.isroutine):
			method_name = member[0]
			if getattr(self, method_name, None) is None:
				setattr(self, method_name, gen_temp_func(method_name))

	def __enter__(self, *args, **kwargs):
		return self.fobj.__enter__(*args, **kwargs)
	
	def __exit__(self, *args, **kwargs):
		return self.fobj.__exit__(*args, **kwargs)

#%% test
if __name__=='__main__':
	with gen_stream('STDIO') as a:
		a.write(a.readline())
