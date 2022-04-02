print("This program if for calculating your Body Mass Index (BMI)")
print('')
name = input("Please enter your first name: ")
print("Choose either option 1 or 2: \n")

print("1. Weight in pounds, height in inches")
print("2. Weight in kilograms, height in meters\n")

choice = int(input("Choice: "))

if choice == 1:
    stringWeight = "pounds"
    stringHeight = "inches"
elif choice == 2:
    stringWeight = "kilograms"
    stringHeight = "meters"
else:
    print("Choice not accepted!")
    exit()


weight = float(input("\nWeight in " + str(stringWeight) + ": "))
height = float(input("\nHeight in " + str(stringHeight) + ": "))


if choice == 1:
    float(weight)*2.20462
    float(height)*39.3701
    BMI = float(weight/(height**2)*703)
elif choice == 2:
    BMI = float(weight/(height**2))

if(BMI>= 18.5 and BMI<= 24.9):
        print("")
        print (name,"you have a healthy body mass index ratio.")
        print("Continue your healthy habits!")
elif(BMI >= 25 and BMI <= 29.9):
        print("")
        print (name,"you are slighty overweight.")
        print("Try to get more physical activity or start with a simple weightloss diet ")
elif(BMI < 18.5):
        print('')
        print(name,'you are underweight.')
        print("Try eating more frequently and eat foods with more nutrients and carbs")
else:
        print('')
        print (name,'you are OBESE.')
        print ('This is not good. Make an apointment with a doctor to devise a plan for a healthier lifestyle as soon as possible. Continuing obesity can lead to some serious health problems, high blood pressure, strokes and more ')


        
print('')
print('')
print('Thanks for using our BMI calculator.\n')
print('Remember: Health is Wealth' )