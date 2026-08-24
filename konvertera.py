
while True:

    try:
        fråga = float(input("Hur många mp/h vill du konvertera till km/h?"))
    except:
        continue


    def mph_to_kmh(x):
        kmh = fråga * 1.60934
        return kmh

    print(f"{fråga}mp/h är {mph_to_kmh(fråga)} km/h")