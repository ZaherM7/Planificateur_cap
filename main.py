import random

matrice_de_conversion= [[1,0.955/2,0.955*0.453/2,0.955*0.453*0.487/2],
                        [2/0.955,1,0.453,0.453*0.487],
                        [2/(0.955*0.453),1/0.453,1,0.487],
                        [2/(0.955*0.453*0.487),1/(0.453*0.487),1/0.487,1]]

distances_en_m=[42195,21097,10000,5000]
"""
Les coefficients de la matrice de conversion respectent :
[[marathon_to_marathon, marathon_to_semi,marathon_to_10km,marathon_to_5km],
[semi_to_marathon],[semi_to_semi],...
]
"""

def convertisseur(temps): #permet de convertir le chrono de la forme hh:mm:ss en secondes
    split=temps.split(":")
    if len(split) !=3:
        return -1
    else :
        heures=int(split[0])
        minutes=int(split[1])
        secondes=int(split[2])
        chrono=heures*3600+minutes*60+secondes
        return(chrono)


def convertisseur_inverse(temps): #permet de convertir un chrono en secondes en la forme hh:mm:ss
    heures=str(int(temps//3600))
    minutes=str(int((temps%3600)//60))
    secondes=str(int((temps%3600)%60))
    if len(heures)<2:
        heures="0"+heures
    if len(minutes)<2:
        minutes="0"+minutes
    if len(secondes)<2:
        secondes="0"+secondes
    chrono=heures+":"+minutes+":"+secondes
    return chrono

def definisseur_indice(distance): #indices pour la matrice de conversion
    if distance=="marathon":
        indice=0
    elif distance=="semi":
        indice=1
    elif distance=="10km":
        indice=2
    elif distance=="5km":
        indice=3
    else:
        indice=-1 #indique une erreur
    return indice

def calcul_vma(distance,chrono): #le chrono doit déjà être converti en secondes, la distance en mètres
    """
    Nous allons appliquer différents pourcentages pour le calcul de la VMA selon les critères suivants :
    Inférieur à 30 min 93% VMA
    Entre 31 et 45 min 87% VMA
    Entre 46 min et 1h00 85% VMA
    Entre 1h01 et 1h30 80% VMA
    Entre 1h31 et 2h00 80% VMA
    Entre 2h01 et 2h30 78% VMA
    Entre 2h31 et 3h00 76% VMA
    Entre 3h01 et 3h30 75% VMA
    3h01 et plus 70% VMA
    """
    vitesse=distance/chrono #en mètres par secondes
    if chrono<= 30*60:
        vma=vitesse/0.93
    elif chrono<=45*60:
        vma=vitesse/0.87
    elif chrono<=60*60:
        vma=vitesse/0.85
    elif chrono<=120*60:
        vma=vitesse/0.8
    elif chrono<=150*60:
        vma=vitesse/0.78
    elif chrono<=180*60:
        vma=vitesse/0.76
    else:
        vma=vitesse/0.7
    return vma

def convertisseur_vitesse(vitesse):
    #Fonction qui va convertir une vitesse en m/s en une allure en min/km
    allure_minkm=1000/(60*vitesse)
    minutes=str(int(allure_minkm//1))
    secondes=str(int((allure_minkm%1)*60))
    if len(secondes)<2:
        secondes="0"+secondes
    allure=minutes+":"+secondes
    return allure

        


indice_entree=-1
indice_estimation=-1
while indice_entree==-1:
    distance_entree=input("Choisissez la distance pour laquelle vous avez un chrono de référence : ")
    indice_entree=definisseur_indice(distance_entree)
    if indice_entree==-1:
        print("La distance n'a pas été reconnue, choisissez parmi les suivantes : marathon, semi, 10km, 5km \n")

while indice_estimation==-1:
    distance_estimation=input("Choisissez la distance pour laquelle vous voulez une estimation : ")
    indice_estimation=definisseur_indice(distance_estimation)
    if indice_estimation==-1:
        print("La distance n'a pas été reconnue, choisissez parmi les suivantes : marathon, semi, 10km, 5km")


entree=input("Entrez votre meilleur chrono sur cette distance de référence ("+distance_entree+") : ")
while convertisseur(entree)==-1:
    entree=input("Le format de chrono est incorrect, veuillez le rentrer sous la forme hh:mm:ss \nEntrez votre meilleur chrono sur cette distance de référence ("+distance_entree+") : ")
estimation=convertisseur_inverse(convertisseur(entree)*matrice_de_conversion[indice_entree][indice_estimation])


print("Votre temps estimé sur "+distance_estimation+" est : " + str(estimation))
plan=input("Souhaitez-vous un plan d'entraînement ? (Oui/Non) ")
plan=plan.lower().replace(" ","")

vma=calcul_vma(distances_en_m[indice_entree],convertisseur(entree))
seuil30=0.9*vma
seuil60=0.85*vma
sweetspot=0.95*seuil60

allure_vma=convertisseur_vitesse(vma)
allure_seuil30=convertisseur_vitesse(seuil30)
allure_seuil60=convertisseur_vitesse(seuil60)
allure_sweetspot=convertisseur_vitesse(sweetspot)

#plans classiques
plan_vma=[["10*1'","r1'"],["12*1'","r1'"],["14*1'","r1'"],["semaine_recup","semaine_recup"],["16*1'","r1'"],["18*1'","r1'"],["20*1'","r1'"],["affutage","affutage"]]
plan_seuil30=[]
plan_seuil60=[["4*5'","r1'40\""],["4*6'","r2'"],["4*7'","r2'20\""],["recup","recup"],["4*8'","r2'40\""],["4*9'","r3'"],["4*10'","r3'20\""],["affutage","affutage"]]
plan_sweetspot=[]
SL_marathon=["1h30","1h45","2h","1h45","2h15","2h30","2h","affutage"]
SL_semi=["1h05","1h10","1h15","1h","1h20","1h25","1h30"]
print("Votre VMA est de : "+str(vma)+"m/s ou " + allure_vma + "/km")
print("Votre seuil est de : "+str(seuil60)+"m/s ou " + allure_seuil60 + "/km")

#Création du plan d'entraînement si nécessaire
while plan!="oui" and plan!="non":
    print("La réponse n'a pas été reconnue, veuillez répondre par oui ou non")
    plan=input("Souhaitez-vous un plan d'entraînement ? (Oui/Non)")
    plan=plan.lower().replace(" ","")

if plan=="oui":
    nom=input("Entrez le nom souhaité pour le plan : ")
    fichier=open(nom+".txt","x")
    allure_intensite=allure_seuil60
    plan_intensite=plan_seuil60
    #Revoir pour adapter une intensité en fonction de la distance et demander à l'utilisateur s'il a une préférence 
    if distance_estimation=="5km" or distance_estimation=="10km":
        fichier.write("PLAN D'ENTRAINEMENT "+distance_estimation.upper()+" EN 8 SEMAINES \n\n")
        for semaine in range (1,9):
            if semaine==4:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 30min EF\n")
                fichier.write("Séance 2 : 30min EF\n")
                fichier.write("Séance 3 : 1h EF\n")
            elif semaine==8:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 30min EF\n")
                fichier.write("Séance 2 : 45min EF\n")
                fichier.write("Séance 3 : COURSE\n")
            else:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 30min EF\n")
                fichier.write("Séance 2 : "+ plan_intensite[semaine-1][0] +" @" + allure_intensite + " " + plan_intensite[semaine-1][1] +"\n")
                fichier.write("Séance 3 : 1h EF\n")
    if distance_estimation=="semi" or distance_estimation=="marathon":
        if distance_estimation=="semi":
            SL=SL_semi
        else:
            SL=SL_marathon
        fichier.write("PLAN D'ENTRAINEMENT "+distance_estimation.upper()+" EN 8 SEMAINES \n\n")
        for semaine in range (1,9):
            if semaine==4:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 30min EF\n")
                fichier.write("Séance 2 : 45min EF\n")
                fichier.write("Séance 3 : "+ SL[semaine-1] +" EF\n")
            elif semaine==8:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 45min EF\n")
                fichier.write("Séance 2 : 45min EF\n")
                fichier.write("Séance 3 : COURSE\n")
            else:
                fichier.write("\n--- Semaine "+str(semaine)+" ---\n")
                fichier.write("Séance 1 : 1h EF\n")
                fichier.write("Séance 2 : "+ plan_intensite[semaine-1][0] +" @" + allure_intensite + " " + plan_intensite[semaine-1][1] +"\n")
                fichier.write("Séance 3 : "+ SL[semaine-1] +" EF\n")
    fichier.close()

    



