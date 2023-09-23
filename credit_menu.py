import os
from credit_simulation import vehicle as vehicle
import sys
import locale
locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')

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
                vehicleType = input("Input Jenis Kendaraan Motor|Mobil : ")
                if(vehicle.Vehicle.isVehicleTypeValid(vehicleType) == False):
                    print(">> Invalid Vehicle Type Input, Vehicle Type must be 'motor/mobil'")
                    isAllowNextStep=False
            elif(self.stepNumber==1):
                vehicleCondition = input("Input Kendaraan Bekas|Baru : ")
                if(vehicle.Vehicle.isVehicleConditionValid(vehicleCondition) == False):
                    print(">> Invalid Vehicle Condition Input, Vehicle Condition must be 'baru/bekas'")
                    isAllowNextStep=False
            elif(self.stepNumber==2):
                isValidVehicleYearInput=True
                
                vehicleYear = input("Input Tahun Kendaraan : ");
                
                if(vehicleYear.isnumeric() and len(vehicleYear)==4):
                    if(vehicle.Vehicle.isVehicleYearValid(vehicleCondition,int(vehicleYear)) == False):
                        if(vehicleCondition.lower()=="baru"):
                            print(f">> Invalid Vehicle Year Input, Vehicle Year must not less than {vehicle.Vehicle.year-1}")
                        else:
                            print(f">> Invalid Vehicle Year Input, Vehicle Year must be greater than 1000 and {vehicle.Vehicle.year} and must be Numeric")
                        isValidVehicleYearInput=False
                else:
                    print(f">> Invalid Vehicle Year Input, Vehicle Year must be greater than 1000 and {vehicle.Vehicle.year} and must be Numeric")
                    isValidVehicleYearInput=False
                    
                if(isValidVehicleYearInput==False):
                    isAllowNextStep=False
                
            elif(self.stepNumber==3):
                isValidTotalLoanInput=True
                
                totalLoan = input("Input Jumlah Pinjaman Total : ");
                
                if(totalLoan.isnumeric()):
                    if(vehicle.Vehicle.isTotalLoanValid(int(totalLoan)) == False):
                        print(">> Invalid Total Loan Input, Total Loan must not be 0 and must not greater than 1 miliyar")
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
                        print(">> Invalid Tenor Input, tenor input must be range 1 - 6 years")
                        isValidTenorInput=False
                else:
                    isValidTenorInput=False

                if(isValidTenorInput==False):
                    isAllowNextStep=False
            elif(self.stepNumber==5):
                isValidTotalDownPaymentInput = True
                formattedMinDP = ""
                if(vehicleCondition.lower()=="bekas"):
                    formattedMinDP = locale.format_string("%.f", vehicle.Vehicle.minimumPercentageDownPaymentBekas * int(totalLoan), grouping=True)
                    totalDownPayment = input(f"Input Jumlah DP Minimum is {formattedMinDP}: ");
                else:
                    formattedMinDP = locale.format_string("%.f", vehicle.Vehicle.minimumPercentageDownPaymentBaru * int(totalLoan), grouping=True)
                    totalDownPayment = input(f"Input Jumlah DP Minimum is {formattedMinDP}: ");


                if(totalDownPayment.isnumeric()):
                    formattedTotalLoan = locale.format_string("%.f", int(totalLoan), grouping=True)
                    if(vehicle.Vehicle.isTotalDownPaymentValid(vehicleCondition,int(totalDownPayment),int(totalLoan)) == False):
                        if(vehicleCondition.lower()=="bekas"):
                            print(f">> Invalid Total Down Payment Vehicle Condition Bekas Input, Total Down Payment Input must greater than {formattedMinDP} and less than {formattedTotalLoan}")
                        else:
                            print(f">> Invalid Total Down Payment Vehicle Condition Baru Input, Total Down Payment Input must greater than {formattedMinDP} and less than {formattedTotalLoan}")
                            
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
                    reCalculate = input("Do you want to ReInput for new Simulation ? Y/N : ");
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
