from datetime import datetime
from copy import copy


log_file = None


def log_init(_config):
	global log_file
	config = copy(_config)
	del config['courier_arrival_dist_fnc']
	filename = 'logs/' + config['strategy'] + '_' + datetime.now().strftime('%d-%m-%Y_%H:%M:%S') + '.events.log'
	log_file = open(filename, 'w+')
	log_obj(config)


def log_obj(obj):
	log_file.write(str(obj) + '\n')


def log_stdout(*args):
	print(*args)


def log_event(event, id, *args):
	global log_file
	msg = "{0:<10} {1:<20} {2:<38} {3}".format(
		datetime.now().strftime('%H:%M:%S'),
		event,
		id,
		' '.join([str(a) for a in args])
	)
	print(msg)
	event = '|'.join([datetime.now().strftime('%H:%M:%S'), event, id] + [str(a) for a in args])
	if log_file:
		log_file.write(event + '\n')


def log_close():
	global log_file
	log_file.close()
