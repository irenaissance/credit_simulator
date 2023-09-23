import os
from credit_simulation import vehicle as vehicle
import sys


class CreditMenu:
    def __init__(self):
        self.totalStep = 7
        self.stepNumber = 0
            
        self.vehicleType = ""
        self.vehicleCondition = ""
        self.vehicleYear = ""
        self.totalLoan = ""
        self.tenor = ""
        self.totalDownPayment = ""
        
    def run(self):
        userInput=None
        while self.stepNumber <= self.totalStep:
            isAllowNextStep=True
            if(self.stepNumber==0):
                vehicleType = input("Input Jenis Kendaraan Motor|Mobil (Alphabet, Ignore Cased)) : ")
                if(vehicle.Vehicle.isVehicleTypeValid(vehicleType) == False):
                    isAllowNextStep=False
            elif(self.stepNumber==1):
                vehicleCondition = input("Input Kendaraan Bekas|Baru. (Alphabet, Ignore Cased) : ")
                if(vehicle.Vehicle.isVehicleConditionValid(vehicleCondition) == False):
                    isAllowNextStep=False
            elif(self.stepNumber==2):
                isValidVehicleYearInput=True
                
                vehicleYear = input("Input Tahun Kendaraan (Numeric, 4 Digit) : ");
                
                if(vehicleYear.isnumeric() and len(vehicleYear)==4):
                    if(vehicle.Vehicle.isVehicleYearValid(vehicleCondition,int(vehicleYear)) == False):
                        isValidVehicleYearInput=False
                else:
                    isValidVehicleYearInput=False
                    
                if(isValidVehicleYearInput==False):
                    isAllowNextStep=False
                
            elif(self.stepNumber==3):
                isValidTotalLoanInput=True
                
                totalLoan = input("Input Jumlah Pinjaman Total. (Numeric <= 1 miliyar) : ");
                
                if(totalLoan.isnumeric()):
                    if(vehicle.Vehicle.isTotalLoanValid(int(totalLoan)) == False):
                        isValidTotalLoanInput=False
                else:
                    isValidTotalLoanInput=False
                    
                if(isValidTotalLoanInput==False):
                    isAllowNextStep=False
                    
            elif(self.stepNumber==4):
                isValidTenorInput = True
                
                tenor = input("Input Tenor Pinjaman 1-6 thn. : ");
                
                if(tenor.isnumeric()):
                    if(vehicle.Vehicle.isTenorValid(int(tenor)) == False):
                        isValidTenorInput=False
                else:
                    isValidTenorInput=False

                if(isValidTenorInput==False):
                    isAllowNextStep=False
            elif(self.stepNumber==5):
                isValidTotalDownPaymentInput = True

                totalDownPayment = input("Input Jumlah DP : ");


                if(totalDownPayment.isnumeric()):
                    if(vehicle.Vehicle.isTotalDownPaymentValid(vehicleCondition,int(totalDownPayment),int(totalLoan)) == False):
                        isValidTotalDownPaymentInput=False
                else:
                    isValidTotalDownPaymentInput=False
                    
                if(isValidTotalDownPaymentInput==False):
                    isAllowNextStep=False
                else:
                    userInput = vehicle.Motorcycle(vehicleCondition, int(vehicleYear), int(totalLoan), int(tenor), int(totalDownPayment)) if vehicleType.lower()=="motor" else vehicle.Car(vehicleCondition, int(vehicleYear), int(totalLoan), int(tenor), int(totalDownPayment))
                    
            elif(self.stepNumber==6):
                
                print("Output Jumlah Cicilan Perbulan : ")
                userInput.printInstallmentSimulation()
            else:
                print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                print("Load Existing Calculation, and automatically display calculation result.")
                print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
                try:
                    data = vehicle.Vehicle.loadExistingCalculation()
                    dataInput = vehicle.Motorcycle(data['vehicleCondition'], int(data['tahunMotor']), int(data['jumlahPinjaman']), int(data['tenorCicilan']), int(data['jumlahDownPayment'])) if data['vehicleType'].lower()=="motor" else vehicle.Car(data['vehicleCondition'], int(data['tahunMobil']), int(data['jumlahPinjaman']), int(data['tenorCicilan']), int(data['jumlahDownPayment']))
                    dataInput.printInstallmentSimulation()
                except ValueError as ve:
                    print(ve)
                reCalculate=''
                print("\n\n")
                while(reCalculate.lower() != 'y' and reCalculate.lower() != 'n'):
                    reCalculate = input("Do you want to recalculate ? Y/N : ");
                if(reCalculate.lower()=='y'):
                    os.system('clear')
                    self.stepNumber=-1
                else:
                    return
            if(isAllowNextStep):
                self.stepNumber+=1




if __name__=="__main__":
    
    if(len(sys.argv)==2):
        filename = sys.argv[1]
        inputFromFile=[]
        with open(sys.argv[1]) as filename:
            for line in filename:
                inputFromFile.append(line.replace("\n",""))
        if(len(inputFromFile)!=6):
            print("===============================================================")
            print("Insufficient Information or Extra Information Detected ...")
            print("===============================================================")
        else:
            print("===============================================================")
            print(f"{inputFromFile[0].upper()} Installment Simulation ...")
            print("===============================================================")
            print(f"Vehicle Condition : {inputFromFile[1].upper()}\nVehicle Year : {inputFromFile[2]}\nTotal Loan : {inputFromFile[3]}\nTenor : {inputFromFile[4]}\nTotal Down Payment : {inputFromFile[5]}")
            print("===============================================================")
            userInput = vehicle.Motorcycle(inputFromFile[1], int(inputFromFile[2]), int(inputFromFile[3]), int(inputFromFile[4]), int(inputFromFile[5])) if inputFromFile[0].lower()=="motor" else vehicle.Car(inputFromFile[1], int(inputFromFile[2]), int(inputFromFile[3]), int(inputFromFile[4]), int(inputFromFile[5]))
            userInput.printInstallmentSimulation()
            print("===============================================================")
                    
    else:
        CreditMenu().run()




