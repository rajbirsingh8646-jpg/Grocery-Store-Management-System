# Grocery Store Management System
# Project 74 - Beginner Level

import os

# Initial inventory
DEFAULT_INVENTORY = {
    "Rice": {"price": 50, "stock": 100, "unit": "kg"},
    "Sugar": {"price": 45, "stock": 50, "unit": "kg"},
    "Milk": {"price": 30, "stock": 40, "unit": "L"},
    "Oil": {"price": 150, "stock": 20, "unit": "L"},}

STOCK_FILE = "stock.txt"
BILL_FILE = "bills.txt"


# Load saved inventory or create the initial inventory
def load_inventory():
    inventory = {}

    if not os.path.exists(STOCK_FILE):
        save_inventory(DEFAULT_INVENTORY)
        return {
            name: details.copy()
            for name, details in DEFAULT_INVENTORY.items()
        }

    try:
        with open(STOCK_FILE, "r") as file:
            for line in file:
                parts = line.strip().split(",")

                if len(parts) == 4:
                    name, price, stock, unit = parts
                    inventory[name] = {
                        "price": float(price),
                        "stock": int(stock),
                        "unit": unit
                    }

        if set(inventory) != set(DEFAULT_INVENTORY):
            raise ValueError("Invalid inventory file")

        return inventory

    except (ValueError, OSError):
        print("Stock file invalid. Loading default inventory.")
        inventory = {
            name: details.copy()
            for name, details in DEFAULT_INVENTORY.items()
        }
        save_inventory(inventory)
        return inventory


# Save inventory to stock.txt
def save_inventory(inventory):
    with open(STOCK_FILE, "w") as file:
        for name, details in inventory.items():
            file.write(
                f"{name},{details['price']},"
                f"{details['stock']},{details['unit']}\n"
            )


# Display available stock
def view_stock(inventory):
    print("\n========== AVAILABLE STOCK ==========")
    print(f"{'Item':<12}{'Price':<12}{'Stock':<10}{'Unit'}")

    for name, details in inventory.items():
        print(
            f"{name:<12}"
            f"Rs. {details['price']:<8.2f}"
            f"{details['stock']:<10}"
            f"{details['unit']}"
        )

    print("=====================================")


# Create a new bill
def new_bill(inventory):
    cart = {}
    print("\n========== NEW BILL ==========")
    print("Available items:", ", ".join(inventory.keys()))
    print("Type 'done' when you finish adding items.")

    while True:
        item = input("\nEnter item name: ").strip().title()

        if item.lower() == "done":
            break

        if item not in inventory:
            print(f"Item '{item}' not found in inventory.")
            continue

        try:
            quantity = int(input("Enter quantity: "))

            if quantity <= 0:
                print("Quantity must be greater than zero.")
                continue

        except ValueError:
            print("Invalid quantity. Enter a whole number.")
            continue

        # Include earlier quantities if item is entered again
        cart[item] = cart.get(item, 0) + quantity

    if not cart:
        print("No items selected. Bill cancelled.")
        return

    # Validate the entire cart before changing stock
    valid = True

    for item, quantity in cart.items():
        available = inventory[item]["stock"]

        if quantity > available:
            print(
                f"Insufficient stock for {item}. "
                f"Available: {available}"
            )
            valid = False

    # Do not charge or reduce stock if any item is invalid
    if not valid:
        print("Bill cancelled. Stock remains unchanged.")
        return

    # Calculate subtotal
    subtotal = sum(
        inventory[item]["price"] * quantity
        for item, quantity in cart.items()
    )

    # Apply 10% discount when subtotal is Rs. 1000 or more
    discount = subtotal * 0.10 if subtotal >= 1000 else 0

    # GST is 5% on the amount after discount
    taxable_amount = subtotal - discount
    gst = taxable_amount * 0.05
    total = taxable_amount + gst

    # Display bill
    print("\n========== GROCERY BILL ==========")

    for item, quantity in cart.items():
        price = inventory[item]["price"]
        amount = price * quantity
        print(
            f"{item}: {quantity} x Rs. {price:.2f}"
            f" = Rs. {amount:.2f}"
        )

    print("----------------------------------")
    print(f"Subtotal:       Rs. {subtotal:.2f}")
    print(f"Discount:       Rs. {discount:.2f}")
    print(f"GST (5%):       Rs. {gst:.2f}")
    print(f"Total:          Rs. {total:.2f}")
    print("==================================")

    # Update stock only after a valid bill
    for item, quantity in cart.items():
        inventory[item]["stock"] -= quantity

    save_inventory(inventory)

    # Append every successful bill to bills.txt
    with open(BILL_FILE, "a") as file:
        file.write("\n========== GROCERY BILL ==========\n")

        for item, quantity in cart.items():
            amount = inventory[item]["price"] * quantity
            file.write(
                f"{item}: {quantity} x "
                f"Rs. {inventory[item]['price']:.2f}"
                f" = Rs. {amount:.2f}\n"
            )

        file.write(f"Subtotal: Rs. {subtotal:.2f}\n")
        file.write(f"Discount: Rs. {discount:.2f}\n")
        file.write(f"GST (5%): Rs. {gst:.2f}\n")
        file.write(f"Total: Rs. {total:.2f}\n")
        file.write("==================================\n")

    print("Bill saved successfully in bills.txt")
    print("Updated stock saved in stock.txt")


# Main menu
def main():
    inventory = load_inventory()

    while True:
        print("\n===== GROCERY STORE MANAGEMENT =====")
        print("1. New Bill")
        print("2. View Stock")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            new_bill(inventory)

        elif choice == "2":
            view_stock(inventory)

        elif choice == "3":
            print("Thank you for visiting the grocery store!")
            break

        else:
            print("Invalid menu option. Please choose 1, 2 or 3.")


# Start the program
if __name__ == "__main__":
    main()