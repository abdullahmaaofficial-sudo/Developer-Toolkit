from random import choices,shuffle

ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
SIGNS = "/;!@#$%^&*()_}{~><?-=+"
DIGITS = '0123456789'

print("========== Password Generator ==========")
print("Guide (1-2-4-5): capital alphabets,small alphabets amount, signs amount, digits amount\n")

while True:
    user_input = input("Enter a range like this (1-2-4-5), Enter anything to quit: ")

    try:
       c_alphabets_amount,alphabets_amount,signs_amount,digits_amount = user_input.split('-') 
    except:
        print("Program Ended")
        break

    selected_signs = ''.join(choices(SIGNS, k = int(signs_amount)))
    selected_alphabets = ''.join(choices(ALPHABETS, k = int(alphabets_amount)))
    selected_c_alphabets = ''.join(choices(ALPHABETS.upper(), k = int(c_alphabets_amount)))
    selected_digits = ''.join(choices(DIGITS, k = int(digits_amount)))

    password = [x for x in f"{selected_c_alphabets}{selected_alphabets}{selected_signs}{selected_digits}"]
    # print(f"Before Shuffle: {password}")
    shuffle(password)

    print(f"Generated Password: {''.join(password)}")
    print(f"Length of password: {len(password)}")
