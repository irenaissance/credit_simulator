import io
import unittest
from unittest.mock import patch
import credit_simulation.vehicle as vehicle
import credit_menu


class VehicleTest(unittest.TestCase):
    def verify_output(self,user_input,expected_output):
        with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
            with patch('builtins.input', side_effect=user_input):
                credit_menu.CreditMenu().run()
                
            self.assertIn(expected_output, fake_stdout.getvalue())
            
    def test_credit_menu_console_success(self):
        user_input = ['mobil','baru','2023','100000000','3','25000000','n']
        expected_output = f"Output Jumlah Cicilan Perbulan : \n\t tahun 1 : Rp. 2,250,000.00/bln , Suku Bunga : 8.00%\n\t tahun 2 : Rp. 2,432,250.00/bln , Suku Bunga : 8.10%\n\t tahun 3 : Rp. 2,641,423.50/bln , Suku Bunga : 8.60%\n\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nLoad Existing Calculation, and automatically display calculation result.\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\nVehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0.\n\n\n\n"
        self.verify_output(user_input,expected_output)
            
    def test_add_car_success(self):
        #"""Test Add Car Success"""
        actual = vehicle.Car("baru",2023,100000000,3,25000000)
        self.assertEqual(isinstance(actual, vehicle.Car), True)
    def test_add_motorcycle_success(self):
        #"""Test Add Motorcycle Success"""
        actual = vehicle.Motorcycle("baru",2023,100000000,3,25000000)
        self.assertEqual(isinstance(actual, vehicle.Motorcycle), True)
    def test_add_car_baru_vehicleyear_less_than_currentyear_minus_1_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2021,100000000,3,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "VehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0."
        )
    def test_add_car_vehicleyear_more_than_currentyear_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2025,100000000,3,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "VehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0."
        )
    def test_add_motorcycle_baru_vehicleyear_less_than_currentyear_minus_1_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2021,100000000,3,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "VehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0."
        )
    def test_add_motorcycle_vehicleyear_more_than_currentyear_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2025,100000000,3,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "VehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0."
        )
    def test_add_car_tenor_not_between_1_and_6_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2023,100000000,0,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "Tenor value cannot input more than 6 and value cannot be 0."
        )
    def test_add_motorcycle_tenor_not_between_1_and_6_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2023,100000000,0,25000000)
        self.assertEqual(
            str(exception_context.exception),
            "Tenor value cannot input more than 6 and value cannot be 0."
        )
    def test_add_car_bekas_dp_less_than_35_percents_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("bekas",2023,100000000,5,24000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )
    def test_add_motorcycle_bekas_dp_less_than_35_percents_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("bekas",2023,100000000,5,24000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )

    def test_add_car_baru_dp_less_than_25_percents_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2023,100000000,5,24000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )
    def test_add_motorcycle_baru_dp_less_than_25_percents_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2023,100000000,5,24000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )
    def test_add_car_baru_dp_greater_than_total_loan_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2023,100000000,5,100000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )
    def test_add_motorycycle_baru_dp_greater_than_total_loan_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2023,100000000,5,100000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan."
        )
    def test_add_car_baru_total_loan_greater_than_1_miliyar_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Car("baru",2023,1000000001,5,100000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalLoan value cannot input more than 1 miliyar or value cannot be 0."
        )
    def test_add_motorycycle_baru_total_loan_greater_than_1_miliyar_exception(self):
        with self.assertRaises(ValueError) as exception_context:
            actual = vehicle.Motorcycle("baru",2023,1000000001,5,100000000)
        self.assertEqual(
            str(exception_context.exception),
            "TotalLoan value cannot input more than 1 miliyar or value cannot be 0."
        )

if __name__ == '__main__':
    unittest.main()
