def numero_mas_frecuente(lista_numeros):
    if not lista_numeros:
        return None
    
    conteo_numeros = {}
    for numerito in lista_numeros:
        conteo_numeros[numerito] = conteo_numeros.get(numerito, 0) + 1
    
    frecuencia_maxima = max(conteo_numeros.values())
    
    numeros_mas_repetidos = [num for num, freq in conteo_numeros.items() 
                           if freq == frecuencia_maxima]
    
    return min(numeros_mas_repetidos)

# Probemos esta vaina
print("¡Probando la función!")
print(numero_mas_frecuente([1, 3, 1, 3, 2, 1]))  # Debe dar: 1
print(numero_mas_frecuente([4, 4, 5, 5]))        # Debe dar: 4