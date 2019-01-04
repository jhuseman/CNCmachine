#%% import dependencies
import sys
import inspect

#%% define class
class stdio(object):
	def __init__(self):
		self.try_first = {
			'default': 				'both',
			'read': 				'in',
			'readinto': 			'in',
			'readline': 			'in',
			'readlines': 			'in',
			'tell': 				'in',
			'truncate': 			'out',
			'write': 				'out',
			'writelines': 			'out',
			'xreadlines': 			'in',
		}
		self.extend_methods()
	
	def extend_methods(self):
		def gen_temp_func(method_name):
			def temp_run_method(*args, **kwargs):
				try_f = self.try_first['default']
				if method_name in self.try_first:
					try_f = self.try_first[method_name]
				ret = None
				if try_f in ['in','both']:
					try:
						method = getattr(sys.stdin, method_name, None)
						if inspect.isroutine(method):
							ret = method(*args, **kwargs)
					except:
						pass
				if try_f in ['out','both']:
					try:
						method = getattr(sys.stdout, method_name, None)
						if inspect.isroutine(method):
							ret = method(*args, **kwargs)
					except:
						pass
				return ret
			return temp_run_method
		for member in inspect.getmembers(sys.stdin, predicate=inspect.isroutine) + inspect.getmembers(sys.stdout, predicate=inspect.isroutine):
			method_name = member[0]
			if getattr(self, method_name, None) is None:
				setattr(self, method_name, gen_temp_func(method_name))

	def __enter__(self, *args, **kwargs):
		sys.stdin.__enter__(*args, **kwargs)
		sys.stdout.__enter__(*args, **kwargs)
		return self
	
	def __exit__(self, *args, **kwargs):
		a = sys.stdin.__exit__(*args, **kwargs)
		b = sys.stdout.__exit__(*args, **kwargs)
		if a is None:
			return b
		if b is None:
			return a
		if isinstance(a, bool):
			return b
		if isinstance(b, bool):
			return a
		return b

#%% test
if __name__=='__main__':
	with stdio() as a:
		a.write(a.readline().encode('utf-8'))