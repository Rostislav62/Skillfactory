from random import randint


class BoardException(Exception):
    pass
    # def __init__(self, message, extra_info):
    #     super().__init__(message)
    #     self.extra_info = extra_info


class BoardOutException(BoardException):
    def __str__(self):
        return "You're trying to shoot outside the battlefield"
    # def __init__(self, message, extra_info):
    #     super().__init__(message)
    #     self.extra_info = extra_info


class BoardUsedException(BoardException):
    pass


class BoardWrongShipException(BoardException):
    def __str__(self):
        return "You've already shot at this place."
    # def __init__(self, message, extra_info):
    #     super().__init__(message)
    #     self.extra_info = extra_info


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship:
    def __init__(self, bow, liv, o):
        self.bow = bow
        self.liv = liv
        self.o = o
        self.lives = liv

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.liv):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.o == 0:
                cur_x += i

            elif self.o == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["0"] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def __str__(self):
        res = ''
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f'\n{i + 1} | ' + " | ".join(row) + " |"

        if self.hid:
            res = res.replace('■', '0')

        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                # self.field[cur.x][cur.y] = "+"
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardOutException()

        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Ship is destroyed!!!")
                    return True
                else:
                    print("The ship is wounded!")
                    return True

        self.field[d.x][d.y] = "."
        print("Missed")
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"The computer shoots: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Your turn:").split()

            if len(cords) != 2:
                print("You must only enter numbers from 1 to 6:")
                continue
            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print("You must only enter numbers from 1 to 6:")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)


class Game:
    def __init__(self, size=6):  # Game constructor

        self.size = size  # The size of the game field.
        player_ = self.random_board()  # A battlefield is created for the player.
        computer_ = self.random_board()  # A battlefield is created for the computer.
        computer_.hid = True  # The computer field is made hidden.

        self.ai = AI(computer_, player_)  # The created battlefield is transferred to the computer.
        self.user = User(player_, computer_)  # The created battlefield is transferred to the player.

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for len_ in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), len_, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greet(self):
        print(f'****************************************************************')
        print(f'***********************  The Battle Ship  **********************')
        print(f"The point of the game is to destroy all the computer's ships before he does.")
        print(f'The computer shoots at random, so your chances of winning are very high.')
        print(f'Input format: x y.')
        print(f'x - number of the row.')
        print(f'y - number of the column.')
        print("You must only enter numbers from 1 to 6:")
        print(f'****************************************************************')
        print()
        print(f'                          START ')
        print()

    def print_board(self):
        print('-' * 20)
        print('Player board')
        print(self.user.board)
        print('-' * 20)
        print('Computer board')
        print(self.ai.board)
        print('-' * 20)
    def loop(self):
        num = 0
        while True:
            self.print_board()

            if num % 2 == 0:
                print('The player shoots.')
                repeat = self.user.move()
            else:
                print('Computer shoots.')
                repeat = self.ai.move()

            if repeat:
                num -= 1

            if self.ai.board.defeat():
                self.print_board()
                print('-' * 20)
                print('The user win!!!')
                break

            if self.user.board.defeat():
                self.print_board()
                print('-' * 20)
                print('Computer win!!!')
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()


g = Game()
g.start()
