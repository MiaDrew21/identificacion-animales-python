"""
Este programa representa hechos mediante diccionarios y conjuntos, y vínculos
entre condiciones y conclusiones mediante tuplas. Después aplica las reglas
para inferir clasificaciones sencillas.
"""

# Cada clave representa un predicado y su valor contiene los animales que cumplen ese hecho.
hechos = {
    "animal": {"perro", "aguila", "guepardo", "tigre", "jirafa", "cebra", "pinguino", "albatros"},
    "tiene_pelo": {"perro", "guepardo", "tigre", "jirafa", "cebra"},
    "da_leche": {"perro"},  # Se usa como característica de la especie, no de un individuo macho.
    "domestico": {"perro"},
    "olfato_desarrollado": {"perro"},
    "tiene_plumas": {"aguila"},
    "pone_huevos": {"aguila"},
    "vuela": {"aguila"},
    "pico_curvo": {"aguila"},
    "garras_fuertes": {"aguila"},

    # Hechos de ejemplo adicionales para representar las reglas de la bióloga.
    "come_carne": {"guepardo", "tigre"},
    "tiene_pezuñas": {"jirafa", "cebra"},
    "color_leonado": {"guepardo"},
    "manchas_oscuras": {"guepardo", "jirafa"},
    "rayas_negras": {"tigre", "cebra"},
    "cuello_largo": {"jirafa"},
    "nada": {"pinguino"},
    "blanco_negro": {"pinguino"},
    "vuela_muy_bien": {"albatros"},
}

# Las tuplas describen vínculos: (predicado, predicado, ..., conclusión).
# Se leen como: si se cumplen todos los predicados de la tupla, se obtiene la conclusión.
reglas = [
    (("tiene_pelo",), "mamifero"),
    (("da_leche",), "mamifero"),
    (("tiene_plumas",), "ave"),
    (("vuela", "pone_huevos"), "ave"),
    (("mamifero", "come_carne"), "carnivoro"),
    (("mamifero", "tiene_pezuñas"), "ungulado"),
    (("carnivoro", "color_leonado", "manchas_oscuras"), "guepardo"),
    (("carnivoro", "rayas_negras"), "tigre"),
    (("ungulado", "cuello_largo", "manchas_oscuras"), "jirafa"),
    (("ungulado", "rayas_negras"), "cebra"),
    (("ave", "nada", "blanco_negro"), "pinguino"),
    (("ave", "vuela_muy_bien"), "albatros"),
    # Reglas adicionales creadas a partir de las entrevistas del equipo:
    (("animal", "tiene_pelo", "domestico", "olfato_desarrollado"), "perro"),
    (("animal", "tiene_plumas", "pone_huevos", "pico_curvo", "garras_fuertes"), "aguila"),
]

def aplicar_reglas(base_hechos, reglas):
    """Aplica las reglas hasta que ya no se agreguen conclusiones nuevas."""
    inferidos = {predicado: set(animales) for predicado, animales in base_hechos.items()}
    cambio = True

    while cambio:
        cambio = False
        for condiciones, conclusion in reglas:
            # Busca animales que aparezcan en todos los predicados de la condición.
            if not condiciones:
                continue
            candidatos = set.intersection(
                *(inferidos.get(condicion, set()) for condicion in condiciones)
            )
            nuevos = candidatos - inferidos.get(conclusion, set())
            if nuevos:
                inferidos.setdefault(conclusion, set()).update(nuevos)
                cambio = True

    return inferidos

def mostrar_hechos(base_hechos):
    print("=== HECHOS REGISTRADOS ===")
    for predicado in sorted(base_hechos):
        animales = ", ".join(sorted(base_hechos[predicado]))
        print(f"{predicado}: {animales}")

def mostrar_reglas(lista_reglas):
    print("\n=== REGLAS REPRESENTADAS CON TUPLAS ===")
    for numero, (condiciones, conclusion) in enumerate(lista_reglas, start=1):
        texto_condiciones = " Y ".join(condiciones)
        print(f"{numero}. SI {texto_condiciones} ENTONCES {conclusion}")

def mostrar_clasificaciones(base_inferida):
    print("\n=== CLASIFICACIONES OBTENIDAS ===")
    clasificaciones = [
        "mamifero", "ave", "carnivoro", "ungulado",
        "guepardo", "tigre", "jirafa", "cebra",
        "pinguino", "albatros", "perro", "aguila"
    ]
    for predicado in clasificaciones:
        animales = sorted(base_inferida.get(predicado, set()))
        if animales:
            print(f"{predicado}: {', '.join(animales)}")

if __name__ == "__main__":
    mostrar_hechos(hechos)
    mostrar_reglas(reglas)
    resultado = aplicar_reglas(hechos, reglas)
    mostrar_clasificaciones(resultado)

    print("\n=== CONSULTAS DE EJEMPLO ===")
    print("¿El perro es mamífero?", "perro" in resultado.get("mamifero", set()))
    print("¿El águila es ave?", "aguila" in resultado.get("ave", set()))
    print("¿El pingüino se identifica como ave?", "pinguino" in resultado.get("ave", set()))
    print("\nNota: los datos son ejemplos didácticos basados en la actividad de clase.")
