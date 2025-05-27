from tabulate import tabulate

"""
In the Shoe class, the class is initialised with the parameters country, code, product, cost, quantity.
The class is used to define fuctions for the purpose of searching the cost and quantity of the shoes.
The class is used to define _str_ function that returns a string representation of a class. 
"""

#========The beginning of the class==========
class Shoe:

    #Function to initialise the attributes
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
      
    #Function to return the cost of the shoes
    def get_cost(self):
        return self.cost

    #Function to return the quantity of the shoes   
    def get_quantity(self):
        return self.quantity

    #Function to return a string representation of a class.   
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}\n"


#=============Shoe list===========
#The list will be used to store a list of objects of shoes.
shoe_list = []


#==========Functions outside the class==============

"""
Function to open the inventory.txt file, read the data 
to create a shoe object and append this object into the shoes list.
"""
def read_shoes_data():

    # Try/except is used in case the file does not exist
    try:
        with open("inventory.txt", "r") as file:
            # Skip header line
            lines = file.readlines()[1:] 

            for line in lines:
                parts = line.strip().split(",")
                #Test for malformed lines
                if len(parts) != 5:
                    print(f"Skipping malformed line: {line.strip()}")
                    continue
                # Cast each item into an object and append to object list
                country, code, product, cost, quantity = parts
                shoe = Shoe(country, code, product, int(cost), int(quantity))
                shoe_list.append(shoe)

    except FileNotFoundError as error:
        print("\nSorry, the inventory file does not exist!\n")
        print(error)


"""
Function to overwrite the file
"""
def write_shoes_data():
    with open("inventory.txt", "w") as f:
        f.write("Country,Code,Product,Cost,Quantity\n")
        for shoe in shoe_list:
            f.write(str(shoe) + "\n")


'''
Function to capture data about a shoe and use this data 
to create a shoe object and append this object inside the shoe list.   
'''
def capture_shoes(): 

    # Use try/except in case the file does not exist
    try:
        #Get input from user for new products
        new_country = input("Please enter the country of your product:\n")
        new_code = input("Please enter the code of your product:\n")
        new_product = input("Please enter the name of your product:\n")
        new_cost = int(input("Please enter the cost of your product, only in numbers. E.g. 12345\n"))
        new_quantity = int(input("Please enter the quantity of your product, only in numbers. E.g. 2\n"))

        # Cast each item into an object and append to object list 
        new_shoe = Shoe(new_country, new_code, new_product, new_cost, new_quantity)
        shoe_list.append(new_shoe)

        # Write to file    
        write_shoes_data()
                      
        print("\nThank you, your product has been loaded!\n")
            
    except ValueError:
        print("Invalid input. Please enter numbers for cost and quantity.")

"""
Function for displaying the details of the shoes returned from the __str__ function.   
"""   

def view_all():

    #Get shoe_list by calling the read_shoes_data() function
    #read_shoes_data()
          
    print("\n---------------------------------------------STOCKLIST---------------------------------------------\n")

    #Store the information in shoe_list in seperate list
    table = []
    for shoe in shoe_list:
        row = [shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity]
        table.append(row)

    # Display the information using tabulate 
    print(tabulate(table, headers = ('Country','Code', 'Product', 'Cost', 'Quantity'), tablefmt='fancy_grid'))

    print("\n---------------------------------------------END-------------------------------------------------\n")
    

'''
Function to find the shoe object with the lowest quantity,
get the new quantity and update the textfile
'''
def re_stock():
    #Get lowest quantity
    lowest_shoe = min(shoe_list, key=lambda x: x.quantity)
                          
    print("----------------------------Lowest stock item:----------------------------")

    #Display shoe with lowest quantity
    print(f"\nRestock needed: {lowest_shoe.product} ({lowest_shoe.code}) has {lowest_shoe.quantity} items.")
                    
    print("---------------------------------------------------------------------------")
    print()

    restock = input("Would you like to restock the stock? (Y/N): ").strip().upper()
    if restock == "Y":
        try:
            new_quantity = int(input("\nPlease confirm the new quantity:\n"))
            lowest_shoe.quantity = new_quantity
            write_shoes_data()
            print("\nYour product has been updated!\n")
        except ValueError:
            print("Invalid input. Quantity must be a number.")
         

'''
Function that will search for a shoe from the list
using the shoe code and return this object so that it will be printed.
'''
def search_shoe():

    #Get the shoe code of the wanted shoe
    search_shoe = input("\nPlease enter the shoe code you are searching for: ")

    #Search for the correct code and print the corresponding information
    for shoe in shoe_list:
        if shoe.code == search_shoe:
            print()
            print("----------------------------Found:----------------------------")
            print(f"Country: {shoe.country}, Code: {shoe.code}, Product: {shoe.product}, Cost: {shoe.cost}, Quantity: {shoe.quantity}")
            print("--------------------------------------------------------------") 
            found = True
            break

    if not found:
        print("Shoe not found.")
   
   
'''
Function to calculate the total value for each item.
''' 
def value_per_item():

    print("\n---------------------------------------------VALUE LIST---------------------------------------------\n")


    table = []
    for shoe in shoe_list:
        # Get cost and quantity for product using get_() class methods
        cost = shoe.get_cost()
        quantity = shoe.get_quantity()

        #Calculate the total value of the item and display it
        value = cost * quantity
        table.append([shoe.product, value])
    
    # Display the information using tabulate 
    print(tabulate(table, headers = ('Product','Total Value(R)'), tablefmt='fancy_grid'))    
    print("\n---------------------------------------------END-------------------------------------------------\n")


'''
Function to determine the product with the highest quantity and
print this shoe as being for sale.
''' 
def highest_qty():

    #Determine the highest quantity
    highest_shoe = max(shoe_list, key=lambda s: s.quantity)

    #Display the sales item
    print("\n----------------------------Sale:----------------------------\n")

    print(f"{highest_shoe.product} is now marked on SALE.")

    print("\n-------------------------------------------------------------\n")
    

#==========Main Menu=============
read_shoes_data()

while True:
    print("Welcome to the Inventory System!")
    try:
        menu = int(input('''\n

            Please select an option from the menu below:

            1. Capture Shoes - Add a new shoe.
            2. View All - View the details of each shoe type
            3. Restock - Restock shoe type with lowest quantity
            4. Search - Search for a shoe type accordig to its code
            5. View Item Values - Calculate the total value of each shoe type
            6. View Sale Items - See what shoe type is on sale
            0. Exit             
            \n'''))

        if menu == 1:
            capture_shoes()
            
        elif menu == 2:
            view_all()
            
        elif menu == 3:
            re_stock()
            
        elif menu == 4:
            search_shoe()
            
        elif menu == 5:
            value_per_item()
            
        elif menu == 6:
            highest_qty()

        elif menu == 0:
            print("Exiting the Inventory System.")
            break    
          
        elif menu > 6:
            print('''\nYou have selected an invalid option. Please try again by choosing from the menu below.
                  1. Capture Shoes - Add a new shoe.
                  2. View All - View the details of each shoe type
                  3. Restock - Restock shoe type with lowest quantity
                  4. Search - Search for a shoe type accordig to its code
                  5. View Item Values - Calculate the total value of each shoe type
                  6. View Sale Items - See what shoe type is on sale\n''')

    except ValueError:
        print("\nYou have selected an invalid option. Please try again by entering a number.\n")
        