P=int(input("Enter Principal Amount (in ₹):- "))
R=float(input("Enter Rate of Interest (in %):- "))
T=int(input("Enter Time Period (in years):- "))

SI= (P*R*T)/100  #Simple_Interest
print(f"Simple Interest for the given amount is:- Rs.{SI}")