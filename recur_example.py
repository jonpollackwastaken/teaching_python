def countdown(x):
	if x == 0:
		print 'blast off'
	else:
		print x
		countdown(x-1)

countdown(10)