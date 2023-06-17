
def run():
	text = 'in a land far, far away, there lived a blank'.split(' ')
	current = 'Once upon a time,'
	for word in text:
		print(current, '___')
		current += ' ' + word

