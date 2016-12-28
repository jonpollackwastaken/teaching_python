import commands

domains = ['pixel.mathtag.com', 'www.mediamath.com', 'www.google.com']

for d in domains:
	output = commands.getoutput( 'curl -s -D - {0}'.format(d) )
	output = output.split('\n')
	print output[0].split(' ')[1], d