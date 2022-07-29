import json
import click
from random import uniform
from defaults import ORDERS_PER_SECOND, COOKS_IN_KITCHEN, COURIER_ARRIVAL_TIME_MAX, COURIER_ARRIVAL_TIME_MIN
from simulation import simulate_orders


@click.command()
@click.option('-o', '--orders_per_second', show_default=True, default=ORDERS_PER_SECOND,
			  help='Number of orders per second for the Kitchen.')
@click.option('-c', '--cooks_in_kitchen', show_default=True, default=COOKS_IN_KITCHEN,
			  help='Number of orders that can be processed in parallel.')
@click.option('-tmin', '--courier_arrival_time_min', show_default=True, default=COURIER_ARRIVAL_TIME_MIN,
			  help='Min time for a courier to arrival.')
@click.option('-tmax', '--courier_arrival_time_max', show_default=True, default=COURIER_ARRIVAL_TIME_MAX,
			  help='Max time for a courier to arrival.')
@click.option('--print_info', is_flag=True, show_default=True, default=False,
			  help='Print Simulation info with Orders and Courier data.')
@click.argument('filename', type=click.Path(exists=True, writable=False, readable=True))
def run(filename, orders_per_second, cooks_in_kitchen, courier_arrival_time_min, courier_arrival_time_max, print_info):
	"""
	Simulate the fulfillment of delivery orders for a kitchen.
	Run 2 simulations;
		1: using the 'FIFO' strategy for couriers where the courier picks up the next available order
		2: using the 'MATCHED' strategy for couriers where each courier has an order assigned and may only pick up that order.
	"""
	# Simulation parameters
	simulation_config = {
		'orders_per_second': orders_per_second,
		'cooks_in_kitchen': cooks_in_kitchen,
		'strategy': 'fifo',
		'courier_arrival_time_min': courier_arrival_time_min,
		'courier_arrival_time_max': courier_arrival_time_max,
		'courier_arrival_dist_fnc': uniform,
		'print_info': print_info
	}
	with open(filename) as f:
		simulation_orders = json.load(f)
		simulate_orders(simulation_orders, simulation_config)
		simulation_config['strategy'] = 'matched'
		simulate_orders(simulation_orders, simulation_config)


if __name__ == '__main__':
	run()
