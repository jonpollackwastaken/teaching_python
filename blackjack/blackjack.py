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
	def __init__(self, player_algo, do_log=False, verbose=False):
		self.deck         = DECK() # a deck class
		self.dealer_hand  = []     # a list of cards
		self.player_hand  = []     # a list of cards
		self.discard_pile = []     # used for discarded cards after each game
		self.player_algo  = player_algo # function that's passed (dealer_card, player_hand, discard_pile) and returns hit or stay
		self.games_played = 0
		self.games_won    = 0
		self.games_tied   = 0
		self.valid_game   = True
		self.do_log       = do_log
		self.verbose      = verbose

	def new_deck(self):
		# reset everything, usually called mid-game when cards run out, and need to ditch the whole game state
		self.dealer_hand  = []
		self.player_hand  = []
		self.discard_pile = []
		self.deck.new_deck()
		if self.verbose:
			print '>>>>>\n SHUFFLING NEW DECK \n>>>>>'

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
		# player loses on bust, regardless of dealer hand (house edge)
		if p > 21:
			return 'loss'
		
		# player loses if less than dealer and dealer doesnt bust
		if p < d and d <=21:
			return 'loss'

		# player wins if under 21 and dealer busts
		if p <= 21 and d > 21:
			return 'win'		
		
		# player wins if under 21 and higher than dealer
		if p <= 21 and p > d:
			return 'win'
		
		# player ties if scores equal and no one busts
		if p==d and p<=21 and d<=21:
			return 'tie'
			
	def play_game(self):
	# may not record game if cards run out
		self.setup_next_game()
		
		# multiple break conditions easier to read in structure below
		while True: 

			# first, verify we didn't run out of cards
			if self.deck.cards_remaining() == 0: # ran out of cards
				self.new_deck() 
				# break without calling record_game()
				break

			# second, determine if player wants more cards
			elif self.player_algo([self.dealer_visible_card()], self.player_hand, self.discard_pile) == 'hit':
				self.deal( self.player_hand )

			# third, determine if dealer wants more cards
			elif self.dealer_algo() == 'hit':
				self.deal( self.dealer_hand )

			# fourth, reaching this else, means both players are done
			else:
				self.record_game()
				break

	def dealer_algo(self):
		if get_hand_value(self.dealer_hand) < 17:
			return 'hit'
		else:
			return 'stay'

	def dealer_visible_card(self):
		return self.dealer_hand[0]

	def record_game(self):
		# take stats
		self.games_played += 1
		if self.check_player_win() == 'win':
			self.games_won += 1
		elif self.check_player_win() == 'tie':
			self.games_tied += 1
		
		# screen print
		if self.verbose:
			self.print_game()

		# log generation
		if self.do_log:
			# win only training set | can be changed to win or tie
			if self.check_player_win() == 'win':
				self.generate_full_log() 
				self.generate_val_log() 
			

############################################
## LOGGING FOR AI 
############################################

	def generate_full_log(self):
	# 0 : unknown (dealer hand or in deck)
	# 1 : dealers card
	# 2 : discard pile
	# 3 : player hand
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
			# write output
			s = ','.join( [str(card_dict[k]) for k in card_order] )
			log_full.write(s+'\n')

			# look at next card				
			card_dict[ self.player_hand[i] ] = 3
			i += 1

		# record a stay : 0
		card_dict['ACTION'] = 0
		
		# write output
		s = ','.join( [str(card_dict[k]) for k in card_order] )
		log_full.write(s+'\n')

	
	def generate_val_log(self):
		# set value of dealer card
		dealer = get_hand_value([ self.dealer_visible_card() ])		
		trash_value = get_hand_value(self.discard_pile)
		trash_count = len(self.discard_pile)
		
		i = 2
		while i < len(self.player_hand):
		# record a hit : 1
			# get hand values
			player = get_hand_value( self.player_hand[:i])
			
			# create two logs (with and without discard)
			val_dp  = '{},{},{}\n'.format(1,dealer,player)
			val_dpt = '{},{},{},{},{}\n'.format(1,dealer,player,trash_value,trash_count)
			log_val_dp.write( val_dp )
			log_val_dpt.write(val_dpt)
			
			# increment i, to consider next card
			i += 1

		# record a stay : 0
		player = get_hand_value( self.player_hand[:i])
		val_dp  = '{},{},{}\n'.format(0,dealer,player)
		val_dpt = '{},{},{},{},{}\n'.format(0,dealer,player,trash_value,trash_count)
		log_val_dp.write( val_dp )
		log_val_dpt.write(val_dpt)

	def print_game(self):
		# print player, hand_value, hand, win
		print 'games played :', self.games_played
		print 'games won    :', self.games_won
		print 'games tied   :', self.games_tied
		print 'dealer hand  :', self.dealer_hand, get_hand_value(self.dealer_hand) 
		print 'player hand  :', self.player_hand, get_hand_value(self.player_hand)
		print 'player wins  :', self.check_player_win()
		print 'cards left   :', self.deck.cards_remaining()
		print 'discard pile :', self.discard_pile, get_hand_value(self.discard_pile)
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


############################################
## HELPER FUNCTIONS
############################################
def sigmoid(z):
	return 1 / (1 + math.e**(-z))

############################################
## PLAYER ALGOS
############################################

def player_lr3(dealer_card, player_hand, discard):
	# logistical regression on wins only, trained by odds
	# input hand, dealer_card, trash_value, trash_count
	# ! 100000 Total Games
	# ! 	42374	 Games Won  42.37%
	# ! 	8462	 Games Tied 8.46%
	# ! 	49164	 Games Lost 49.16%
	# theta0 =  4.264910
	# theta1 =  0.102531
	# theta2 = -0.347303
	# theta3 =  0.020743
	# theta4 = -0.138796
	theta0 =  3.420509
	theta1 =  0.028824
	theta2 = -0.254646
	theta3 =  0.020154
	theta4 = -0.134577
	x1 = get_hand_value(dealer_card)
	x2 = get_hand_value( player_hand )
	x3 = get_hand_value(discard)
	x4 = len(discard)
	predict = sigmoid(theta0 + theta1*x1 + theta2*x2 + theta3*x3 + theta4*x4)
	if predict > .5:
		return 'hit'
	else:
		return 'stay'
 

def player_lr2(dealer_card, player_hand, discard):
	# logistical regression on wins and ties
	# input hand and dealer_card
	# ! 100000 Total Games
	# ! 	41732	 Games Won  41.73%
	# ! 	8693	 Games Tied 8.69%
	# ! 	49575	 Games Lost 49.58%
	theta0 =  3.556079
	theta1 = -0.002270
	theta2 = -0.246408
	x1 = get_hand_value(dealer_card)
	x2 = get_hand_value( player_hand )
	predict = sigmoid(theta0 + theta1*x1 + theta2*x2)
	if predict > .5:
		return 'hit'
	else:
		return 'stay'


 
 

def player_lr1(dealer_card, player_hand, discard):
	# logistical regression on wins only
	# input hand and dealer_card
	# ! 100000 Total Games
	# ! 	41966	 Games Won  41.97%
	# ! 	8698	 Games Tied 8.7%
	# ! 	49336	 Games Lost 49.34%
	theta0 =  3.114547
	theta1 = -0.005880
	theta2 = -0.217994
	x1 = get_hand_value(dealer_card)
	x2 = get_hand_value( player_hand )
	predict = sigmoid(theta0 + theta1*x1 + theta2*x2)
	if predict > .5:
		return 'hit'
	else:
		return 'stay'


def player_odds(dealer_card, player_hand, discard):
	# odds from http://wizardofodds.com/games/blackjack/strategy/1-deck/
	# ! 100000 Total Games
	# ! 	42780	 Games Won  42.78%
	# ! 	9155	 Games Tied 9.15%
	# ! 	48065	 Games Lost 48.06%

	p = get_hand_value(player_hand)
	d = get_hand_value(dealer_card)
	# low and always hit
	if p <= 11:
		return 'hit'
	# high and always stay
	if p >= 17:
		return 'stay'
	# funny 12
	if p == 12 and d <=3:
		return 'hit'
	if p == 12 and d in [4,5,6]:
		return 'stay'
	if p == 12 and d >= 7:
		return 'hit'
	if p >= 13 and d <= 6:
		return 'stay'
	if p >= 13 and d >= 7:
		return 'hit'

def player_hit16(dealer_card, player_hand, discard):
	# hits on 16 or lower
	# ! 100000 Total Games
	# ! 	40758	 Games Won  40.76%
	# ! 	10281	 Games Tied 10.28%
	# ! 	48961	 Games Lost 48.96%
	if get_hand_value(player_hand) <= 16:
		return 'hit'
	else:
		return 'stay'

def player_stay(dealer_card, player_hand, discard):
	# never hits
	# ! 100000 Total Games
	# ! 	37881	 Games Won  37.88%
	# ! 	4864	 Games Tied 4.86%
	# ! 	57255	 Games Lost 57.26%
	return 'stay'

def player_random(dealer_card, player_hand, discard):
	# random player
	# ! 100000 Total Games
	# ! 	18662	 Games Won  18.66%
	# ! 	3558	 Games Tied 3.56%
	# ! 	77780	 Games Lost 77.78%
	return random.choice( ['hit', 'stay'] )





def write(d, a):
	s = ','.join( [str(d[k]) for k in a] )
	f.write(s+'\n')


games   = 100000
do_log  = True
verbose = False
algo    = player_lr3
if do_log:
	log_full    = open('data_full.txt','w+')
	log_val_dp  = open('data_val_dp.txt','w+')
	log_val_dpt = open('data_val_dpt.txt','w+')

T = TABLE(algo, do_log, verbose)

while T.games_played < games:
	T.play_game()
print '! {} Total Games'.format(T.games_played)
print '! \t{}\t Games Won  {}%'.format(T.games_won,  round(100.0 * T.games_won  / T.games_played, 2))
print '! \t{}\t Games Tied {}%'.format(T.games_tied, round(100.0 * T.games_tied / T.games_played, 2))
print '! \t{}\t Games Lost {}%'.format(T.games_played-T.games_tied-T.games_won, round(100.0 * (T.games_played-T.games_tied-T.games_won)/T.games_played,2))

