import functools
import random

from functools import total_ordering
from random import randint

@total_ordering
class Die:
	'''A single rollable die with an arbitrary number of sides'''
	
	def __init__(self, sides):
		self._sides = sides
	
	def __eq__(self, other):
		if self.is_valid(other):
			return self._sides == other._sides
		else:
			return NotImplemented
	
	def __lt__(self, other):
		if self.is_valid(other):
			return self._sides < other._sides
		else:
			return NotImplemented
	
	def __repr__(self):
		return "d%d" % (self._sides)
	
	def is_valid(self, other):
		return hasattr(other, '_sides')
	
	def roll(self, quantity = 1):
		highest = 0
		lowest = self._sides + 1
		values = []
		
		for i in range(quantity):
			value = randint(1, self._sides)
			if value > highest:
				highest = value
			if value < lowest:
				lowest = value
			values.append(value)
		
		return Roll(self, highest, lowest, sum(values), values)

@total_ordering
class DieCount:
	'''Simple tuple connecting a Die with a desired quantity of rolls'''
	
	def __init__(self, die):
		self.die = die
		self.quantity = 0
	
	def __eq__(self, other):
		if self.is_valid(other):
			return self.die == other.die and self.quantity == other.quantity
		else:
			return NotImplemented
	
	def __lt__(self, other):
		if self.is_valid(other):
			return self.die < other.die and self.quantity < other.quantity
		else:
			return NotImplemented
	
	def __repr__(self):
		return "%d%s" % (self.quantity, self.die)
	
	def is_valid(self, other):
		return hasattr(other, 'die') and hasattr(other, 'quantity')

@total_ordering
class Roll:
	'''The result of rolling a single Die an arbitrary number of times'''
	
	def __init__(self, die, highest, lowest, total, values):
		self.die = die
		self.highest = highest
		self.lowest = lowest
		self.total = total
		self.values = values
	
	def __eq__(self, other):
		if self.is_valid(other):
			return self.die == other.die and self.values == other.values and self.total == other.total and self.highest == other.highest and self.lowest == other.lowest
		else:
			return NotImplemented
	
	def __lt__(self, other):
		if self.is_valid(other):
			return self.die < other.die and self.values < other.values and self.total < other.total and self.highest < other.highest and self.lowest < other.lowest
		else:
			return NotImplemented
	
	def is_valid(self, other):
		return hasattr(other, 'die') and hasattr(other, 'highest') and hasattr(other, 'lowest') and hasattr(other, 'total') and hasattr(other, 'values')

class RollType:
	Normal = 0
	Highest = 1
	Lowest = 2

# "Static" instances

d4 = Die(4)
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d20 = Die(20)
d100 = Die(100)
