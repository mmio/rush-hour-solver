import copy
import sys

# Pri vynorovnaní si tu pamätáme posuny
solution = []

# Slovník na pamätanie si navštívených stavov
visited = {}

class Car:
    def __init__(self, name, len , posy, posx, dir):
        self.name = name
        self.points = []

        posy -= 1
        posx -= 1

        self.dir = dir
        if dir == 'h':
            self.dirx = 1
            self.diry = 0
            for i in range(len):
                self.points.append([posy, posx + i])
        elif dir == 'v':
            self.dirx = 0
            self.diry = 1
            for i in range(len):
                self.points.append([posy + i, posx])
        self.len = len

class State:
    def __init__(self, cars):
        self.map = [
            ['1','1','1','1','1','1'],
            ['1','1','1','1','1','1'],
            ['1','1','1','1','1','1'],
            ['1','1','1','1','1','1'],
            ['1','1','1','1','1','1'],
            ['1','1','1','1','1','1']
        ]

        cc = '2'
        for c in cars:
            c.id = cc
            cc = (chr(ord(cc)+1)) 
            for i in c.points:
                self.map[i[0]][i[1]] = c.id
        self.cars = cars

# Pomocná funkcia pre debugovanie
def printState(state):
    for car in state.cars:
        print(state.map[car.points[0][0]][car.points[0][1]],'-->', car.name, car.points[0][0]+1, car.points[0][1]+1)
    for x in state.map:
        for i in x:
            print(i, end='')
        print('')

# Testovanie, či sa auto môže pohnúť vybraným smerom, robené na základe mapy v stave
# Operácia, ktorá sa má vykonať(VLAVO, VPRAVO, HORE, DOLE) je automaticky určená na základe premennej "len" ak má
# kladnú hodnotu pohybuje sa od začkatky mapy 0,0 ak zápornú tak k začiatku 0,0.
# Smer pohybu je teda určený premennou len a orientáciou auta(práve
# preto neimplementujeme každú operáciu zvlášť) 
def canMove(c, len, map):
    first = c.points[0]
    last = c.points[c.len-1]
    if len > 0:
        y = last[0]
        x = last[1]
        if (x + len*c.dirx >= 6 or y + len*c.diry >= 6):
            return False

        for i in range(1, len+1):
            if map[y+i*c.diry][x+i*c.dirx] != '1':
                return False
        
    elif len < 0:
        y = first[0]
        x = first[1]
        if (x + len*c.dirx < 0 or y + len*c.diry < 0):
            return False

        len = abs(len)
        for i in range(1, len+1):
            if map[y-i*c.diry][x-i*c.dirx] != '1':
                return False
    return True

# Posunutie auta na základe overených smerov z funkcie canMove
# Táto funkcia je len jedna, kvôli tomu že smer akým sa má auto pohnúť
# vieme určiť z jediného čísla(len) a orientácie auta 
def move(c, len, ns):
    if len > 0:
        x = c.len - 1
        for i in range(x, -1, -1):
            ns.map[c.points[i][0]][c.points[i][1]] = '1'
            c.points[i][0] += len*c.diry;
            c.points[i][1] += len*c.dirx;
            ns.map[c.points[i][0]][c.points[i][1]] = c.id
    elif len < 0:
        x = c.len
        for i in range(0, x):
            ns.map[c.points[i][0]][c.points[i][1]] = '1'
            c.points[i][0] += len*c.diry;
            c.points[i][1] += len*c.dirx;
            ns.map[c.points[i][0]][c.points[i][1]] = c.id

# Rekurzívne volaná funkcia, ktorá nám kontroluje a generuje nové
# stavy a konec koncov vykonáva prehľadávanie do hĺbky s návratom
def dfs(level, state):
    if level == 0:
        return

    # Ak sme už našli navštívení stav, pokračujeme len ak sme ho našli
    # v nižšej úrovni statového priestora, inak nerozvetvujeme
    s = str(state.map)
    if s in visited:
        if visited[s] < level:
            visited[s] = level
        else:
            return
            

    # Prvé auto vždy musí byť to, ktoré chceme z križovatky dostať von
    # Stav sa za finálny považuje keď je na pravom boku
    if state.cars[0].points[0][1] == 4:
        print("\nFinálny stav:")
        printState(state)
        return True

    visited[s] = level

    #Pre každé jedno auto vyskúšame každý jeden pohyb, ktorý môžu spraviť
    ns = copy.copy(state)
    for c in ns.cars:
        for mvs in [-4,4,-3,3,-2,2,-1,1]:
            if canMove(c, mvs, ns.map):
                move(c, mvs, ns)

                # Pri návrate z rekurzívneho volania, ak sme našli riešenie
                # nevnárame sa ďalej, vynárame sa a ukladáme si potrebné údaje do lišty
                if dfs(level - 1, ns):
                    smer = ""
                    if c.dir == 'h':
                        if mvs > 0:
                            smer = 'Vpravo'
                        else:
                            smer = 'Vlavo'
                    else:
                        if mvs > 0:
                            smer = 'Dole'
                        else:
                            smer = 'Hore'

                    solution.append((c.name, smer, abs(mvs)))
                    return True
                
                move(c, -mvs, ns)

    return False

# Primitívny test
def test1():
    run(State([
        Car('cervene', 2, 3, 2, 'h'),
    ]))
    
# Toto je najťažsia možná konfigurácia(http://www.ulb.ac.be/di/algo/secollet/papers/crs06.pdf)
def test2():
    run(State([
        Car('cervene', 2, 3, 3, 'h'),
        Car('oranzove', 2, 2, 1, 'v'),
        Car('zlte', 2, 5, 2, 'v'),
        Car('zelene', 2, 4, 3, 'v'),
        Car('modre', 2, 1, 4, 'v'),
        Car('svetlomodre', 3, 1, 5, 'v'),
        Car('tmavomodre', 3, 1, 6, 'v'),
        Car('ruzove', 3, 1,1,'h'),
        Car('fialove', 2, 2, 2, 'h'),
        Car('sive', 2,4,1,'h'),
        Car('bordove', 2, 5,5, 'h'),
        Car('kaki', 2,6,3,'h'),
        Car('fuchsia', 2,6,5, 'h'),
    ]))

# Ukážkový test zo zadania
def test3():
    run(State([
        Car('cervene', 2, 3, 2, 'h'),
        Car('oranzove', 2, 1, 1, 'h'),
        Car('zlte', 3, 2, 1, 'v'),
        Car('fialove', 2, 5, 1, 'v'),
        Car('zelene', 3, 2, 4, 'v'),
        Car('svetlomodre', 3, 6, 3, 'h'),
        Car('sive', 2, 5, 5, 'h'),
        Car('tmavomodre', 3, 1, 6, 'v')
    ]))
# Vymyslený originálny scenár
def test4():
    run(State([
        Car('cervene', 2, 3, 1, 'h'),
        Car('oranzove', 2, 4, 1, 'h'),
        Car('zlte', 2, 5, 1, 'h'),
        Car('fialove', 2, 6, 2, 'h'),
        Car('zelene', 3, 3, 3, 'v'),
        Car('sive', 3, 4, 5, 'v'),
    ]))
    
# Test5 z http://www.theiling.de/projects/rushhour.html
def test5():
    run(State([
        Car('cervene', 2, 3, 1, 'h'),
        Car('oranzove', 2, 1, 1, 'h'),
        Car('zelene', 3, 1, 3, 'v'),
        Car('fialove', 2, 1, 4, 'v'),
        Car('zlte', 2, 1, 5, 'h'),
        Car('svetlomodre', 2, 4, 1, 'v'),
        Car('sive', 2, 4, 2, 'h'),
        Car('tmovomodre', 2, 4, 4, 'h'),
        Car('cierne', 2, 6, 1, 'h'),
        Car('ruzove', 2, 5, 4, 'v'),
        Car('fuchsia', 3, 4, 6, 'v'),
    ]))
# Test6, scenár bez riešenia
def test6():
    run(State([
        Car('cervene', 2, 3, 1, 'v'),
    ]))
# Hlavný funkcia programu
def run(state):
    print("-----------------------------------------------------------")
    global solution, visited
    solution = []
    visited = dict()

    print("Začiatočný stav:");
    for c in state.cars:
        print(c.name, c.points[0][0]+1, c.points[0][1]+1, c.dir)
    
    # Najväčšie množstvo pohybov ktoré sú možne pre tuto hru je 93,ak považujeme
    # pohyb iba za posun 1 a hľadáme najlepšie riešenia
    #(http://www.ulb.ac.be/di/algo/secollet/papers/crs06.pdf)
    # Práve preto nám 94 iterácií bude vždy stačiť
    for j in range(1, 95):      
        if dfs(j, state):
            # Výpis riešenia, ak exituje. Musí byť od zadu, lebo sa z rekurzie vynárame od posledného stavu
            print("\nRiešenie:")
            for x in reversed(solution):
                for y in x:
                    print(y, end=' ')
                print('')
            break
    else:
        print('Riešenie neexistuje')

# Spracovanie vstupu
if len(sys.argv) > 1:
    def default():
        print("Wrong argument")

    test = {
        '-t1': lambda: test1(),
        '-t2': lambda: test2(),
        '-t3': lambda: test3(),
        '-t4': lambda: test4(),
        '-t5': lambda: test5(),
        '-t6': lambda: test6(),
    }

    test.get(sys.argv[1], default)()
else:
    cars = []
    while True:
        n = input()
        if n == "quit":
            break
        
        l = int(input())
        y = int(input())
        x = int(input())
        o = input()
        cars.append(Car(n, l, y, x, o))
    run(State(cars))
    
