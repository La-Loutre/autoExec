import subprocess
import signal
from subprocessGenerator import *


##Création du générateur de sous processus
generator=SubprocessGenerator()

## On crée une action de type EMPTY pour le premier cas
## si jamais on lance trop vite. ( juste pour le premier cas)
event=createEvent("EMPTY","5") 

## On crée une action pour le premier cas si 
## on est assez rapide.
## createEvent(partie de chaine rencontrer,action)
event2=createEvent("?","5")


##On crée un tableau d'event
events=[event,event2]

## On crée notre processus addProcess(NOM_EXECUTABLE,events=TABLEAU D'EVENTS)
## il est lancé dès la création . On peut en crée autant que l'on souhaite
generator.addProcess(programmeName="/tmp/test",events=events)

##On bloque notre programme tant que les différents sous processus n'ont pas terminé
result=generator.waitAll()

##On affiche les code d'erreur des différents processus.
## != 0 == ERREUR
print(result)



