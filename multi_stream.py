#%% import dependencies
import gen_stream
import inspect
import threading
import time

#%% define class
class MultiStream(object):
	def __init__(self, *idents):
		self.streams = []
		for ident in idents:
			self.streams.append(gen_stream.gen_stream(ident))
		self.read_threads = []
		self.read_cache = ''
		self.read_cache_lock = threading.Lock()
		self.threads_stopping = False
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

	def read(self, size=1, newline_cache=True):
		def gen_read_func(stream, callback):
			def read_func(size=1):
				local_cache=''
				while not self.threads_stopping:
					ret = stream.read(size=size)
					if newline_cache:
						local_cache=local_cache + ret
						while '\n' in local_cache:
							nl_pos = local_cache.index('\n')
							new_ret = local_cache[:(nl_pos+1)]
							local_cache = local_cache[(nl_pos+1):]
							callback(new_ret)
					else:
						callback(ret)
			return read_func
		
		def recv_cb(data):
			with self.read_cache_lock:
				self.read_cache = self.read_cache + data
		if len(self.read_threads)==0:
			for stream in self.streams:
				thr = threading.Thread(target=gen_read_func(stream, recv_cb))
				thr.daemon = True
				self.read_threads.append(thr)
				thr.start()
		while len(self.read_cache) < size:
			time.sleep(0.001)
		with self.read_cache_lock:
			ret = self.read_cache[:size]
			self.read_cache = self.read_cache[size:]
		return ret
	
	def readline(self):
		ret = self.read()
		while ret[-1]!='\n':
			ret = ret + self.read(size=1, newline_cache=True)
		return ret

	def __enter__(self, *args, **kwargs):
		for stream in self.streams:
			stream.__enter__(*args, **kwargs)
		return self
	
	def __exit__(self, *args, **kwargs):
		self.threads_stopping = True
		for thr in self.read_threads:
			thr.join(0.5)
		ret = []
		for stream in self.streams:
			ret.append(stream.__exit__(*args, **kwargs))
		rem = list(ret) # make copy
		for r in ret:
			if r is None:
				rem.remove(r)
		if len(rem)==0:
			return None
		rem2 = list(rem) # make copy
		for r in rem:
			if isinstance(r, bool):
				rem2.remove(r)
		if len(rem2)>0:
			return rem2[-1]
		return rem[-1]

#%% test
if __name__=='__main__':
	with MultiStream('STDIO') as a:
		a.write(a.readline()) # pylint: disable=E1101