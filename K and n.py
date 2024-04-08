# Игра крестики нолики
# Итоговое задание 7.6.1 (HW-02)
# Студент Ростислав Шмиглюк

# Игра запускается, верно осуществляется смена хода игрока.
# Реализована проверка введения чисел вне диапазона,
# проверка на занятость клетки.
# Игра корректно завершается при победе одной из сторон.
#
# Однако,
# 1. вывод игрового поля не соответствует шаблону, отсутствует нумерация строк и столбцов.
# 2. Не проверяется ввод нечисловых значений,
# 3. случайный ввод пустого значения нажатием Enter приводит к падению программы.
# 4. Игра не завершается при ничейном результате.


game_ = 'Крестики и нолики' # Game`s name
userN = 'x'  # Name of player
# steps_user_x = 0  # Number of steps made by player x
# steps_user_o = 0  # Number of steps made by player o
steps = 0
matrix_size = 3  # matrix size
row = 0  # row number
col = 0  # column number
winner_x = False  # player x won
winner_o = False  # player o won

print(f'****************************************************************')
print(f'*******************  Игра {game_}  *******************')
print(f'Суть игры чтобы заполнить 3 ячейки подряд своим знаком, х или 0.')
print(f'Вы можете заполнять по горизонтали, вертикали или по диагонали.')
print(f'****************************************************************')
print()
print(f'                    Игру начинает игрок {userN}')
print()


# Функция проверяет если введена цифра
def is_number(m_size):
    try:
        int(m_size)
        return True
    except ValueError:
        return False


def message_wrong_matrix_size(m_size):
    print("Вы ввели неправильную координату")
    print(f'Вы можете вводить цифры от 0 до {m_size - 1}')
    print()


# проверяет если правильно введен размер матрицы и если это цифра
while True:
    matrix_size = 3
    # matrix_size = input("Введите размер матрицы: ") # as an exercise we use a 3x3 matrix
    if is_number(matrix_size):
        N = int(matrix_size)
        if N > 2:
            break
        else:
            message_wrong_matrix_size(matrix_size)
    else:
        message_wrong_matrix_size(matrix_size)

# Строится пустая матрица
matrix = [['-' for i in range(matrix_size + 1)] for j in range(matrix_size + 1)]
# Функция добавления цифр с обозначением координаты строк и столбцов.
for i in range(matrix_size + 1):
    for j in range(matrix_size + 1):
        matrix[0][0] = ' '
        if j > 0 and i == 0:
            matrix[0][j] = j - 1
        if j == 0 and i > 0:
            matrix[i][0] = i - 1


def message_wrong_coordinate(m_size):
    print("Вы ввели неправильную координату")
    print(f'Вы можете вводить цифры от 0 до {m_size - 1}')
    print()



# Функция ввода координат
def coordinate(m_size, coordinate_):
    while True:
        coordinate_x_or_o = input(f"Введите координату по {coordinate_}")
        if is_number(coordinate_x_or_o):
            if int(coordinate_x_or_o) < m_size:
                break
            else:
                message_wrong_coordinate(m_size)
        else:
            message_wrong_coordinate(m_size)
    return int(coordinate_x_or_o) + 1


# Функция которая вызывает функцию ввода координат
def input_coordinate(m_size):
    horizontal_ = coordinate(m_size, 'горизонтали: ')
    vertical_ = coordinate(m_size, 'вертикали: ')
    is_free_cell(horizontal_, vertical_)
    return horizontal_, vertical_


# Функция проверки ячейки если она свободна
def is_free_cell(row_coordinate, col_coordinate):
    if matrix[int(row_coordinate)][int(col_coordinate)] == 'x':
        print(f'Эта координата уже занята игроком x')
        input_coordinate(N)
    elif matrix[int(col_coordinate)][int(col_coordinate)] == 'o':
        print(f'Эта координата уже занята игроком o')
        input_coordinate(N)


# Функция смены игрока
def change_user(user_name_):
    if user_name_ == 'x':
        user_name_ = 'o'

    else:
        if user_name_ == 'o':
            user_name_ = 'x'
    return user_name_


# Функция заполнения матрицы
def fill_matrix(user_nm, row_, col_, step_):
    for i in matrix:
        matrix[int(row_)][int(col_)] = user_nm
        print(*i)
    step_ += 1
    print(f'Step nr {step_}')
    return step_


def winner(matrix_a, n1, m1, n2, m2, n3, m3, winn):
    res = False
    if matrix_a[n1][m1] == matrix_a[n2][m2] == matrix_a[n3][m3] == winn:
        res = True
    else:
        res = False
    return res


def check_player_for_win(ma_a, winn):

    # Функция проверки на победу по верхней горизонтали.
    res = winner(ma_a, 1, 1, 1, 2, 1, 3, winn)
    if not res:
    # Функция проверки на победу по средней горизонтали.
        res = winner(ma_a, 2, 1, 2, 2, 2, 3, winn)
    if not res:
    # Функция проверки на победу по нижней  горизонтали.
        res = winner(ma_a, 3, 1, 3, 2, 3, 3, winn)
    if not res:
    # Функция проверки на победу по диагонали их верхнего левого угла до нижнего правого угла.
        res = winner(ma_a, 1, 1, 2, 2, 3, 3, winn)
    if not res:
    # Функция проверки на победу по диагонали их верхнего правого угла до нижнего левого угла
        res = winner(ma_a, 1, 3, 2, 2, 3, 1, winn)
    if not res:
    # Функция проверки на победу по 1 вертикали.
        res = winner(ma_a, 1, 1, 2, 1, 3, 1, winn)
    if not res:
    # Функция проверки на победу по 2 вертикали.
        res = winner(ma_a, 1, 2, 2, 2, 3, 2, winn)
    if not res:
    # Функция проверки на победу по 3 вертикали.
        res = winner(ma_a, 1, 3, 2, 3, 3, 3, winn)
    return res


#  Функция проверки если выиграл игрок х
def win_player_x():
    print(f'**************************************')
    print(f'')
    print(f'*********  Выиграл игрок X ***********')
    print(f'*********  Выиграл игрок X ***********')
    print(f'')
    print(f'**************************************')
    print(f'')
    print(f'**************************************')
    print(f'************  конец игры! ************')



#  Функция проверки если выиграл игрок о
def win_player_o():
    print(f'**************************************')
    print(f'')
    print(f'*********  Выиграл игрок O ***********')
    print(f'*********  Выиграл игрок O ***********')
    print(f'')
    print(f'**************************************')
    print(f'')
    print(f'**************************************')
    print(f'************  конец игры! ************')


#  Функция проверки если ничья
def both_win():
    print(f'**************************************')
    print(f'')
    print(f'*********  Ничья ***********')
    print(f'*********  Выиграли оба игрока  ***********')
    print(f'')
    print(f'**************************************')
    print(f'')
    print(f'**************************************')
    print(f'************  конец игры! ************')


def check_for_win(step, matrix_, won_x, won_o):
    if step == 5:
        won_x = check_player_for_win(matrix_, 'x')
    if step == 7 or step == 9:
        if not won_x:
            won_x = check_player_for_win(matrix_, 'x')
    if step == 6:
        won_o = check_player_for_win(matrix_, 'o')
    if step == 8:
        if not won_x:
            won_o = check_player_for_win(matrix_, 'o')
    return won_x, won_o


def who_won(step_):
    res = False
    if step_ == 6 or step_ == 8 or step_ == 9:
        if winner_x and not winner_o:
            win_player_x()
            res = True
        if not winner_x and winner_o:
            win_player_o()
            res = True
        if winner_x and winner_o:
            both_win()
            res = True
    return res
while True:
    print()
    print(f'Теперь вводит игрок: {userN}')
    row, col = input_coordinate(matrix_size)
    print()
    steps = fill_matrix(userN, row, col, steps)
    winner_x, winner_o = check_for_win(steps, matrix, winner_x, winner_o)
    if who_won(steps):
        break
    userN = change_user(userN)

# *****************************************************************************************************************
