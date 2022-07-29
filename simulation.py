import simpy
from utils import log_init, log_obj, log_close
from models import Kitchen, Delivery


def process_orders(env, orders, kitchen, orders_per_second, delivery):
	"""
	Process `orders_per_second` orders per second
	:param env: simpy simulation environment
	:param orders: list of orders
	:param kitchen: Kitchen object
	:param orders_per_second: number of order to process per second
	:param delivery: Deliver object

	After processing all orders wait for them to be finished and stop loops
	"""
	for idx, order in enumerate(orders, 1):
		kitchen.create_order(order)
		delivery.dispatch_new_courier(order)
		if idx % orders_per_second == 0:
			yield env.timeout(1)
	env.process(wait_orders(env, kitchen, delivery))


def wait_orders(env, kitchen, delivery):
	"""
	Wait for all the orders to be processed	and stop Kitchen and Delivery loops
	:param env: simpy simulation environment
	:param kitchen: Kitchen object
	:param delivery: Delivery object
	"""
	while (
			len(kitchen.orders) > 0 or
			len(kitchen.orders_processing) > 0 or
			len(kitchen.orders_for_delivery) > 0
	):
		yield env.timeout(0.1)
	kitchen.end_loop = True
	delivery.end_loop = True


def simulate_orders(orders, config):
	"""
	Simulate the fulfillment of delivery orders for a kitchen.
	:param orders: list of order for proccesing
	:param config: configuration object for simulation
			attributes:
				'orders_per_second': int
				'cooks_in_kitchen': int
				'strategy': 'fifo' | 'matched'
				'courier_arrival_time_min': int
				'courier_arrival_time_max': int
				'courier_arrival_dist_fnc': function for generating the time couriers take to arrive
				'print_info': bool: print orders and couriers details of the simulation
	"""
	log_init(config)
	env = simpy.rt.RealtimeEnvironment(initial_time=0, factor=1, strict=True)
	kitchen = Kitchen(env, config['cooks_in_kitchen'])
	delivery = Delivery(
		env,
		kitchen,
		config['strategy'],
		config['courier_arrival_time_min'],
		config['courier_arrival_time_max'],
		config['courier_arrival_dist_fnc']
	)
	env.process(process_orders(env, orders, kitchen, config['orders_per_second'], delivery))
	env.run()
	if config['print_info']:
		print_simulation_info(kitchen, delivery, config)
	print_simulation_result(kitchen, delivery)
	log_obj({
		'avg_order_wait_time': kitchen.avg_wait_time(),
		'avg_courier_wait_time': delivery.avg_wait_time()
	})
	log_close()


def print_orders(orders, title):
	print('-' * 120)
	print('- ' + title)
	print('{0:>37}{1:>25}{2:>5}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10}'.format(
		'ID',
		'Name',
		'Time',
		'Added',
		'Started',
		'Finished',
		'Delivered',
		'Wait'
	))
	for order in orders:
		print('{0:>37}{1:>25}{2:>5}{3:>10}{4:>10}{5:>10}{6:>10}{7:>10.4f}s'.format(
			order.get('id', 'N/A'),
			order.get('name', 'N/A'),
			str(order.get('prepTime', 'N/A')) + 's',
			order.get('added_time', 0).strftime('%H:%M:%S'),
			order.get('start_time', 0).strftime('%H:%M:%S'),
			order.get('end_time', 0).strftime('%H:%M:%S'),
			order.get('delivered_time', 0).strftime('%H:%M:%S'),
			order.get('wait_time')
		))


def print_couriers(couriers, title):
	print('-' * 120)
	print('- ' + title)
	print('{0:>37}{1:>37}{2:>10}{3:>10}{4:>10}'.format(
		'ID',
		'Order ID',
		'Arrival',
		'Delivery',
		'Wait'
	))
	for courier in couriers:
		print('{0:>37}{1:>37}{2:>10}{3:>10}{4:>10.4f}s'.format(
			courier.get('id', 'N/A'),
			courier.get('order', {}).get('id', 'N/A'),
			courier.get('arrival_time', 0).strftime('%H:%M:%S'),
			courier.get('delivery_time', 0).strftime('%H:%M:%S'),
			courier.get('wait_time')
		))


def print_simulation_info(kitchen, delivery, config):
	print('=' * 120)
	print('=== SIMULATION =====' + '='*100)
	print('- STRATEGY: ' + config['strategy'].upper())
	print('- ORDERS PER SECOND: ' + str(config['orders_per_second']))
	print('- COOKS IN KITCHEN: ' + str(config['cooks_in_kitchen']))
	print('- COURIER ARRIVAL MIN TIME: ' + str(config['courier_arrival_time_min']))
	print('- COURIER ARRIVAL MAX TIME: ' + str(config['courier_arrival_time_max']))
	print_orders(kitchen.orders_delivered, 'ORDERS')
	print_couriers(delivery.couriers_done, 'COURIERS')


def print_simulation_result(kitchen, delivery):
	print('=' * 120)
	print('=== RESULTS ========' + '='*100)
	print('AVG ORDER WAIT TIME: {0:.4f}s'.format(kitchen.avg_wait_time()))
	print('AVG COURIER WAIT TIME: {0:.4f}s'.format(delivery.avg_wait_time()))
	print('=' * 120)