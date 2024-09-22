def celsius_K():            #Converting Tempertaure from Celsius to Kelvin
    conv_t=temp+273
    return conv_t

def kelvin_C():             #Converting Tempertaure from Kelvin to Celsius
    conv_t=temp-273
    return conv_t

print("---WELCOME TO TEMPERATURE CONVERTER---")
print("1.Celsius to Kelvin\n2.Kelvin to Celsius")

a=int(input("Choose any one option:- "))
if a==1:
    temp=int(input("Enter Temperture to be converetd (in Celsius):- "))
    print(f"The Temperature in Kelvin for the given tempertaure is:- {celsius_K()} K")
elif a==2:
    temp=int(input("Enter Temperture to be converetd (in Kelvin):- "))
    print(f"The Temperature in Celsius for the given tempertaure is:- {kelvin_C()}) C")
else:
    print("ERROR ! Please Choose a valid opiton.")