# ## ACTIVIDAD CONOCIMIENTO
# En una isla remota, hay dos tipos de habitantes: caballeros (knights) y ladrones (knaves). Los caballeros siempre dicen la verdad, mientras que los ladrones siempre mienten.
# Un día, te encuentras con tres habitantes de la isla, A y B (y C), pero no sabes quién es quién. Quieres averiguar qué tipo de habitante es cada uno de ellos:
# Primer escenario:
# **A dice: “Soy un caballero y un ladrón”**
# Segundo escenario:
# **A dice: “Ambos somos ladrones”**
# **B no dice nada**
# Tercer escenario:
# **A dice: “Somos del mismo tipo”**
# **B dice: “Somos de distintos tipos”**
# Cuarto escenario:
# **A dice: “Soy un caballero” o “Soy un ladrón” (pero no sabemos cuál frase dijo)**
# **B dice: “A dijo ‘Soy un ladrón’ ”**
# **B luego dice: “C es un ladrón”**
# **C dice “A es un caballero”**


from logic import *

Acaballero = Symbol("A es un caballero")
Bcaballero = Symbol("B es un caballero")
Ccaballero = Symbol("C es un caballero")

Aladron = Symbol("A es un ladron")
Bladron = Symbol("B es un ladron")
Cladron = Symbol("C es un ladron")
personajes = [Acaballero , Bcaballero , Ccaballero , Aladron, Bladron, Cladron]


print(personajes)

symbols = []



# Solo puede haber una persona, una habitacion y un arma
escenario_1 = And   (
Or(symbols["Acaballero"], symbols ["Aladron"]),
        Not(And(symbols["Acaballero"], symbols ["Aladron"])),
        )
escenario_1.add(
Implication(symbols["Acaballero"],
        And(symbols["Acaballero",symbols["Aladron"]])
    )
)   


escenario_2 = And (
    And(symbols("Acaballero",symbols["Aladron"])),
    Not(And(symbols("Acaballero",symbols["Aladron"]))),
)

escenario_3 = And (
    And(symbols("Acaballero"),symbols("Aladron")),  
     Or(symbols("Bcaballero"),symbols("Bladron")),
     )

escenario_4 = And(
        
    Or(Acaballero,Aladron),
    Not(And(Acaballero,Aladron)),
    Or(Bcaballero,Bladron),
    Not(And(Bcaballero,Bladron)),
    Or(Ccaballero,Cladron), 
    Not(And(Ccaballero,Cladron)),

    Implication(Bcaballero,And(Implication(Acaballero, Aladron), Implication(Aladron, Not(Aladron)))),
    Implication(Bladron,Not(And(Implication(Acaballero, Aladron), Implication(Aladron, Not(Aladron))))),

    Implication(Bcaballero,Cladron),
    Implication(Bladron,Not(Cladron)),

    Implication(Ccaballero,Acaballero),
    Implication(Cladron,Not(Acaballero)),

    )




def check_knowledge(knowledge):
    for symbol in symbols:
        if model_check(knowledge, symbol):
            print(f"{symbol}: SI", "Caballero")
        elif not model_check(knowledge, Not(symbol)):
            print(f"{symbol}: QUIZAS")
