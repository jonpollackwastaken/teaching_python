f = open('all_words.txt', 'r')


def b_words(word):
	if word.startswith('b'):
		return True
	else:
		return False

def palindrom(forward):
	forward = line.strip()
	if line.startswith('b'):
		print forward
	
	backward = list(forward)
	backward.reverse()
	backward = ''.join(backward)

	if forward == backward:
		return True
	else:
		return False



class WORD():
	def __init__(self, s):
		self.word = s.strip()
		self.palindrom = self.is_palindrom()
		self.b_word = self.is_bword()

	def is_palindrom(self):
		forward = self.word.strip()		
		backward = list(forward)
		backward.reverse()
		backward = ''.join(backward)

		if forward == backward:
			return True
		else:
			return False

	def is_bword(self):
		if self.word.startswith('b'):
			return True
		else:
			return False


for line in f:
	w = WORD(line)
	print w.word, w.palindrom, w.b_word, w
