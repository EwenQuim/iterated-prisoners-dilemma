# ======================================================== #
# ======================================================== #
# =================== Théorie des jeux =================== #
# ======================================================== #
# ======================================================== #

# Confrontation de stratégies pour le Dilemme du Prisonnier
#               dans sa version Itérée 

# Étude des équilibres et des stratégies Zero Determinant de
#                   Press & Dyson

# Créé par Ewen Quimerc'h, 2018

# ========================================================= #

import random
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter

# ========================================================= #  
# ================== Fonction auxiliaire ================== #
# ========================================================= # 

def transpose(A):
    (n, p) = np.shape(A)
    B = np.zeros((p, n))
    for i in range(n):
        for j in range(p):
            B[j][i] = A[i][j]
    return B
    
# ========================================================= #  
# ================== Modélisation du jeu ================== #
# ========================================================= # 

jeu_initial = (0, 0)

(S,P,R,T) = (0,1,3,5)

matrice_gains = np.array([[[R, R], [S, T]],
                          [[T, S], [P, P]]])

# on les considère comme des variables globales

# ================================================ #  
# ================== STRATÉGIES ================== #
# ================================================ # 
#strat_de_A_exemple = [[p1,p2],
#                      [p3,p4]]
# Renvoie la probabilité pour A de coopérer après les résultats du dernier jeu
# p1 : probabilité que A coopère si A et B on coopéré au tour précédent
# p2 : probabilité que A coopère si A a coopéré et B a trahi au tour précédent
# p3 : probabilité que A coopère si A a trahi et B a coopéré au tour précédent
# p4 : probabilité que A coopère si A et B on trahi au tour précédent

# ============ Stratégies indépendantes de l'adversaire ============ #

strat_naif    = {"strat" : np.array([[1,1],
                                     [1,1]]),
                 "premier" : 1,
                 "nom" : "Naïf"}
                 
strat_vol    = {"strat" : np.array([[0,0],
                                    [0,0]]),
                 "premier" : 0,
                 "nom" : "Voleur"}
                 
strat_alea    = {"strat" : np.array([[0.5,0.5],
                                     [0.5,0.5]]),
                 "premier" : 0.5,
                 "nom" : "Aléatoire"}
                 
strat_indecis = {"strat" : np.array([[0,0],
                                     [1,1]]),
                 "premier" : 1,
                 "nom" : "Indécis"} #(il alterne entre trahir et coopérer)

 
# ================== Stratégies déterministes ================== #
# Ces stratégies s'adaptent à l'adversaire et choisissent
# clairement de trahir ou coopérer

strat_copieur = {"strat" : np.array([[1,0],    # si l'adv a coopéré, on cooperera au prochain tour
                                     [1,0]]),  # si l'adv a trahi, on le trahira
                 "premier" : 1,
                 "nom" : "Copieur"} 
                 
                 
strat_rancunier = {"strat" : np.array([[1,0],
                                       [0,0]]),
                   "premier" : 1,
                   "nom" : "Rancunier"}            
                 
strat_inverse = {"strat" : np.array([[0,1],
                                     [0,1]]),
                 "premier" : 1,
                 "nom" : "Copieur inverse"} # si l'adv a coop, on le trahira
                 
# ================== Stratégies mixtes (aléatoires) ================== #
# Le choix du joueur dépend de l'adversaire mais n'est pas 
# entièrement déterminé : c'est une probabilité de coopérer


strat_alea_total = {"strat" : np.array([[random.random(),random.random()],
                                     [random.random(),random.random()]]),
                    "premier" : 1,
                    "nom" : "Aléa total"}

strat_conciliant = {"strat" : np.array([[1, 0.1],    
                                        [1, 0.1]]),
                   "premier" : 1,
                   "nom" : "Cop. conciliant"} 
                    
strat_prudent = {"strat" : np.array([[0.99, 0.5],    
                                      [0.9, 0.1]]),
                   "premier" : 1,
                   "nom" : "Prudent"} 
                   
strat_inspiree =   {"strat" : np.array([[0.9,0.1],
                                        [0.1,0.2]]),
                    "premier" : 1,
                    "nom" : "Inspirée"}

# ================== Stratégies Zero Determinant (ZD) ================== #
# Ces stratégies sont le fruit du travail des informaticiens Press & Dyson
# Pour plus d'information, consultez
# https://sciencetonnante.wordpress.com/2017/03/03/la-theorie-des-jeux/ (simple)
# http://www.pnas.org/content/109/26/10409.full (très technique)

# La stratégie "maitrise" impose un gain fixe à l'adversaire
# (pour plus de 10 000 itérations)

p1 = 1/4 # 0.9 pour gain de 2 / 0.0 pour un gain de 1
p4 = 0.0 # 0.1 pour un gain de 2 / 0.0 pour un gain de 1
p2 = (p1*(T-P)-(1+p4)*(T-R))/(R-P)
p3 = ((1-p1)*(P-S)+p4*(R-S))/(R-P)

gain_moyen = ((1-p1)*P+p4*R)/(1-p1+p4)
# = 2 pour (0,1,3,5)
print(p2,p3,gain_moyen)
strat_maitrise = {"strat" : np.array([[p1,p2],
                                      [p3,p4]]),
                  "premier" : 1,
                  "nom" : "Maitrise (ZD)"}

# La stratégie "extorque" impose un rapport fixe entre le gain du
# joueur et celui de l'adversaire (pour 10 000 itérations)
chi = 100
phi = 0.5 * (P-S)/((P-S) + chi*(T-P))
print(phi, chi)
q1 = 1 - phi*(chi-1)*(R-P)/(P-S)
q2 = 1 - phi*(1 + chi*(T-P)/(P-S))
q3 = phi*(chi+ (T-P)/(P-S) )
q4 = 0
print(q1, q2,q3)

strat_extorque =   {"strat" : np.array([[q1,q2],
                                        [q3,q4]]),
                    "premier" : 1,
                    "nom" : "Extortion (ZD)"}

# ================ Recensement des stratégies ================ #
# dans le but de se les faire affronter entre elles
# on les considère comme des variables globales

liste_strat = [strat_naif, strat_vol, strat_alea, strat_indecis,
               strat_copieur, strat_rancunier, 
               strat_conciliant, strat_prudent, strat_alea_total,
               strat_maitrise, strat_extorque]
# Non inclus : inverse, inspiree qui n'ont que peu d'interêt


# ========================================================= #  
# =================== Simulation du jeu =================== #
# ========================================================= # 

# ========= Jeu itéré simple à deux joueurs, avec choix de l'affichage ========= #

def jeu_itere(nb_de_jeux, strat_a, strat_b, afficher=False, matrice_gain=matrice_gains):
    
    if random.random() < strat_a["premier"]:
        a = 0 # A coopère
    else:
        a = 1 # A trahi
    if random.random() < strat_b["premier"]:
        b = 0 # B coopère
    else:
        b = 1 # B trahi 
    
    gain_a = matrice_gain[a][b][0]
    gain_b = matrice_gain[a][b][1]

    if afficher:
        A = np.zeros(nb_de_jeux)
        B = np.zeros(nb_de_jeux)
        A[0] = gain_a
        B[0] = gain_b
        
    for i in range(1, nb_de_jeux):
        
        if random.random() < strat_a["strat"][a][b]: 
            nouveau_choix_de_A = 0 # A coopère
        else:
            nouveau_choix_de_A = 1 # A trahi
            
        if random.random() < strat_b["strat"][b][a]:
            nouveau_choix_de_B = 0 # B coopère
        else:
            nouveau_choix_de_B = 1 # B trahi 
        # On remarque que la stratégie actuelle dépend du choix précédent de A ET de B
        
        (a, b) = (nouveau_choix_de_A, nouveau_choix_de_B)
        
        gain_a += matrice_gain[a][b][0]
        gain_b += matrice_gain[a][b][1]
        
        if afficher:
            A[i] = gain_a / (i+1)
            B[i] = gain_b / (i+1)
        
    if afficher:
        plt.plot(A, "r")
        plt.plot(B, "b")
        plt.xlabel("Rouge : "+strat_a["nom"]+" - Bleu : "+strat_b["nom"])
        plt.ylabel("Gain moyen")
        plt.show
    gain_moyen_a = int(100*gain_a/nb_de_jeux)/100
    gain_moyen_b = int(100*gain_b/nb_de_jeux)/100
    return (gain_moyen_a, gain_moyen_b)
          
#jeu_itere(10000, strat_prudent, strat_alea_total, afficher = True)
#jeu_itere(5000, strat_vol, strat_alea_total, afficher = True)
#jeu_itere(50, strat_rancunier, strat_prudent, afficher = True)


# ================== Bilan d'une stratégie ================== #

def resultat_strategie(strat, nb_de_jeux, adversaires = liste_strat):
    
    n = len(adversaires)
    M = np.zeros((n,2)) # on stocke ici les gains totaux de la stratégie 
                                     # à tester et ceux des autres
    for i in range(n):
        
        M[i] = jeu_itere(nb_de_jeux, strat, adversaires[i])

    return M

# ================== Affichage sous forme d'histogramme ================== #
# !!! module xlsxwriter requis !!!
# Obtensible ici : https://github.com/jmcnamara/XlsxWriter
# Téléchargez, et dézippez dans votre dossier Python
# L'histogramme sera créé à l'emplacement suivant :
# \WinPython-64bit-3.4.4.4Qt5\XlsxWriter-master\examples
# Il est possible de changer l'emplacement de création de fichier
# en modifiant le fichier  setup.py du module xlsxwriter
    
def creer_tableur(liste_strategies, liste_adversaires, nombre_de_jeux):

    nb_adversaires = len(liste_adversaires)
    liste_noms_adv = [adv["nom"] for adv in liste_adversaires]

    for strat in liste_strategies:
        # Obtenir les résultats
        res = resultat_strategie(strat, nombre_de_jeux, adversaires = liste_adversaires)
        tab = transpose(res)
        
        # Exporter les données
        workbook = xlsxwriter.Workbook("strat_"+strat["nom"]+".xlsx")
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        
        headings = ['Nom adv', 'Gain joueur', 'Gain adv']
        worksheet.write_row('A1', ["Réalisé par E. Quimerc'h"], bold)
        worksheet.write_row('A3', headings, bold)
        worksheet.write_column('A4', liste_noms_adv)
        worksheet.write_column('B4', tab[0])
        worksheet.write_column('C4', tab[1])
        
        # Créer le graphique
        chart1 = workbook.add_chart({'type': 'column'})
        
        chart1.add_series({
            'name':       '=Sheet1!$B$3',
            'categories': '=Sheet1!$A$4:$A$'+str(nb_adversaires+3),
            'values':     '=Sheet1!$B$4:$B$'+str(nb_adversaires+3),
        })
        
        chart1.add_series({
            'name':       '=Sheet1!$C$3',
            'categories': '=Sheet1!$A$4:$A$'+str(nb_adversaires+3),
            'values':     '=Sheet1!$C$4:$C$'+str(nb_adversaires+3),
        })
        
        chart1.set_title({'name': 'Résultats de la stratégie '+strat["nom"]+" pour "+str(nombre_de_jeux)+" itérations"})
        chart1.set_y_axis({'name': 'Gain moyen'})
        chart1.set_table({'show_keys': True})
        chart1.set_legend({'position': 'none'})
        worksheet.insert_chart('D18', chart1, {'x_offset': 15, 'y_offset': 5})
        workbook.close()
        print("Stratégie "+strat["nom"]+" imprimée")
    print("\nFin de l'impression. Impression réussie\n\n\n")
    return
    

creer_tableur(liste_strat, liste_strat, 10000)


