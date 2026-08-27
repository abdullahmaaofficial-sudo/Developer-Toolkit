from random import choices,shuffle

ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
SIGNS = "/.,;:!@#$%^&*()_}{`~><?"
NUMBERS = '0123456789'


try:
    alp_amount = int(input("Enter the amount of alphabets you want: "))
    sig_amount = int(input("Enter the amount of signs you want: "))
    num_amount = int(input("Enter the amount of numbers you want: "))
except:
    print("Please enter a number")


alpha = ''.join(choices(ALPHABETS, k = alp_amount))
sign = ''.join(choices(SIGNS, k = sig_amount))
num = ''.join(choices(NUMBERS, k = num_amount))

password = [x for x in f"{alpha}{sign}{num}"]
# print(f"Before Shuffle: {password}")
shuffle(password)

print(f"Generated Password: {''.join(password)}")
print(f"Length of password: {len(password)}")