from datetime import datetime
from random import uniform
from utils import gen_id, log_event, log_stdout
from defaults import COURIER_ARRIVAL_TIME_MIN, COURIER_ARRIVAL_TIME_MAX


class Delivery:
	"""
	Class used to represent a Delivery system for a Kitchen

	Attributes:
		couriers_fifo: list of couriers for 'fifo' strategy
		couriers_done: list of couriers that already delivered the order
		couriers_matched: dictionary of couriers for 'matched' strategy where key is the order ID and value the courier
		kitchen: the Kitchen object where orders are processed
		action: simulation process
		end_loop: flag for ending the simulation loop
	"""
	def __init__(
			self,
			env,
			kitchen,
			strategy='fifo',
			arrival_time_min=COURIER_ARRIVAL_TIME_MIN,
			arrival_time_max=COURIER_ARRIVAL_TIME_MAX,
			arrival_dist_fnc=uniform
	):
		"""
		Initialize Delivery object
		:param env: simpy simulation environment
		:param kitchen: the Kitchen object where orders are processed
		:param arrival_dist_fnc: fnc(min: int, max: int) random function for generating the arrival time for couriers
		:param arrival_time_min: first parameter for arrival_dist_fnc
		:param arrival_time_max: second parameter for arrival_dist_fnc
		"""
		self.__env = env
		self.couriers_fifo = []
		self.couriers_done = []
		self.couriers_matched = {}
		self.__strategy = strategy
		self.kitchen = kitchen
		self.end_loop = False
		self.action = env.process(self.run())
		self.__arrival_time_min = arrival_time_min
		self.__arrival_time_max = arrival_time_max
		self.__arrival_dist_fnc = arrival_dist_fnc

	def __dispatch_new_courier(self, order):
		arrival_delay = self.__arrival_dist_fnc(self.__arrival_time_min, self.__arrival_time_max)
		courier_id = gen_id()
		if self.__strategy == 'matched':
			log_event('COURIER DISPATCHED', courier_id, 'DELAY', arrival_delay, 'ORDER ASSIGNED', order['id'])
		else:
			log_event('COURIER DISPATCHED', courier_id, 'DELAY', arrival_delay)
		yield self.__env.timeout(arrival_delay)
		if self.__strategy == 'matched':
			log_event('COURIER ARRIVED', courier_id, 'ORDER ASSIGNED', order['id'])
		else:
			log_event('COURIER ARRIVED', courier_id)
		courier = {
			'id': courier_id,
			'arrival_delay': arrival_delay,
			'arrival_time': datetime.now(),
		}
		self.couriers_fifo.append(courier)
		self.couriers_matched[order['id']] = courier

	def dispatch_new_courier(self, order):
		"""
		Dispatch a new courier
		:param order:
		"""
		self.__env.process(self.__dispatch_new_courier(order))

	def pickup_order(self, courier, order):
		"""
		Set the order delivered for the courier
		:param courier: The courier who delivered the order
		:param order: The order delivered
		"""
		courier['delivery_time'] = order['delivered_time']
		courier['wait_time'] = (courier['delivery_time'] - courier['arrival_time']).total_seconds()
		courier['order'] = order
		self.couriers_done.append(courier)
		log_event('ORDER PICKED UP', order['id'], order['name'], "COURIER:", courier['id'])
		log_stdout('           ORDER WAIT TIME: {0} s.'.format(order['wait_time']))
		log_stdout('           COURIER WAIT TIME: {0} s.'.format(courier['wait_time']))

	def run(self):
		while True:
			if (
					self.__strategy == 'fifo' and
					len(self.couriers_fifo) > 0 and
					self.kitchen.has_orders_for_delivery()
			):
				"""
				For 'fifo' strategy pick the first available courier and assign the first order available for delivery
				"""
				courier = self.couriers_fifo.pop(0)
				order = self.kitchen.pickup_first_order_for_delivery()
				self.pickup_order(courier, order)
			elif (
					self.__strategy == 'matched' and
					len(self.couriers_matched.keys()) > 0 and
					self.kitchen.has_orders_for_delivery()
			):
				"""
				For 'matched' strategy.  For the available orders check if the assigned courier is available.
				"""
				delivered = False
				for order in self.kitchen.orders_for_delivery:
					if order['id'] in self.couriers_matched.keys():
						self.kitchen.pickup_order_for_delivery(order)
						self.pickup_order(self.couriers_matched[order['id']], order)
						del self.couriers_matched[order['id']]
						delivered = True
				if not delivered:
					yield self.__env.timeout(0.1)
			else:
				if self.end_loop:
					break
				yield self.__env.timeout(0.1)

	def avg_wait_time(self):
		return sum([c['wait_time'] for c in self.couriers_done]) / len(self.couriers_done)
