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

initial_game = (0, 0)

(S,P,R,T) = (0,1,3,5)

utility_matrix = np.array([[[R, R], [S, T]],
                          [[T, S], [P, P]]])

# on les considère comme des variables globales

# ================================================ #  
# ================== STRATEGIES ================== #
# ================================================ # 

# ============ Strategies independant from the opponent ============ #

all_c      = {"strat" : np.array([[1,1],
                                  [1,1]]),
                 "first" : 1,
                 "name" : "Naive (all_c)"}
                 
all_d    = {"strat" : np.array([[0,0],
                                [0,0]]),
                 "first" : 0,
                 "name" : "Thief (all_d)"}
                 
random_strat  = {"strat" : np.array([[0.5,0.5],
                                     [0.5,0.5]]),
                 "first" : 0.5,
                 "name" : "Random"}
                 
strat_indecis = {"strat" : np.array([[0,0],
                                     [1,1]]),
                 "first" : 1,
                 "name" : "Irresolute"} #(il alterne entre trahir et coopérer)

 
# ================== Deterministic (pure) strategies ================== #

tit_for_tat = {"strat" : np.array([[1,0],    # si l'adv a coopéré, on cooperera au prochain tour
                                     [1,0]]),  # si l'adv a trahi, on le trahira
                 "first" : 1,
                 "name" : "Copycat (tit for tat)"} 
                 
                 
resentful = {"strat" : np.array([[1,0],
                                 [0,0]]),
                   "first" : 1,
                   "name" : "Resentful"}            
                 
strat_inverse = {"strat" : np.array([[0,1],
                                     [0,1]]),
                 "first" : 1,
                 "name" : "Inverse tit-for-tat"} # si l'adv a coop, on le trahira
                 
# ================== Mixed strategies ================== #

strat_conciliant = {"strat" : np.array([[1, 0.1],    
                                        [1, 0.1]]),
                   "first" : 1,
                   "name" : "Accommodating"} 
                    
strat_prudent = {"strat" : np.array([[0.99, 0.5],    
                                      [0.9, 0.1]]),
                   "first" : 1,
                   "name" : "Cautious"} 
                   
strat_inspiree =   {"strat" : np.array([[0.9,0.1],
                                        [0.1,0.2]]),
                    "first" : 1,
                    "name" : "Inspired"}

# ================== Stratégies Zero Determinant (ZD) ================== #
# Ces stratégies sont le fruit du travail des informaticiens Press & Dyson
# Pour plus d'information, consultez
# https://sciencetonnante.wordpress.com/2017/03/03/la-theorie-des-jeux/ (simple)
# http://www.pnas.org/content/109/26/10409.full (très technique)

p1 = 0.9 # 0.9 pour gain de 2 / 0.0 pour un gain de 1
p4 = 0.1 # 0.1 pour un gain de 2 / 0.0 pour un gain de 1
p2 = (p1*(T-P)-(1+p4)*(T-R))/(R-P)
p3 = ((1-p1)*(P-S)+p4*(R-S))/(R-P)

gain_moyen = ((1-p1)*P+p4*R)/(1-p1+p4)
# = 2 pour (0,1,3,5)
print("Control", int(gain_moyen*100)/100)
print("p1", p1, "p2", p2, "p3", p3, "p4", p4)
strat_maitrise = {"strat" : np.array([[p1,p2],
                                      [p3,p4]]),
                  "first" : 1,
                  "name" : "Control 2 (ZD)"}

# La stratégie "extorque" impose un rapport fixe entre le gain du
# joueur et celui de l'adversaire (pour 10 000 itérations)
chi = 2
phi = 0.5 * (P-S)/((P-S) + chi*(T-P))
print(phi, chi)
q1 = 1 - phi*(chi-1)*(R-P)/(P-S)
q2 = 1 - phi*(1 + chi*(T-P)/(P-S))
q3 = phi*(chi+ (T-P)/(P-S) )
q4 = 0
print("Extortion", chi)
print("q1", q1, "q2", q2, "q3", q3, "q4 0")

strat_extorque =   {"strat" : np.array([[q1,q2],
                                        [q3,q4]]),
                    "first" : 1,
                    "name" : "Extortion 2 (ZD)"}

# ================ List of strategies ================ #
# dans le but de se les faire affronter entre elles
# on les considère comme des variables globales

liste_strat = [all_c, all_d, random_strat, strat_indecis,
               tit_for_tat, resentful, 
               strat_conciliant, strat_prudent,
               strat_maitrise, strat_extorque]
# Non inclus : inverse, inspiree qui n'ont que peu d'interêt


# ========================================================= #  
# ======================= Simulation ====================== #
# ========================================================= # 

# ========= Iterated game for 2 strategies ========= #

def iterated_game(nb_of_games, strat_a, strat_b, display=False, utility_matrix=utility_matrix):
    
    if random.random() < strat_a["first"]:
        a = 0
    else:
        a = 1
    if random.random() < strat_b["first"]:
        b = 0
    else:
        b = 1
    
    gain_a = utility_matrix[a][b][0]
    gain_b = utility_matrix[a][b][1]

    if display:
        A = np.zeros(nb_of_games)
        B = np.zeros(nb_of_games)
        A[0] = gain_a
        B[0] = gain_b
        
    for i in range(1, nb_of_games):
        
        if random.random() < strat_a["strat"][a][b]: 
            new_choice_of_A = 0
        else:
            new_choice_of_A = 1
            
        if random.random() < strat_b["strat"][b][a]:
            new_choice_of_B = 0
        else:
            new_choice_of_B = 1
        
        (a, b) = (new_choice_of_A, new_choice_of_B)
        
        gain_a += utility_matrix[a][b][0]
        gain_b += utility_matrix[a][b][1]
        
        if display:
            A[i] = gain_a / (i+1)
            B[i] = gain_b / (i+1)
        
    if display:
        plt.plot(A, "r")
        plt.plot(B, "b")
        plt.plot(np.ones(nb_of_games), "g")
        plt.xlabel("Red : "+strat_a["name"]+" - Blue : "+strat_b["name"])
        plt.ylabel("Mean score")
        plt.show()
    mean_score_a = int(100*gain_a/nb_of_games)/100
    mean_score_b = int(100*gain_b/nb_of_games)/100
    return (mean_score_a, mean_score_b)
          
#iterated_game(10000, strat_prudent, strat_alea_total, display = True)
#iterated_game(5000, strat_vol, strat_alea_total, display = True)
iterated_game(10000, strat_maitrise, strat_extorque, display = True)


# ================== For a Strategy ================== #

def results_strategies(strat, nb_of_games, opponents = liste_strat):
    
    n = len(opponents)
    M = np.zeros((n,2)) 

    for i in range(n): 
        M[i] = iterated_game(nb_of_games, strat, opponents[i])

    return M

# ================== Affichage sous forme d'histogramme ================== #
# !!! xlsxwriter required !!!
# Get it here : https://github.com/jmcnamara/XlsxWriter
# Or just `pip install xlsxwriter`
    
def create_sheets(list_strategies, list_opponents, nb_of_rounds):

    nb_opponents = len(list_opponents)
    liste_noms_adv = [adv["name"] for adv in list_opponents]

    for strat in list_strategies:
        # Get the results
        res = results_strategies(strat, nb_of_rounds, opponents = list_opponents)
        tab = transpose(res)
        
        # Export data
        workbook = xlsxwriter.Workbook("strat_"+strat["name"]+".xlsx")
        worksheet = workbook.add_worksheet()
        bold = workbook.add_format({'bold': 1})
        
        headings = ['name adv', 'Score', 'Opp score']
        worksheet.write_row('A1', ["Made by E. Quimerc'h"], bold)
        worksheet.write_row('A3', headings, bold)
        worksheet.write_column('A4', liste_noms_adv)
        worksheet.write_column('B4', tab[0])
        worksheet.write_column('C4', tab[1])
        
        # Créer le graphique
        chart1 = workbook.add_chart({'type': 'column'})
        
        chart1.add_series({
            'name':       '=Sheet1!$B$3',
            'categories': '=Sheet1!$A$4:$A$'+str(nb_opponents+3),
            'values':     '=Sheet1!$B$4:$B$'+str(nb_opponents+3),
        })
        
        chart1.add_series({
            'name':       '=Sheet1!$C$3',
            'categories': '=Sheet1!$A$4:$A$'+str(nb_opponents+3),
            'values':     '=Sheet1!$C$4:$C$'+str(nb_opponents+3),
        })
        
        chart1.set_title({'name': 'Results of strategy '+strat["name"]+" for "+str(nb_of_rounds)+" rounds"})
        chart1.set_y_axis({'name': 'Mean score'})
        chart1.set_table({'show_keys': True})
        chart1.set_legend({'position': 'none'})
        worksheet.insert_chart('D18', chart1, {'x_offset': 15, 'y_offset': 5})
        workbook.close()
        print("Strategy "+strat["name"]+": printing")
    print("\Everything printed\n\n\n")
    return
    

create_sheets(liste_strat, liste_strat, 10000)


