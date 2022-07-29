import sys
from unittest import TestCase, main
from unittest.mock import patch, Mock

sys.path.append('.')
from models import Kitchen


mock_simpy_env = Mock()
mock_simpy_env.timeout = Mock()
mock_simpy_env.process = Mock()
mock_simpy_env.active_process = Mock(return_value=1)
mock_simpy_env.schedule = Mock(return_value=1)


class TestSimulation(TestCase):
	@patch('builtins.print')
	def test_kitchen(self, mock_print):
		kitchen = Kitchen(mock_simpy_env, 1)
		kitchen.run = lambda x: 1
		order = {'id': '1', 'name': 'test', 'prepTime': 1}
		order2 = {'id': '1', 'name': 'test', 'prepTime': 1}
		order3 = {'id': '1', 'name': 'test', 'prepTime': 1}

		# Empty kitchen
		self.assertEqual(len(kitchen.orders), 0)
		self.assertEqual(len(kitchen.orders_processing), 0)
		self.assertEqual(len(kitchen.orders_for_delivery), 0)
		self.assertEqual(len(kitchen.orders_delivered), 0)
		self.assertEqual(kitchen.has_orders_for_delivery(), False)

		# Order processing
		kitchen.create_order(order)
		self.assertEqual(len(kitchen.orders), 1)
		self.assertEqual(len(kitchen.orders_processing), 0)
		self.assertEqual(len(kitchen.orders_for_delivery), 0)
		self.assertEqual(len(kitchen.orders_delivered), 0)
		self.assertEqual(kitchen.has_orders_for_delivery(), False)
		self.assertIn('added_time', order)
		mock_print.assert_called_once()
		mock_print.reset_mock()

		for _ in kitchen.process_order(order, None): pass
		self.assertEqual(len(kitchen.orders), 1)
		self.assertEqual(len(kitchen.orders_processing), 0)
		self.assertEqual(len(kitchen.orders_for_delivery), 1)
		self.assertEqual(len(kitchen.orders_delivered), 0)
		self.assertEqual(kitchen.has_orders_for_delivery(), True)
		self.assertIn('end_time', order)
		mock_print.assert_called_once()
		mock_print.reset_mock()

		delivered_order = kitchen.pickup_first_order_for_delivery()
		self.assertEqual(len(kitchen.orders), 1)
		self.assertEqual(len(kitchen.orders_processing), 0)
		self.assertEqual(len(kitchen.orders_for_delivery), 0)
		self.assertEqual(len(kitchen.orders_delivered), 1)
		self.assertEqual(kitchen.has_orders_for_delivery(), False)
		self.assertIn('delivered_time', delivered_order)
		self.assertIn('wait_time', delivered_order)
		mock_print.assert_not_called()
		mock_print.reset_mock()

		kitchen.create_order(order2)
		kitchen.create_order(order3)
		for _ in kitchen.process_order(order2, None): pass
		for _ in kitchen.process_order(order2, None): pass
		mock_print.reset_mock()
		delivered_order = kitchen.pickup_order_for_delivery(order2)
		self.assertEqual(len(kitchen.orders), 3)
		self.assertEqual(len(kitchen.orders_processing), 0)
		self.assertEqual(len(kitchen.orders_for_delivery), 1)
		self.assertEqual(len(kitchen.orders_delivered), 2)
		self.assertEqual(kitchen.has_orders_for_delivery(), True)
		self.assertIn('delivered_time', delivered_order)
		self.assertIn('wait_time', delivered_order)
		mock_print.assert_not_called()


if __name__ == "__main__":
	main()
