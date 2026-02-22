# Goal: Take user input, add a $5.00 fee, and print the total.
price_input = input ("What is the item price? ")
delivery_fee = 5
# Something is wrong here!
total = int(price_input) + delivery_fee
print("Your total is: " + str(total))
         
    #the error stems from combinging the price input string and the delivery fee which is an integer. 
    #to solve this issue, we needed to convert the price input into an integer to add the numbers properly, 
    # and then convert the total to a string so we can print it properly
