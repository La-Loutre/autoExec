import subprocess
import signal
#Ouverture du fichier en écriture (w = write) 
fichier = open("sortie.txt","w")

#Lancement du processus fils (ici programme ls ) et redirection sortie standard
subProcess=subprocess.Popen("ls",stdout=fichier)

#On bloque jusqu'a ce que le processus subProcess termine
subProcess.wait()
fichier.close()

##On regarde si le processus à terminé normalement 
if subProcess.returncode == 0:
    print("Subprocess terminated succefully .")
else:
    print("Subprocess terminated with error . Code ="+str(subProcess.returncode)

