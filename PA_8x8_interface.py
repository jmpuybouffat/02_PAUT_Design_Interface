t = float(input("Entrez la position t sur la courbe (-30 à 110) : "))
x = t
y = -0.003609404789*t**2 + 0.3901494991*t + 19.70324623
z = -0.005488828669*t**2 + 0.4063509956*t + 322.5637799
print(f"Position PA : x={x:.2f}, y={y:.2f}, z={z:.2f}")
