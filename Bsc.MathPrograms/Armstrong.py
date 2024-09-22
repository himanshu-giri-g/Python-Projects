a=int(input("Enter a Number:- "))
b=str(a)
c=len(b)
sum=0
for i in b:
    sum+= int(i)**c
if sum==a:
    print(f"The No. {a} is an Armstrong Numeber.")
else:
    print(f"The No. {a} is not an Armstrong Numeber.")