import sys
from unittest import TestCase, main
from unittest.mock import patch, Mock
from datetime import datetime

sys.path.append('.')
from models import Kitchen, Delivery


mock_simpy_env = Mock()
mock_simpy_env.timeout = Mock()
mock_simpy_env.process = Mock()
mock_simpy_env.active_process = Mock(return_value=1)
mock_simpy_env.schedule = Mock(return_value=1)


class TestSimulation(TestCase):
	"""Test """

	@patch('builtins.print')
	def test_delivery(self, mock_print):
		mock_kitchen = Mock()
		orders = [
			{'id': '1', 'name': 'test', 'prepTime': 1, 'delivered_time': datetime.now(), 'wait_time': datetime.now()},
			{'id': '2', 'name': 'test', 'prepTime': 1, 'delivered_time': datetime.now(), 'wait_time': datetime.now()},
			{'id': '3', 'name': 'test', 'prepTime': 1, 'delivered_time': datetime.now(), 'wait_time': datetime.now()}
		]
		mock_kitchen.pickup_first_order_for_delivery = Mock(return_value=orders[0])
		mock_kitchen.has_orders_for_delivery = Mock(return_value=True)
		mock_kitchen.orders_for_delivery = orders
		def dist_fnc(x, y): return 1
		delivery = Delivery(mock_simpy_env, mock_kitchen, arrival_dist_fnc=dist_fnc)

		# Empty delivery system
		self.assertEqual(len(delivery.couriers_fifo), 0)
		self.assertEqual(len(delivery.couriers_matched.keys()), 0)
		self.assertEqual(len(delivery.couriers_done), 0)

		# Dispatching a courier: test env call
		delivery.dispatch_new_courier(orders[0])
		mock_simpy_env.process.assert_called()

		# Dispatching a courier: test courier added to list
		for _ in delivery._Delivery__dispatch_new_courier(orders[0]): pass
		mock_print.assert_called()
		mock_print.reset_mock()
		# Check courier in FIFO list
		self.assertEqual(len(delivery.couriers_fifo), 1)
		courier = delivery.couriers_fifo[0]
		self.assertEqual(courier['arrival_delay'], 1)
		self.assertIn('arrival_time', courier)
		# Check courier in MATCHED list
		self.assertEqual(len(delivery.couriers_matched.keys()), 1)
		self.assertEqual(delivery.couriers_matched[orders[0]['id']], courier)

		# Pickup an order for FIFO
		delivery.end_loop = True
		for _ in delivery.run(): pass
		self.assertEqual(len(delivery.couriers_fifo), 0)
		self.assertEqual(len(delivery.couriers_done), 1)
		mock_kitchen.pickup_first_order_for_delivery.assert_called_once()
		self.assertIn('delivery_time', courier)
		self.assertIn('wait_time', courier)
		self.assertIn('order', courier)
		mock_print.assert_called()
		mock_print.reset_mock()

		# Pickup an order for MATCHED
		delivery._Delivery__strategy = 'matched'
		for _ in delivery.run(): pass
		self.assertEqual(len(delivery.couriers_matched.keys()), 0)
		self.assertEqual(len(delivery.couriers_done), 2)
		mock_kitchen.pickup_first_order_for_delivery.assert_called_once()
		self.assertIn('delivery_time', courier)
		self.assertIn('wait_time', courier)
		self.assertIn('order', courier)
		mock_print.assert_called()
		mock_print.reset_mock()


if __name__ == "__main__":
	main()
