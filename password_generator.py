from random import choices,shuffle

ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
SIGNS = "/.,;!@#$%^&*()_}{`~><?"
NUMBERS = '0123456789'

print("========== Password Generator ==========")
print("Guaid (2-4-5): alphabets amount, signs amount, digits amount\n")

while True:
    user_input = input("Enter a range like this (2-4-5), Enter anything to quit: ")

    try:
        alp,sig,num = user_input.split('-') 
    except:
        print("Program finished")
        break

    if not alp or not sig or not num:
        print("Invalid input, valid input (1-2-3)")
        break

    alpha = ''.join(choices(ALPHABETS, k = int(alp)))
    sign = ''.join(choices(SIGNS, k = int(sig)))
    num = ''.join(choices(NUMBERS, k = int(num)))

    password = [x for x in f"{alpha}{sign}{num}"]
    # print(f"Before Shuffle: {password}")
    shuffle(password)

    print(f"Generated Password: {''.join(password)}")
    print(f"Length of password: {len(password)}")