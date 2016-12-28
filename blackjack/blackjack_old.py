import random 
import sys
import math

class DECK():
	def __init__(self):
		self.new_deck()

	def new_deck(self):
		self.cards  = []
		for val in ['A','2','3','4','5','6','7','8','9','T','J','Q','K']:
			for suit in ['H','D','S','C']:
				self.cards.append(val+suit)
		random.shuffle(self.cards)

	def get_card(self):
		return self.cards.pop()

	def cards_remaining(self):
		return len(self.cards)

class TABLE():
	def __init__(self, player_algo, do_log=False):
		self.deck         = DECK() # a deck class
		self.dealer_hand  = []     # a list of cards
		self.player_hand  = []     # a list of cards
		self.discard_pile = []     # used for discarded cards after each game
		self.player_algo  = player_algo # function that's passed (dealer_card, player_hand, discard_pile) and returns hit or stay
		self.games_played = 0
		self.games_won    = 0
		self.valid_game   = True
		self.do_log       = do_log

	def new_deck(self):
		# reset everything, usually called mid-game when cards run out, and need to ditch the whole game state
		self.dealer_hand  = []
		self.player_hand  = []
		self.discard_pile = []
		self.deck.new_deck()
		#print '>>>>>\n SHUFFLING NEW DECK \n>>>>>'


	def setup_next_game(self): # deal new hands
		# move hands to discard pile and reset hand
		self.discard_pile += self.dealer_hand + self.player_hand
		self.dealer_hand = []
		self.player_hand = []

		# verify deck has enough cards to deal before starting
		if self.deck.cards_remaining() < 4:
			self.new_deck()

		# deal next game
		self.deal( self.dealer_hand )
		self.deal( self.dealer_hand )
		self.deal( self.player_hand )
		self.deal( self.player_hand )

	def deal(self, hand):
		hand.append( self.deck.get_card() )			

	def check_player_win(self):
		d = get_hand_value(self.dealer_hand)
		p = get_hand_value(self.player_hand)
		if p <= 21 and d > 21:
			return True
		if p <= 21 and p > d:
			return True
		return False

	def record_game(self):
		self.games_played += 1
		if self.check_player_win():
			self.games_won += 1

		self.generate_machine_learning_log2()	

			
	def play_game(self):
	# may fail to record game if cards run out
		self.setup_next_game()
		
		# multiple break conditions easier to read in structure below
		while True: 

			# first, verify we didn't run out of cards
			if self.deck.cards_remaining() == 0: # ran out of cards
				self.new_deck() 
				# break without calling record_game()
				break

			# second, determine if player wants more cards
			elif self.player_algo(self.dealer_visible_card(), self.player_hand, self.discard_pile) == 'hit':
				self.deal( self.player_hand )

			# third, determine if dealer wants more cards
			elif self.dealer_algo() == 'hit':
				self.deal( self.dealer_hand )

			# fourth, reaching this else, means both players are done
			else:
				self.record_game()
				break

	def dealer_algo(self):
		if get_hand_value(self.dealer_hand) < 16:
			return 'hit'
		else:
			return 'stay'

	def dealer_visible_card(self):
		return self.dealer_hand[0]

	def generate_machine_learning_log(self):
	# 0 : unknown (dealer hand or in deck)
	# 1 : dealers card
	# 2 : discard pile
	# 3 : player hand
		if self.check_player_win() and self.do_log: # only create reconds on win
			# default array to unknown : 0
			card_dict  = {'ACTION':1}
			card_order = ['ACTION']
			for val in ['A','2','3','4','5','6','7','8','9','T','J','Q','K']:
				for suit in ['H','D','S','C']:
					card_dict[val+suit] = 0
					card_order.append(val+suit)

			# insert in dealer card : 1
			card_dict[self.dealer_visible_card()] = 1
			
			# insert discard plile : 2
			for c in self.discard_pile:
				card_dict[c] = 2

			# seed starting hand
			card_dict[ self.player_hand[0] ] = 3
			card_dict[ self.player_hand[1] ] = 3

			i = 2
			while i < len(self.player_hand):
				# record a hit : 1
				write(card_dict, card_order)				
				card_dict[ self.player_hand[i] ] = 3
				i += 1

			# record a stay : 0
			card_dict['ACTION'] = 0
			write(card_dict, card_order)
	
	def generate_machine_learning_log2(self):
		if self.check_player_win() and self.do_log: # only create reconds on win
			i = 2
			while i < len(self.player_hand):
				# record a hit : 1
				d = get_hand_value([ self.dealer_visible_card() ])
				p = get_hand_value( self.player_hand[:i])
				s = '{},{},{}\n'.format(d,p,1)
				#print s
				f.write(s)
				i += 1

			# record a stay : 0
			d = get_hand_value([ self.dealer_visible_card() ])
			p = get_hand_value( self.player_hand[:i])
			s = '{},{},{}\n'.format(d,p,0)
			#print s
			f.write(s)
	



	def print_game(self):
		# print player, hand_value, hand, win
		print 'games played :', self.games_played
		print 'games won    :', self.games_won
		print 'dealer hand  :', self.dealer_hand, get_hand_value(self.dealer_hand) 
		print 'player hand  :', self.player_hand, get_hand_value(self.player_hand)
		print 'player wins  :', self.check_player_win()
		print 'cards left   :', self.deck.cards_remaining()

		print '#'*30


def get_hand_value(hand):
	card_values = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':10,'Q':10,'K':10}
	hand_values = [card_values[c[0]] for c in hand]
	total = sum(hand_values)

	# use ace as 11 unless bust
	if 1 in hand_values and total + 10 <=21:
		return total + 10
	else:
		return total

######################
## PLAYER ALGOS
######################
def sigmoid(z):
	return 1 / (1 + math.e**(-z))

def player_lr1(dealer_card, player_hand, discard):
	# logistical regression machine learning
	# 2k examples, inputs of hand size and dealer card
	# win rate = 42% (out of 100k games)
	theta0 = 3.883246
	theta1 = 0.000017
	theta2 = -0.270047
	x1 = get_hand_value([dealer_card])
	x2 = get_hand_value( player_hand )
	predict = sigmoid(theta0 + theta1*x1 + theta2*x2)
	if predict > .5:
		return 'hit'
	else:
		return 'stay'

def player_random(dealer_card, player_hand, discard):
	# random player
	# win rate = 19% (out of 100k games)
	return random.choice( ['hit', 'stay'] )

def player_stay(dealer_card, player_hand, discard):
	# never hits
	# 
	return 'stay'

def player_hit16_algo(dealer_card, player_hand, discard):
	if get_hand_value(player_hand) < 16:
			return 'hit'
	else:
		return 'stay'

def write(d, a):
	s = ','.join( [str(d[k]) for k in a] )
	f.write(s+'\n')

f = open('bj_data.txt','a+')
T = TABLE(player_stay)
while T.games_played < 100000:
	T.play_game()
	#T.print_game()
print '! {} Played, {} Won, {}% '.format(T.games_played, T.games_won, 100.0 * T.games_won / T.games_played)
