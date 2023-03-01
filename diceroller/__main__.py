import functools
import gi
import diceroller.dice

gi.require_version('Gtk', '4.0')

from functools import total_ordering
from gi.repository import Gtk
from diceroller.dice import DieCount, Roll, RollType, d4, d6, d8, d10, d12, d20, d100

die_counts = []
winBuilder = Gtk.Builder.new_from_file('diceroller\\ui\\window.ui')
butBuilder = Gtk.Builder.new_from_file('diceroller\\ui\\buttons.ui')

def clear_ui():
	die_counts.clear()
	update_equation()
	update_output(RollType.Normal)

def do_roll(rollType):
	rolls = []
	
	for count in die_counts:
		if count.quantity > 0:
			rolls.append(count.die.roll(count.quantity))
	
	individual = []
	intermediate = []
	value = 0
	for roll in rolls:
		individual.append("%s%s" % (roll.die, roll.values))
		
		if rollType == RollType.Normal:
			intermediate.append(roll.total)
			value += roll.total
		elif rollType == RollType.Highest:
			intermediate.append(roll.highest)
			value += roll.highest
		elif rollType == RollType.Lowest:
			intermediate.append(roll.lowest)
			value += roll.lowest
	
	return (individual, intermediate, value)

def format_individual_values(values):
	output = ''
	for v in values:
		if(len(output) > 0):
			output += ' + '
		output += v
	
	return output

def format_intermediate_values(values):
	output = ''
	for v in values:
		if(len(output) > 0):
			output += ' + '
		output += '%s' % v
	
	return output

def update_die_count(die, increment):
	found = False
	
	for count in die_counts:
		if count.die == die:
			found = True
			if not increment:
				count.quantity -= 1
				if count.quantity < 1:
					count.quantity = 0
			else:
				count.quantity += 1
	
	if not found:
		count = DieCount(die)
		count.quantity = 1
		die_counts.append(count)
	
	sorted(die_counts)
	update_equation()

def update_equation():
	new_label = ''
	for count in die_counts:
		if count.quantity > 0:
			if len(new_label) > 0:
				new_label += ' + '
			new_label += '%s' % count
	
	label = winBuilder.get_object('equation')
	label.set_label(new_label)

def update_output(rollType):
	results = do_roll(rollType)
	label = winBuilder.get_object('output')
	
	if results[2] > 0:
		label.set_label('%s -> %s = %s' % (format_individual_values(results[0]), format_intermediate_values(results[1]), results[2]))
	else:
		label.set_label('')

def wire_die_button(button, die):
	right = Gtk.GestureClick()
	right.set_button(3)
	right.connect('pressed', lambda a, b, c, d: update_die_count(die, False))
	
	button.add_controller(right)
	button.connect('clicked', lambda x: update_die_count(die, True))

def on_activate(app):
	# Wire up handlers
	wire_die_button(butBuilder.get_object('button_d4'), d4)
	wire_die_button(butBuilder.get_object('button_d6'), d6)
	wire_die_button(butBuilder.get_object('button_d8'), d8)
	wire_die_button(butBuilder.get_object('button_d10'), d10)
	wire_die_button(butBuilder.get_object('button_d12'), d12)
	wire_die_button(butBuilder.get_object('button_d20'), d20)
	wire_die_button(butBuilder.get_object('button_d100'), d100)
	
	total = butBuilder.get_object('button_total')
	total.connect('clicked', lambda x: update_output(RollType.Normal))
	
	highest = butBuilder.get_object('button_highest')
	highest.connect('clicked', lambda x: update_output(RollType.Highest))
	
	lowest = butBuilder.get_object('button_lowest')
	lowest.connect('clicked', lambda x: update_output(RollType.Lowest))
	
	clear = butBuilder.get_object('button_clear')
	clear.connect('clicked', lambda x: clear_ui())
	
	# Put together the full structure
	buttons = winBuilder.get_object('column')
	buttons.append(butBuilder.get_object('buttons_row'))
	
	win = winBuilder.get_object('main_window')
	win.set_application(app)
	win.set_default_size(375, 275)
	win.present()

app = Gtk.Application(application_id = 'com.github.nemesisx00.diceroller.python')
app.connect('activate', on_activate)
app.run(None)
