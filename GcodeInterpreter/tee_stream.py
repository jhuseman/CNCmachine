#%% import dependencies
import gen_stream
import inspect
import threading
import time

#%% define class
class TeeStream(object):
	def __init__(self, main_ident, tee_ident):
		self.main = gen_stream.gen_stream(main_ident)
		self.tee = gen_stream.gen_stream(tee_ident)
		self.streams = [self.main, self.tee]
		self.extend_methods()
	
	def extend_methods(self):
		def gen_temp_func(method_name):
			def temp_run_method(*args, **kwargs):
				ret = None
				for stream in self.streams:
					try:
						method = getattr(stream, method_name, None)
						if inspect.isroutine(method):
							ret = method(*args, **kwargs)
					except:
						pass
				return ret
			return temp_run_method
		for stream in self.streams:
			for member in inspect.getmembers(stream, predicate=inspect.isroutine):
				method_name = member[0]
				if getattr(self, method_name, None) is None:
					setattr(self, method_name, gen_temp_func(method_name))

	def read(self, *args, **kwargs):
		ret = self.main.read(*args, **kwargs) # pylint: disable=E1101
		self.tee.write(ret) # pylint: disable=E1101
		return ret
	
	def readline(self, *args, **kwargs):
		ret = self.main.readline(*args, **kwargs) # pylint: disable=E1101
		self.tee.write(ret) # pylint: disable=E1101
		return ret

	def __enter__(self, *args, **kwargs):
		for stream in self.streams:
			stream.__enter__(*args, **kwargs)
		return self
	
	def __exit__(self, *args, **kwargs):
		a = self.main.__exit__(*args, **kwargs)
		b = self.tee.__exit__(*args, **kwargs)
		if b is None:
			return a
		if a is None:
			return b
		if isinstance(b, bool):
			return a
		if isinstance(a, bool):
			return b
		return a

#%% test
if __name__=='__main__':
	with TeeStream('STDIO', 'STDERR') as a:
		a.write(a.readline()) # pylint: disable=E1101