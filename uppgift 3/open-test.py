import csv
import subprocess
import locale


def format_currency(value):
   return locale.currency(value,grouping=True)


def list_products(products):
   for nr, product in enumerate(products, start=1):    #börjar på 1 istället för 0

      name = product['name']
      price = format_currency(product['price'])
      quantity = product['quantity']

      print(f"{nr}) {name} \t {price} \t {quantity:<5}")


def get_product(product_id, products):
   for product in products:
      if product['id'] == product_id:
         return product

   return None       #hittade ingen produkt med det id:t


def view_product(nr, products):
   subprocess.run('cls', shell=True)

   product = products[nr - 1]      #listan visas från 1 men börjar på 0

   print(f"Id: \t\t {product['id']}")
   print(f"Namn: \t\t {product['name']}")
   print(f"Beskrivning: \t {product['desc']}")
   print(f"Pris: \t\t {format_currency(product['price'])}")
   print(f"Antal: \t\t {product['quantity']}")


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

   print(f"{name} lades till")


def edit_product(nr, products):
   subprocess.run('cls', shell=True)

   product = products[nr - 1]

   print("Tryck bara Enter för att behålla det gamla värdet")

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

   print(f"{product['name']} ändrades")


def remove_product(nr, products):
   product = products[nr - 1]

   answer = input(f"Vill du ta bort {product['name']}? [j/n] ")

   if answer.lower() == "j":
      products.remove(product)
      print(f"{product['name']} togs bort")


def load_data(filename):
   products = []           #lista

   with open(filename, 'r', encoding='utf-8') as file:       #öppnar en fil med read-rättighet
      reader = csv.DictReader(file)
      for row in reader:
         product_id = int(row['id'])
         name = row['name']
         desc = row['desc']
         price = float(row['price'])
         quantity = int(row['quantity'])

         products.append(
               {
                  "id": product_id,
                  "name": name,
                  "desc": desc,
                  "price": price,
                  "quantity": quantity
               }
         )

   return products


def save_data(filename, products):
   with open(filename, 'w', encoding='utf-8', newline='') as file:     #öppnar en fil med write-rättighet
      writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
      writer.writeheader()
      writer.writerows(products)


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

subprocess.run('cls',shell=True)

products = load_data('db_products.csv')


while True:
   list_products(products)

   print("-" * 140)
   option = input("Vad vill du göra? [# = visa produkt | L = lägg till | T = ta bort | E = ändra | Q = avsluta] ")

   try:
      if option.isdigit(): # om det är siffror
         idx = int(option)

         if 0 < idx <= len(products):
            view_product(idx, products)
         else:
            print("Det finns ingen produkt med det numret")

      elif option.upper() == "L":
         new_product(products)
         save_data('db_products.csv', products)

      elif option.upper() == "T":
         idx = int(input("Vilket nummer vill du ta bort? "))

         if 0 < idx <= len(products):
            remove_product(idx, products)
            save_data('db_products.csv', products)
         else:
            print("Det finns ingen produkt med det numret")

      elif option.upper() == "E":
         idx = int(input("Vilket nummer vill du ändra? "))

         if 0 < idx <= len(products):
            edit_product(idx, products)
            save_data('db_products.csv', products)
         else:
            print("Det finns ingen produkt med det numret")

      elif option.upper() == "Q":
         exit(0)

      else:
         print("Ogiltigt val")

   except ValueError:      #om man skriver bokstäver där det ska vara siffror
      print("Felaktig inmatning, försök igen")

   input() #bara vänta till tangentbordsklick
   subprocess.run('cls', shell=True)
