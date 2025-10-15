import random

matrice_de_conversion= [[1,0.955/2,0.955*0.453/2,0.955*0.453*0.487/2],
                        [2/0.955,1,0.453,0.487],
                        [2/(0.955*0.453),1/0.453,1,0.487],
                        [2/(0.955*0.453*0.487),1/(0.453*0.487),1/0.487,1]]
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
estimation=convertisseur_inverse(convertisseur(entree)*matrice_de_conversion[indice_entree][indice_estimation])


print("Votre temps estimé sur "+distance_estimation+" est : " + str(estimation)) 


