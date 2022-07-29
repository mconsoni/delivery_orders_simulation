import simpy
from datetime import datetime
from utils import log_event


class Kitchen:
	"""
	Class used to represent a Kitchen

	Attributes:
		orders: list of pending orders orders
		orders_processing: list of orders that are being processed
		orders_for_delivery: list of orders ready for delivery
		orders_delivered: list of orders already delivered
		action: simulation process
		end_loop: flag for ending the simulation loop
	"""
	def __init__(self, env, num_cooks):
		"""
		Initialize Kitchen object
		:param env: simpy simulation environment
		:param num_cooks: number of cooks available / number of orders that can be processed in parallel
		"""
		self.__env = env
		self.__cooks = simpy.Resource(env, num_cooks)
		self.orders = []
		self.orders_processing = []
		self.orders_for_delivery = []
		self.orders_delivered = []
		self.action = env.process(self.run())
		self.end_loop = False

	def has_orders_for_delivery(self):
		"""
		:return: boolean indicating if there are order ready for delivery
		"""
		return len(self.orders_for_delivery) > 0

	def __pickup_order_for_delivery(self, order):
		order['delivered_time'] = datetime.now()
		order['wait_time'] = (order['delivered_time'] - order['end_time']).total_seconds()
		self.orders_delivered.append(order)
		return order

	def pickup_order_for_delivery(self, order):
		"""
		:param: order to set as delivered
		:return: order with 'delivered_time' and 'wait_time' attributes
		"""
		self.orders_for_delivery.remove(order)
		return self.__pickup_order_for_delivery(order)

	def pickup_first_order_for_delivery(self):
		"""
		Set the first order available for delivery as delivered
		:return: order delivered with 'delivered_time' and 'wait_time' attributes
		"""
		assert(len(self.orders_for_delivery) > 0)
		order = self.orders_for_delivery.pop(0)
		return self.__pickup_order_for_delivery(order)

	def create_order(self, order):
		log_event('ORDER RECEIVED', order['id'], order['name'])
		order['added_time'] = datetime.now()
		self.orders.append(order)

	def run(self):
		while True:
			if len(self.orders) > 0:
				cook = self.__cooks.request()
				yield cook
				order = self.orders.pop(0)
				order['start_time'] = datetime.now()
				self.__env.process(self.process_order(order, cook))
			else:
				if self.end_loop:
					break
				yield self.__env.timeout(0.1)

	def process_order(self, order, cook):
		self.orders_processing.append(order)
		yield self.__env.timeout(order['prepTime'])
		log_event('ORDER PREPARED', order['id'], order['name'])
		order['end_time'] = datetime.now()
		self.orders_processing.remove(order)
		self.orders_for_delivery.append(order)
		self.__cooks.release(cook)

	def avg_wait_time(self):
		return sum([o['wait_time'] for o in self.orders_delivered]) / len(self.orders_delivered)