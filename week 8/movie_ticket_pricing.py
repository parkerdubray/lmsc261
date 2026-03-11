while True:
    user_input = input("How old are you? ")
    if user_input == "quit":
        break
    elif user_input >= "65":
        print("your total is $10")
    elif user_input < "65" and user_input > "12":
        print("your total is $15")
    else: 
     print("your total is $8")