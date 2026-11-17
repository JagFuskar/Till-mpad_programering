import csv
import os
import locale
from colorama import Fore, Style, init

COLUMNS = ["id", "name", "desc", "price", "quantity"]


def truncate(text, length):
   if len(text) > length:
      return text[:length - 3] + "..."
   else:
      return text

def format_currency(value):
   return locale.currency(value,grouping=True)


def parse_price(text):
   price = float(text.replace(",", "."))
   if price < 0:
      raise ValueError("ogiltigt pris")
   return price


def parse_quantity(text):
   quantity = int(text)
   if quantity < 0:
      raise ValueError("ogiltigt antal")
   return quantity


def quantity_color(quantity):
   if quantity < 5:
      return Fore.RED
   else:
      return Fore.GREEN


def list_products(products):
   bar = Fore.CYAN + "│" + Style.RESET_ALL

   print(Fore.CYAN + f"┌{'─' * 5}┬{'─' * 27}┬{'─' * 42}┬{'─' * 16}┬{'─' * 8}┐")
   print(Fore.CYAN + Style.BRIGHT + f"│ {'#':>3} │ {'Namn':<25} │ {'Beskrivning':<40} │ {'Pris':>14} │ {'Antal':>6} │")
   print(Fore.CYAN + f"├{'─' * 5}┼{'─' * 27}┼{'─' * 42}┼{'─' * 16}┼{'─' * 8}┤")

   for nr, product in enumerate(products, start=1):

      name = truncate(product['name'], 25)
      desc = truncate(product['desc'], 40)
      price = format_currency(product['price'])
      quantity = product['quantity']
      color = quantity_color(quantity)

      print(f"{bar} {Fore.CYAN}{nr:>3} {bar} {name:<25} {bar} {desc:<40} {bar} {Fore.YELLOW}{price:>14} {bar} {color}{quantity:>6} {bar}")

   print(Fore.CYAN + f"└{'─' * 5}┴{'─' * 27}┴{'─' * 42}┴{'─' * 16}┴{'─' * 8}┘")


def print_info_row(label, text, color=""):
   bar = Fore.CYAN + "│" + Style.RESET_ALL
   text = truncate(str(text), 66)

   print(f"{bar} {Fore.CYAN}{label:<13} {bar} {color}{text:<66} {bar}")


def view_product(nr, products):
   os.system('cls')

   product = products[nr - 1]
   price = format_currency(product['price'])
   quantity = str(product['quantity']) + " st"
   color = quantity_color(product['quantity'])
   bar = Fore.CYAN + "│" + Style.RESET_ALL

   print(Fore.CYAN + f"┌{'─' * 84}┐")
   print(f"{bar} {Fore.CYAN}{Style.BRIGHT}{'PRODUKTINFO':^82} {bar}")
   print(Fore.CYAN + f"├{'─' * 15}┬{'─' * 68}┤")
   print_info_row("Id", product['id'])
   print_info_row("Namn", product['name'])
   print_info_row("Beskrivning", product['desc'])
   print_info_row("Pris", price, Fore.YELLOW)
   print_info_row("Antal", quantity, color)
   print(Fore.CYAN + f"└{'─' * 15}┴{'─' * 68}┘")


def new_product(products):
   os.system('cls')

   name = input("Namn: ")
   desc = input("Beskrivning: ")
   price = parse_price(input("Pris: "))
   quantity = parse_quantity(input("Antal: "))

   new_id = 0
   for product in products:
      if product['id'] >= new_id:
         new_id = product['id'] + 1

   products.append(
         {
            "id": new_id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
         }
   )

   print(Fore.GREEN + f"{name} lades till")


def edit_product(nr, products):
   os.system('cls')

   product = products[nr - 1]

   print(Fore.YELLOW + "Tryck bara Enter för att behålla det gamla värdet")

   name = input(f"Namn ({product['name']}): ")
   desc = input(f"Beskrivning ({product['desc']}): ")
   price = input(f"Pris ({product['price']}): ")
   quantity = input(f"Antal ({product['quantity']}): ")

   new_price = None
   if price != "":
      new_price = parse_price(price)

   new_quantity = None
   if quantity != "":
      new_quantity = parse_quantity(quantity)

   if name != "":
      product['name'] = name
   if desc != "":
      product['desc'] = desc
   if new_price is not None:
      product['price'] = new_price
   if new_quantity is not None:
      product['quantity'] = new_quantity

   print(Fore.GREEN + f"{product['name']} ändrades")


def remove_product(nr, products):
   product = products[nr - 1]

   answer = input(f"Vill du ta bort {product['name']}? [j/n] ")

   if answer.lower() == "j":
      products.remove(product)
      print(Fore.GREEN + f"{product['name']} togs bort")


def load_data(filename):
   products = []

   try:
      with open(filename, 'r', encoding='utf-8-sig') as file:
         reader = csv.DictReader(file)

         if reader.fieldnames is None:
            return products

         for column in COLUMNS:
            if column not in reader.fieldnames:
               print(Fore.RED + f"Filen saknar kolumnen {column}, ingen data lästes in")
               return products

         for row in reader:
            try:
               product_id = int(row['id'])
               name = row['name']
               desc = row['desc']
               price = parse_price(row['price'])
               quantity = parse_quantity(row['quantity'])
            except (ValueError, TypeError):
               print(Fore.RED + f"Rad {reader.line_num} i filen hade fel data och hoppades över")
               continue

            products.append(
                  {
                     "id": product_id,
                     "name": name,
                     "desc": desc,
                     "price": price,
                     "quantity": quantity
                  }
            )
   except FileNotFoundError:
      print(Fore.YELLOW + "Hittade ingen produktfil, en ny skapas när du sparar")
   except (UnicodeDecodeError, csv.Error, OSError):
      print(Fore.RED + "Filen kunde inte läsas")
      return []

   return products


def save_data(filename, products):
   try:
      with open(filename, 'w', encoding='utf-8', newline='') as file:
         writer = csv.DictWriter(file, fieldnames=COLUMNS)
         writer.writeheader()
         writer.writerows(products)
   except OSError:
      print(Fore.RED + "Kunde inte spara, är filen öppen i ett annat program?")


init(autoreset=True)
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

filename = os.path.join(os.path.dirname(__file__), 'db_products.csv')

os.system('cls')

products = load_data(filename)


while True:
   list_products(products)

   print(Fore.CYAN + "[#] visa produkt | [L] lägg till | [T] ta bort | [E] ändra | [Q] avsluta")
   option = input("Vad vill du göra? ")

   try:
      if option.isdigit():
         idx = int(option)

         if 0 < idx <= len(products):
            view_product(idx, products)
         else:
            print(Fore.RED + "Det finns ingen produkt med det numret")

      elif option.upper() == "L":
         new_product(products)
         save_data(filename, products)

      elif option.upper() == "T":
         idx = int(input("Vilket nummer vill du ta bort? "))

         if 0 < idx <= len(products):
            remove_product(idx, products)
            save_data(filename, products)
         else:
            print(Fore.RED + "Det finns ingen produkt med det numret")

      elif option.upper() == "E":
         idx = int(input("Vilket nummer vill du ändra? "))

         if 0 < idx <= len(products):
            edit_product(idx, products)
            save_data(filename, products)
         else:
            print(Fore.RED + "Det finns ingen produkt med det numret")

      elif option.upper() == "Q":
         exit(0)

      else:
         print(Fore.RED + "Ogiltigt val")

   except ValueError:
      print(Fore.RED + "Felaktig inmatning, försök igen")

   input()
   os.system('cls')
