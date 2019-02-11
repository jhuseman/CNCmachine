#%% import dependencies
import inspect

import sys
import serial

import stdio
import multi_stream
import tee_stream

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
		if type(ident) in [str]:
			if ident[:3]=='COM' or ident[:8]=='/dev/tty':
				self.fobj = serial.Serial(ident, *args, **kwargs)
				# additional setup for serial encoding support
				def serial_write(data):
					if isinstance(data, str):
						ser_data = data.encode('utf-8')
					else:
						ser_data = data
					return self.fobj.write(ser_data)
				def serial_read(*args, **kwargs):
					ret = self.fobj.read(*args, **kwargs)
					if isinstance(ret, str):
						return ret
					else:
						return ret.decode('utf-8')
				def serial_readline(*args, **kwargs):
					ret = self.fobj.readline(*args, **kwargs)
					if isinstance(ret, str):
						return ret
					else:
						return ret.decode('utf-8')
				setattr(self, 'write', serial_write)
				setattr(self, 'read', serial_read)
				setattr(self, 'readline', serial_readline)
			elif ident=='STDIO':
				self.fobj = stdio.stdio()
			elif ident=='STDIN':
				self.fobj = sys.stdin
			elif ident=='STDOUT':
				self.fobj = sys.stdout
			elif ident=='STDERR':
				self.fobj = sys.stderr
			elif ident=='multi':
				self.fobj = multi_stream.MultiStream(*args, **kwargs)
			elif ident=='tee':
				self.fobj = tee_stream.TeeStream(*args, **kwargs)
			else:
				self.fobj = open(ident, *args, **kwargs)
		else:
			# assume is a file-like object and will work as normal
			self.fobj = ident
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
