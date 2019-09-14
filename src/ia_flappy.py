from tkinter import *
from random import *
from math import sqrt, pi, sin

def amelio(event):
    global ame, lbest, loop
    ame +=1
    print('     generation {}'.format(ame))
    if ame <=40:
        loop = 0
        lancer()
    else:
        print(lbest[0])


def jump(nois):
    global lv,t
    lv[nois] = -550/t



def lancer():
    canvas.create_rectangle(0,0,1300,800, outline = 'white', fill = 'white')
    initia()

def create_lintel():
    global lintel, n_oiseau
    lintel = []
    for a in range(n_oiseau):
        lintel.append([random()*2-1,random()*2-1,random()*2-1,random()*2-1,random()*2*pi-pi,random()*2*pi-pi])  #[coef1,coef2,coef3,coef4,ega1,ega2]


def evolve(l, taux, n):
    global lintel
    for a in range(n):
        lintel.append([gauss(0,taux/1.75)+l[0],gauss(0,taux/1.75)+l[1],gauss(0,taux/1.75)+l[2],gauss(0,taux/1.75)+l[3],gauss(0,taux*pi/3.5)+l[4],gauss(0,taux*pi/3.5)+l[5]])  #[coef1,coef2,coef3,coef4,ega1,ega2]




def initia():
    global t ,lv, oiseau, obstacle, distance, ly, sortie, lsor, lscore, mort, n_oiseau, lintel, lbest, ame, loop, maxloop, ntuy, ltuy, mattuy
    n_oiseau = 100
    if loop == 0:
        if ame == 1:
            lintel = []
            create_lintel()
        else:
            lintel = list(lbest)
            evolve(lbest[0],max([1/(ame+1),0.1]),38)
            evolve(lbest[1],max([1/(ame+1),0.1]),32)
            evolve(lbest[2],max([1/(ame+1),0.1]),27)


    mort = []
    ly=[]
    lv=[]
    if loop == 0:
        lscore = []
    for a in range(n_oiseau):
        mort.append(1)
        ly.append(400)
        lv.append(0)
        if loop == 0:
            lscore.append(0)

    obstacle1 = canvas.create_rectangle(500,0,580,800,outline = 'black', fill = 'green')
    obstacle2 = canvas.create_rectangle(1000,0,1080,800,outline = 'black', fill = 'green')
    obstacle3 = canvas.create_rectangle(1500,0,1580,800,outline = 'black', fill = 'green')
    obstacle = [obstacle1,obstacle2,obstacle3]

    lsor = []
    ltuy = mattuy[loop]
    ntuy = 3
    for a in range(3):
        lsor.append(ltuy[a])
    
    sortie1 = canvas.create_rectangle(500,lsor[0],580,lsor[0]+250,outline = 'white', fill = 'white')
    sortie2 = canvas.create_rectangle(1000,lsor[1],1080,lsor[1]+250,outline = 'white', fill = 'white')
    sortie3 = canvas.create_rectangle(1500,lsor[2],1580,lsor[2]+250,outline = 'white', fill = 'white')
    sortie = [sortie1,sortie2,sortie3]

    distance= [500,1000,1500]

    oiseau = []
    for a in range(n_oiseau):
        oiseau.append(canvas.create_oval(50,370,110,430,outline = "red", fill = "yellow"))


    t = 25
    maxloop = 0
    boucle()
    


def gros_calcul(a):
    global lv, distance, ly, lsor, lintel
    d = min(distance)
    if d < 50:
        d += 500 
    ys = lsor[distance.index(min(distance))]
    deltay = (ly[a]-ys-220)/700
    vit = lv[a]/60
    deltax = (d-50)/500
    l = lintel[a]
    noeud = sin(l[4]*(l[0]*deltay+l[1]*vit))
    return sin(l[5]*(l[2]*noeud+l[3]*deltax))


def boucle():
    global t, lv, ly, lscore, mort, lintel, n_oiseau, lbest, oiseau, loop, maxloop, ntourpargen

    for a in range(n_oiseau):
        if mort[a]==1:
            if gros_calcul(a) > 0:
                jump(a)
            lv[a] += 30/t
            dplo(a)
            if ly[a] >-200 and ly[a] < 1000 and touch(a) == 'none':
                lscore[a] += 1
            else:
                canvas.move(oiseau[a],-150,0)
                mort[a] = 0


    dplt()
    if 1 in mort:
        maxloop+=1
        tk.after(int(100/t),boucle)
    else:
        if loop < ntourpargen-1:
            loop += 1
            print('     ',maxloop)
            lancer()
        else:
            lbest = []
            print('     ',maxloop)
            print('      fin génération :')
            for a in range(3):
                curs = lscore.index(max(lscore))
                print((max(lscore)))
                lbest.append(lintel[curs])
                del lscore[curs]
                del lintel[curs]
            amelio('<space>')

        


def dplo(nois):
    global oiseau, ly, lv
    canvas.move(oiseau[nois],0,int(round(lv[nois])))
    ly[nois] += int(round(lv[nois]))


def dplt():
    global obstacle, distance, sortie, lsor, ltuy, ntuy
    for a in range(3):
        canvas.move(obstacle[a],-200/t,0)
        canvas.move(sortie[a],-200/t,0)
        distance[a] -= 200/t
        if distance[a]<=-100:
                canvas.move(obstacle[a],1500,0)
                '''
                aleat = randint(50-lsor[a],500-lsor[a])
                canvas.move(sortie[a],1500,aleat)  # pour générer un tueau de hauteur aléatoire
                '''

                canvas.move(sortie[a],1500,ltuy[ntuy]-lsor[a])
                lsor[a] = ltuy[ntuy]
                ntuy+=1

                distance[a] = 1400



def touch(nois):
    global ly, distance, lsor
    for a in range(3):
        if distance[a]<=110:
            if distance[a]<=80 and distance[a]>=0:
                if ly[nois] - lsor[a] <30 or  lsor[a]+250-ly[nois]<30:
                    return 'death'
            elif lsor[a]<ly[nois] and lsor[a] + 250>ly[nois]:
                if sqrt((ly[nois]-lsor[a])**2+(distance[a]-80)**2)<30 or sqrt((ly[nois]-lsor[a])**2+(distance[a])**2)<30 or sqrt((ly[nois]-lsor[a]-250)**2+(distance[a]-80)**2)<30 or sqrt((ly[nois]-lsor[a]-250)**2+(distance[a])**2)<30:
                    return 'death'
            else:
                if abs(distance[a]-80)<30:
                    return 'death'
    return 'none'


global ame, ltuy, ntourpargen
ame = 0
ntourpargen = 10
#mattuy = [[256, 451, 203, 474, 154, 56, 275, 205, 347, 106, 240, 416, 77, 270, 434, 63, 415, 351, 201, 221, 353, 210, 81, 165, 365, 293, 221, 358, 189, 444, 123, 345, 72, 441, 75,288, 98, 218, 133, 275, 260, 417, 173, 418, 406, 345, 63, 290, 332, 108, 481, 493, 254, 392, 164, 485, 78, 234, 250, 324, 393, 301, 240, 481, 91, 380, 445, 113, 445, 138, 109, 68, 178, 143, 439, 465, 203, 179, 105, 496, 257, 63, 472, 404, 444, 373, 175, 129, 177, 64, 229, 88, 92, 498, 324, 262, 245, 121, 464, 467]]

mattuy= [[randint(50,500) for a in range(100)] for b in range(ntourpargen)]

print(mattuy)

tk = Tk()
canvas = Canvas(tk,width = 1300, height = 800, bd = 0, bg = "white")
canvas.pack(padx = 10, pady = 10)
tk.title("flappy bird")
canvas.bind_all('<space>', amelio)


tk.mainloop()



# apres 40 générations a 5 phases de tests et avec la fonction random, voici le meilleur : [0.5417369766692495, 0.10645938533333107, 0.8968038967835816, 0.14424564977894072, -0.8127782998319314, -1.5211282664209702] 
# apres 40 générations a 5 phases de tests et avec la fonction gauss mais avec un taux élevé , voici le meilleur : [1.1490630645109243, 0.3141330995023927, 0.3513194867581561, 0.38771631115279437, -2.0600997678331514, -0.13966876808774312]
# [256, 451, 203, 474, 154, 56, 275, 205, 347, 106, 240, 416, 77, 270, 434, 63, 415, 351, 201, 221, 353, 210, 81, 165, 365, 293, 221, 358, 189, 444, 123, 345, 72, 441, 75,288, 98, 218, 133, 275, 260, 417, 173, 418, 406, 345, 63, 290, 332, 108, 481, 493, 254, 392, 164, 485, 78, 234, 250, 324, 393, 301, 240, 481, 91, 380, 445, 113, 445, 138, 109, 68, 178, 143, 439, 465, 203, 179, 105, 496, 257, 63, 472, 404, 444, 373, 175, 129, 177, 64, 229, 88, 92, 498, 324, 262, 245, 121, 464, 467]



