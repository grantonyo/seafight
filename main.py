from random import randint


class ShipLocationException(Exception):
    pass


class ShotOutError(Exception):
    def __str__(self):
        print("Вы стреляеете за доску. Веедите две цифры от 1 до 6 через пробел.")


class FilledCellError(Exception):
    def __str__(self):
        print("Эта клетка уже занята. Введите другие координаты.")


class InputError(Exception):
    def __str__(self):
        print("Неверные ввод данных. Веедите две цифры от 1 до 6 через пробел.")


class Board:
    def __init__(self, type_):
        self.type = type_
        self.matr = self.field = [["0"] * 6 for _ in range(6)]
        self.ships = []
        self.filled_cells = []
        self.killed_ships = 0

    def add_ship(self, ship):
        control_num = 0
        for i in ship.location():
            if not self.out_check(i) or i in self.filled_cells:
                control_num += 1
                raise ShipLocationException

        if control_num == 0:
            self.ships.append(ship)
            for j in ship.location():
                self.ship_contour(j)
                self.matr[j.x - 1][j.y - 1] = "■"

    def out_check(self, dot):
        return dot.x in range(1, 7) and dot.y in range(1, 7)

    def ship_contour(self, dot, show=False):
        near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        for i, j in near:
            res = Dot(dot.x + i, dot.y + j)
            if self.out_check(res) and res not in self.filled_cells:
                self.filled_cells.append(res)
                if show and self.matr[res.x - 1][res.y - 1] == "0":
                    self.matr[res.x - 1][res.y - 1] = "."


    def ship_generator(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        for l in lens:
            check_num = 0
            while check_num < 2000:
                ship = Ship(Dot(randint(1, 6), randint(1, 6)), l, randint(0, 1))
                try:
                    check_num += 1
                    self.add_ship(ship)
                    break
                except ShipLocationException:
                    pass
        if len(self.ships) != 7:
            self.matr = self.field = [["0"] * 6 for _ in range(6)]
            self.ships = []
            self.filled_cells = []
            self.ship_generator()

    def shot(self, dot):
        if not self.out_check(dot):
            raise ShotOutError
        if self.matr[dot.x - 1][dot.y - 1] == "." or self.matr[dot.x - 1][dot.y - 1] == "X":
            raise FilledCellError
        self.filled_cells.append(dot)
        print(f'Выстрел в клетку ({dot.x},{dot.y})')
        if self.matr[dot.x - 1][dot.y - 1] == "■":
            self.matr[dot.x - 1][dot.y - 1] = "X"
            for ship in self.ships:
                    if dot in ship.coords:
                        ship.lives -= 1
                        if ship.lives !=0:
                            print("Корабль ранен.")
                        else:
                            print("Корабль убит.")
                            self.killed_ships += 1
                            for d in ship.coords:
                                self.ship_contour(d, show=True)
        else:
            self.matr[dot.x - 1][dot.y - 1] = "."
            print("Промах.")


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Ship:
    def __init__(self, bow, length, orient):
        self.bow = bow
        self.length = length
        self.orient = orient
        self.lives = length
        self.coords = []

    def location(self):

        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.orient == 1:
                cur_x += i

            elif self.orient == 0:
                cur_y += i

            self.coords.append(Dot(cur_x, cur_y))

        return self.coords

class BoardDisplay:
    def __init__(self, board1, board2):
        self.board1 = board1
        self.board2 = board2

    def display(self):
        print(f"{self.board1.type} board:", "       ", f"{self.board2.type} board:")
        print(" |1|2|3|4|5|6|", "     ", "|1|2|3|4|5|6|")
        n = 0
        while n < 6:
            print(f'{n + 1}|', end="")
            for i in self.board1.matr[n]:
                print(f'{i}', end="|")
            else:
                print(f"      {n + 1}|", end="")
                for i in self.board2.matr[n]:
                    if self.board2.type == "Computer" and i == "■":
                        print("0", end="|")
                    else:
                        print(f'{i}', end="|")
            print()
            n += 1


class Player:
    def __init__(self, type):
        self.type = type  # User or Computer
        self.board = Board(type)

    def manual_shoot(self):
        while True:
            coords = input("Введите кординаты через пробел: ").split()
            if len(coords) != 2:
                print("Введите две координаты")
            else:
                a, b = coords
                if (not a.isdigit()) or (not b.isdigit()):
                    print("Введите две цифры от 1 до 6 через пробел")
                else:
                    a, b = int(a), int(b)
                    return Dot(a, b)

    def authomatic_shot(self):
        a, b = randint(1, 6), randint(1, 6)
        return Dot(a, b)


class Game:
    def __init__(self):
        self.user = Player("Player")
        self.cpu = Player("Computer")
        self.user.board.ship_generator()
        self.user.board.filled_cells = []
        self.cpu.board.ship_generator()
        self. cpu.board.filled_cells = []
        self.interface = BoardDisplay(self.user.board, self.cpu.board)

    def greetings(self):
        print('''
Игра "Морской бой"
_______________________
В этой игре для растановки кораблей используются поля размером 6 на 6. 
Первая строка и первый столбец - это координаты поля.
Корабли расставляются на поле игрока и компьютера автоматически в случайном порядке.
Ставится один трехпалубный, два двухпалубных и четыре одноппалубных корабля.
Формат ввода координат выстела - две цифры от 1 до 6 через пробел.
Первая цифра - координата на доске по вертикальной оси (x).
Вторая цифра - кордината на доске по горизонатльной оси (y)
_______________________''')

    def user_move(self):
        while True:
            try:
                print("ХОД ИГРОКА")
                s = self.user.manual_shoot()
                self.cpu.board.shot(s)  # ход игрока на доске компьютера
                self.interface.display()
                print(f"Подбито кораблей: {self.cpu.board.killed_ships} из 7")
                if self.user.board.killed_ships == 7:
                    break
            except FilledCellError:
                print("Эта клета занята. Попробуйте выстрелить еще раз.")
            except ShotOutError:
                print("Вы стреляете за доску. Укажите две цифры от 1 до 6 через пробел.")
            else:

                if self.cpu.board.matr[s.x-1][s.y-1] == "X" and self.cpu.board.killed_ships < 7:
                    self.user_move()
                break

    def cpu_move(self):
        while True:
            try:
                print("ХОД КОМПЬЮТЕРА")
                s = self.cpu.authomatic_shot()
                self.user.board.shot(s)  # ход игрока на доске компьютера
                self.interface.display()
                print(f"Подбито кораблей: {self.user.board.killed_ships} из 7")
                if self.user.board.killed_ships == 7:
                    break

            except FilledCellError:
                pass
            except ShotOutError:
                pass
            else:
                if self.user.board.matr[s.x-1][s.y-1] == "X" and self.user.board.killed_ships < 7:
                    self.cpu_move()
                break

    def start(self):
        self.greetings()
        self.interface.display()
        while True:
            self.user_move()
            if self.cpu.board.killed_ships == 7:
                print('Вы победили! Конец игры.')
                break
            self.cpu_move()
            if self.user.board.killed_ships == 7:
                print('Компьютер побелил. Конец игры.')
                break
g=Game()
g.start()
