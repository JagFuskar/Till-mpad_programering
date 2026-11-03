import csv
import os
import subprocess
import locale
from colorama import Fore, Style, init


def truncate(text, length):
   if len(text) > length:
      return text[:length - 3] + "..."
   else:
      return text

def format_currency(value):
   return locale.currency(value,grouping=True)


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

   for nr, product in enumerate(products, start=1):    #börjar på 1 istället för 0

      name = truncate(product['name'], 25)
      desc = truncate(product['desc'], 40)
      price = format_currency(product['price'])
      quantity = product['quantity']
      color = quantity_color(quantity)

      print(f"{bar} {Fore.CYAN}{nr:>3} {bar} {name:<25} {bar} {desc:<40} {bar} {Fore.YELLOW}{price:>14} {bar} {color}{quantity:>6} {bar}")

   print(Fore.CYAN + f"└{'─' * 5}┴{'─' * 27}┴{'─' * 42}┴{'─' * 16}┴{'─' * 8}┘")


def get_product(product_id, products):
   for product in products:
      if product['id'] == product_id:
         return product

   return None       #hittade ingen produkt med det id:t


def view_product(nr, products):
   subprocess.run('cls', shell=True)

   product = products[nr - 1]      #listan visas från 1 men börjar på 0
   price = format_currency(product['price'])
   quantity = str(product['quantity']) + " st"
   color = quantity_color(product['quantity'])
   bar = Fore.CYAN + "│" + Style.RESET_ALL

   print(Fore.CYAN + f"┌{'─' * 84}┐")
   print(f"{bar} {Fore.CYAN}{Style.BRIGHT}{'PRODUKTINFO':^82} {bar}")
   print(Fore.CYAN + f"├{'─' * 15}┬{'─' * 68}┤")
   print(f"{bar} {Fore.CYAN}{'Id':<13} {bar} {product['id']:<66} {bar}")
   print(f"{bar} {Fore.CYAN}{'Namn':<13} {bar} {product['name']:<66} {bar}")
   print(f"{bar} {Fore.CYAN}{'Beskrivning':<13} {bar} {product['desc']:<66} {bar}")
   print(f"{bar} {Fore.CYAN}{'Pris':<13} {bar} {Fore.YELLOW}{price:<66} {bar}")
   print(f"{bar} {Fore.CYAN}{'Antal':<13} {bar} {color}{quantity:<66} {bar}")
   print(Fore.CYAN + f"└{'─' * 15}┴{'─' * 68}┘")


def new_product(products):
   subprocess.run('cls', shell=True)

   name = input("Namn: ")
   desc = input("Beskrivning: ")
   price = float(input("Pris: "))
   quantity = int(input("Antal: "))

   if len(products) == 0:
      new_id = 0
   else:
      found_max = max(products, key=lambda product: product['id'])
      max_id = found_max['id']
      new_id = max_id + 1

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
   subprocess.run('cls', shell=True)

   product = products[nr - 1]

   print(Fore.YELLOW + "Tryck bara Enter för att behålla det gamla värdet")

   name = input(f"Namn ({product['name']}): ")
   desc = input(f"Beskrivning ({product['desc']}): ")
   price = input(f"Pris ({product['price']}): ")
   quantity = input(f"Antal ({product['quantity']}): ")

   if name != "":
      product['name'] = name
   if desc != "":
      product['desc'] = desc
   if price != "":
      product['price'] = float(price)
   if quantity != "":
      product['quantity'] = int(quantity)

   print(Fore.GREEN + f"{product['name']} ändrades")


def remove_product(nr, products):
   product = products[nr - 1]

   answer = input(f"Vill du ta bort {product['name']}? [j/n] ")

   if answer.lower() == "j":
      products.remove(product)
      print(Fore.GREEN + f"{product['name']} togs bort")


def load_data(filename):
   products = []           #lista

   try:
      with open(filename, 'r', encoding='utf-8') as file:       #öppnar en fil med read-rättighet
         reader = csv.DictReader(file)
         for row in reader:
            try:
               product_id = int(row['id'])
               name = row['name']
               desc = row['desc']
               price = float(row['price'])
               quantity = int(row['quantity'])
            except (ValueError, KeyError, TypeError):
               print(Fore.RED + "En rad i filen hade fel data och hoppades över")
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
   except (UnicodeDecodeError, csv.Error):
      print(Fore.RED + "Filen kunde inte läsas")

   return products


def save_data(filename, products):
   try:
      with open(filename, 'w', encoding='utf-8', newline='') as file:     #öppnar en fil med write-rättighet
         writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
         writer.writeheader()
         writer.writerows(products)
   except PermissionError:
      print(Fore.RED + "Kunde inte spara, är filen öppen i ett annat program?")


init(autoreset=True)
locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

filename = os.path.join(os.path.dirname(__file__), 'db_products.csv')

subprocess.run('cls',shell=True)

products = load_data(filename)


while True:
   list_products(products)

   print(Fore.CYAN + "[#] visa produkt | [L] lägg till | [T] ta bort | [E] ändra | [Q] avsluta")
   option = input("Vad vill du göra? ")

   try:
      if option.isdigit(): # om det är siffror
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

   except ValueError:      #om man skriver bokstäver där det ska vara siffror
      print(Fore.RED + "Felaktig inmatning, försök igen")

   input() #bara vänta till tangentbordsklick
   subprocess.run('cls', shell=True)
