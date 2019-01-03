#%% define functions
def gcode2pairs(gcode):
	token_pairs = []
	tokens = gcode.split(' ')
	for token in tokens:
		key = token[0]
		val = token[1:]
		try:
			val = int(val)
		except ValueError:
			try:
				val = float(val)
			except ValueError:
				pass
		token_pairs.append((key, val))
	return token_pairs

def pairs2dict(pairs):
	out_dict = {}
	out_order = []
	for pair in pairs:
		out_dict[pair[0]] = pair[1]
		out_order.append(pair[0])
	return (out_dict, out_order)

def gcode2dict(gcode):
	return pairs2dict(gcode2pairs(gcode))

def dict2gcode(tokens, token_order):
	ret = ''
	for t in token_order:
		if not ret=='':
			ret = ret + ' '
		ret = ret + t + str(tokens[t])
	return ret