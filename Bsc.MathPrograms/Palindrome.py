str_n=input("Enter a word:- ")
if (str_n == str_n[::-1]):
    print(f"The word {str_n} is a Palindrome.")
else:
    print(f"The word {str_n} is not a Palindrome.")