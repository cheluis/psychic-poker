class Card():
	def __init__(self, face, suite):
		#Suite of the Card (Club, Spade, Hearts, Diamond)
		self.suite = suite
		#2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A
		self.face = str(face)
		try:
			#A value given to every face of the card
			self.value = int(face)
		except ValueError:
			if face == 'T':
				self.value = 10
			if face == 'J':
				self.value = 11
			if face == 'Q':
				self.value = 12
			if face == 'K':
				self.value = 13
			if face == 'A':
				self.value = 14

	def get_suite(self):
		return self.suite
	
	def get_value(self):
		return self.value

	def get_face(self):
		return self.face

class Hand():
	FACE_VALUES = {14:'A', 13:'K', 12:'Q', 11:'J', 10:'T', 9:'9', 8:'8', 7:'7', 6:'6', 5:'5', 4:'4', 3:'3', 2:'2'}
	#size of the poker hand
	SIZE_HAND = 5
	#Height give to any of the possible poker hands
	STRAIGHT_FLUSH_SCORE = 8
	FOUR_OF_A_KIND_SCORE = 7
	FULL_HOUSE_SCORE = 6
	FLUSH_SCORE = 5
	STRAIGHT_SCORE = 4
	THREE_OF_A_KIND_SCORE = 3
	TWO_PAIRS_SCORE = 2
	ONE_PAIR_SCORE = 1
	HIGHER_CARD_SCORE = 0

	def __init__(self, hand_cards, desk_cards):
		self.hand_value = 0
		self.arr_hand = hand_cards
		self.arr_desk = desk_cards
		self.best_hand = []


	def get_hand_value(self):
		return self.hand_value

	"""
	String representation of the hand FaceSuite
	"""
	def to_string(self, cards):
		output = ''
		for card in cards:
			output = output + self.FACE_VALUES[card.get_value()]+card.get_suite()+" "
		return output

	"""
	Sort the array of cards by the value given to every card
	"""
	def sort(self, arr):
		arr.sort(key = lambda x: x.value, reverse = False)

	"""
	Check if a pair is on the hand
	"""
	def is_one_pair(self, hand):
		for i in range(0, self.SIZE_HAND - 1):
			if hand[i].get_value() == hand[i+1].get_value():
				return True 
		return False

	"""
	Check if a three of a kind is on the hand
	"""
	def is_three_of_a_kind(self, hand):
		for i in range(0, self.SIZE_HAND - 2):
			if hand[i].value == hand[i + 1].value and hand[i].value == hand[i + 2].value:
				return True 
		return False

	"""
	Check if a poker is on the hand
	"""
	def is_four_of_a_kind(self, hand):
		for i in range(0, self.SIZE_HAND - 3):
			if hand[i].value == hand[i + 1].value and hand[i].value == hand[i + 2].value and hand[i].value == hand[i + 3].value:
				return True 
		return False

	"""
	Checks if exists two pairs on the hand
	"""
	def is_two_pairs(self, hand):
		for i in range(0, self.SIZE_HAND - 1):
			if hand[i].value == hand[i + 1].value:
				for j in range(i+2, self.SIZE_HAND - 1):
					if hand[j].value == hand[j + 1].value:
						return True 
		return False

	def is_flush(self, hand):
		for i in range(1, self.SIZE_HAND):
			if hand[i].get_suite() != hand[0].get_suite():
				return False 
		return True


	def is_straight(self, hand):
		if hand[1].get_value() == (hand[0].get_value() + 1) % 15 and hand[2].get_value() == (hand[0].get_value() + 2) % 15 and hand[3].get_value() == (hand[0].get_value() + 3) % 15 and hand[4].get_value() == (hand[0].get_value() + 4) % 15:
			return True
		if hand[0].get_value() == 0 and hand[1].get_value() == 1 and hand[2].get_value() == 2 and hand[3].get_value() == 3 and self.arr_hand[4].get_value() == 12:
			return True
		return False

	def is_full_house(self, hand):
		if (hand[0].get_value() == hand[1].get_value() and hand[0].get_value() == hand[2].get_value()) and (hand[3].get_value() == hand[4].get_value()):
			return True
		return False

	def is_straight_flush(self, hand):
		return self.is_straight(hand) and self.is_flush(hand)

	def get_best_hand(self):
		return self.best_hand

	def calc_best_hand(self):
		self.sort(self.arr_hand)
		arr_res_hand = [Card(0, 0) for x in range(0, self.SIZE_HAND)]
		for i in range(0, self.SIZE_HAND):
			aux_card = Card(self.arr_desk[i].get_value(), self.arr_desk[i].get_suite())
			arr_res_hand[i] = aux_card
			self.calc_hands(arr_res_hand, i+1, 0)


	def calc_hands(self, res, start, end):
		if start == 5:
			solution_hand = []
			for i in range(0, self.SIZE_HAND):
				solution_hand.append(res[i])
			self.sort(solution_hand)
			if self.is_straight_flush(solution_hand) and self.hand_value < self.STRAIGHT_FLUSH_SCORE:
				#print "es escalera de color "+self.to_string(solution_hand)
				self.hand_value = self.STRAIGHT_FLUSH_SCORE
				self.best_hand = solution_hand
			elif self.is_four_of_a_kind(solution_hand) and self.hand_value < self.FOUR_OF_A_KIND_SCORE:
				#print "es poker "+self.to_string(solution_hand)
				self.hand_value = self.FOUR_OF_A_KIND_SCORE
				self.best_hand = solution_hand
			elif self.is_full_house(solution_hand) and self.hand_value < self.FULL_HOUSE_SCORE:
				#print "es full "+self.to_string(solution_hand)
				self.hand_value = self.FULL_HOUSE_SCORE
				self.best_hand = solution_hand
			elif self.is_flush(solution_hand) and self.hand_value < self.FLUSH_SCORE:
				#print "es color "+self.to_string(solution_hand)
				self.hand_value = self.FLUSH_SCORE
				self.best_hand = solution_hand
			elif self.is_straight(solution_hand) and self.hand_value < self.STRAIGHT_SCORE:
				#print "es seguidilla "+self.to_string(solution_hand)
				self.hand_value = self.STRAIGHT_SCORE
				self.best_hand = solution_hand
			elif self.is_three_of_a_kind(solution_hand) and self.hand_value < self.THREE_OF_A_KIND_SCORE:
				#print "es trio "+self.to_string(solution_hand)
				self.hand_value = self.THREE_OF_A_KIND_SCORE
				self.best_hand = solution_hand
			elif self.is_two_pairs(solution_hand) and self.hand_value < self.TWO_PAIRS_SCORE:
				#print "es dos pares "+self.to_string(solution_hand)
				self.hand_value = self.TWO_PAIRS_SCORE
				self.best_hand = solution_hand
			elif self.is_one_pair(solution_hand) and self.hand_value < self.ONE_PAIR_SCORE:
				#print "es par "+self.to_string(solution_hand)
				self.hand_value = self.ONE_PAIR_SCORE
				self.best_hand = solution_hand
			return
		for i in range(end, self.SIZE_HAND):
			res[start] = self.arr_hand[i]
			self.calc_hands(res, start + 1, i + 1)
		return


class FileParser():

	def __init__(self, file):
		self.file = file
		self.file_handler = ''

	def open_file(self):
		self.file_handler = open(self.file, 'r')

	def read_games(self):
		self.open_file()
		games = []
		for line in self.file_handler:
			#print line
			cards = self.read_cards(line)
			games.append(cards)
		return games

	def read_cards(self, line):
		aux_line = line.split(" ")
		cards = []
		for card in aux_line:
			#print card + "/"
			cards.append(Card(card[0], card[1]))
		return cards


class PsychicPoker():

	POSSIBLE_HANDS_VALUE = {0:'high-card', 1:'one-pair', 2:'two-pairs', 3:'three-of-a-kind', 4:'straight', 5:'flush', 6:'full-house', 7:'four-of-a-kind', 8:'straight-flush'}

	def __init__(self, file):
		self.parser = FileParser(file)
		self.advice_best_hand_player()

	def advice_best_hand_player(self):
		hand = []
		deck = []
		games = self.parser.read_games()
		for game in games:
			hand = game[0:5]
			desk = game[5:10]
			hand_handler = Hand(hand, desk)
			hand_handler.calc_best_hand()
			print "Hand %s Deck %s Best Hand %s (%s) " % (hand_handler.to_string(hand), hand_handler.to_string(desk), hand_handler.to_string(hand_handler.get_best_hand()), self.POSSIBLE_HANDS_VALUE[hand_handler.get_hand_value()])


p = PsychicPoker('inputs.txt')