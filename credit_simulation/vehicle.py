import datetime
import time
import requests
import json
import locale
locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

class Vehicle(object):
    maxTotalLoan = 1000000000
    minimumPercentageDownPaymentBaru = 0.25
    minimumPercentageDownPaymentBekas = 0.35
    
    today = datetime.date.today()
    year = today.year
    
    def __init__(self, vehicleCondition,vehicleYear,totalLoan,tenor,totalDownPayment,vehicleBaseInterest):
        self.vehicleCondition = self._is_valid_vehicle_condition(vehicleCondition)
        self.vehicleYear = self._is_valid_vehicle_year(vehicleCondition,vehicleYear)
        self.totalLoan = self._is_valid_total_loan(totalLoan)
        self.totalPrincipalLoan = totalLoan - totalDownPayment
        self.totalNetLoan = self.totalPrincipalLoan
        self.tenor = self._is_valid_tenor(tenor)
        self.totalDownPayment = self._is_valid_total_down_payment(vehicleCondition,totalDownPayment,totalLoan)
        self.vehicleBaseInterest = vehicleBaseInterest

    def _is_valid_vehicle_condition(self, vehicleCondition):
        if(Vehicle.isVehicleConditionValid(vehicleCondition) == False):
            raise ValueError("VehicleCondition value must be [baru/bekas].")
        return vehicleCondition

    def _is_valid_vehicle_year(self, vehicleCondition, vehicleYear):
        if(Vehicle.isVehicleYearValid(vehicleCondition,vehicleYear) == False):
            raise ValueError("VehicleYear value if condition \"baru\" cannot input year less than currentYear - 1 and value must be 4 digits and value cannot start with 0.")
        return vehicleYear

    def _is_valid_total_loan(self, totalLoan):
        if(Vehicle.isTotalLoanValid(totalLoan) == False):
            raise ValueError("TotalLoan value cannot input more than 1 miliyar or value cannot be 0.")
        return totalLoan

    def _is_valid_tenor(self, tenor):
        if(Vehicle.isTenorValid(tenor) == False):
            raise ValueError("Tenor value cannot input more than 6 and value cannot be 0.")
        return tenor

    def _is_valid_total_down_payment(self, vehicleCondition,totalDownPayment,totalLoan):
        if(Vehicle.isTotalDownPaymentValid(vehicleCondition,totalDownPayment,totalLoan) == False):
            raise ValueError("TotalDownPayment value if condition \"bekas\" must greater than equal 35% and if condition \"baru\" must greater than equal 25% and TotalDownPayment value not greater than equal totalLoan.")
        return totalDownPayment
    
    def __str__(self):
        return f"Vehicle Condition : {self.vehicleCondition}\nVehicle Year : {self.vehicleYear}\nVehicleBaseInterest : {self.vehicleBaseInterest}\nTenor : {self.tenor}\nTotal Loan : {self.totalLoan}\nTotal Net Loan : {self.totalNetLoan}\nTotal Principal Loan : {self.totalPrincipalLoan}\nTotal Down Payment : {self.totalDownPayment}"

    def printInstallmentSimulation(self):
        installmentMonthly=0
        installmentYearly=0
        interest=self.vehicleBaseInterest*100

        for i in range(self.tenor):
            self.totalNetLoan = self.totalPrincipalLoan+(self.totalPrincipalLoan * interest/100)
            
            if(i+1 > 1):
                if(i%2==0):
                    interest+=0.5
                else:
                    interest+=0.1
                self.totalPrincipalLoan = self.totalNetLoan - installmentYearly
                self.totalNetLoan = (self.totalPrincipalLoan * interest/100) + self.totalPrincipalLoan
                installmentMonthly = self.totalNetLoan/((12*self.tenor)-((i)*12))
                installmentYearly = installmentMonthly*12
                
            else:
                installmentMonthly = self.totalNetLoan/((12*self.tenor))
                installmentYearly = installmentMonthly*12
            installmentMonthlyInRupiahFormat = locale.format_string("%.2f", installmentMonthly, grouping=True)
            print(f"\t tahun {i+1} : Rp. {installmentMonthlyInRupiahFormat}/bln , Suku Bunga : {interest:.2f}%")

    
    @staticmethod
    def isVehicleTypeValid(vehicleType):
        listVehicleType = ["mobil","motor"]
        return vehicleType.lower() in listVehicleType
    
    @staticmethod
    def isVehicleConditionValid(vehicleCondition):
        listVehicleCondition = ["baru","bekas"]
        return vehicleCondition.lower() in listVehicleCondition
    
    @staticmethod
    def isTotalDownPaymentValid(vehicleCondition,totalDownPayment,totalLoan):
        rate = Vehicle.minimumPercentageDownPaymentBaru if vehicleCondition.lower() == "baru" else Vehicle.minimumPercentageDownPaymentBekas
        minimumDownPayment = rate * totalLoan
        if(totalDownPayment < minimumDownPayment or totalDownPayment >= totalLoan ):
            return False
        else:
            return True

    @staticmethod
    def isTenorValid(tenor):
        return False if (tenor > 6 or tenor < 1) else True

    @staticmethod
    def isVehicleYearValid(condition, vehicleYear):
        if(condition.lower() == "baru" and (vehicleYear > Vehicle.year or vehicleYear < Vehicle.year-1)):
            return False
        elif(vehicleYear > Vehicle.year or vehicleYear < 1000):
            return False
        else:
            return True
        
    @staticmethod
    def isTotalLoanValid(totalLoan):
        if(totalLoan > Vehicle.maxTotalLoan or totalLoan == 0):
            return False
        else:
            return True

    @staticmethod
    def loadExistingCalculation():
        headers = {'content-type': 'application/json'}
        rawResponse = requests.get('http://www.mocky.io/v2/5d06e6ae3000005300051d16', headers=headers)
        jsonResponse = json.loads(str(rawResponse.content.decode("utf-8")).replace(" ","").replace("\n","").replace('"}"','"},"'))
        return jsonResponse['vehicleModel']

class Motorcycle(Vehicle):
    baseInterest = 0.09
    def __init__(self, condition,year,totalLoan,tenor,totalDownPayment):
        super().__init__(condition,year,totalLoan,tenor,totalDownPayment,self.baseInterest)

        
class Car(Vehicle):
    baseInterest = 0.08
    def __init__(self, condition,year,totalLoan,tenor,totalDownPayment):
        super().__init__(condition,year,totalLoan,tenor,totalDownPayment,self.baseInterest)
