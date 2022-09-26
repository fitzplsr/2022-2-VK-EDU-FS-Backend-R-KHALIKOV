class TicTacGame:
    def __init__(self):
        self.cells = ["_"] * 9
        self.letters = ['a', 'b', 'c']
        self.move = 'X'

    def show_board(self):
        print("  a  b  c")
        for i in range(3):
            print(f"{i + 1} ", end='')
            for j in range(3):
                print(f"{self.cells[i * 3 + j]}  ", end='')
            print('')

    def validate_input(self, text):
        try:
            let, num = text
        except ValueError:
            return -1
        try:
            num = int(num)
        except ValueError:
            return -2
        if let not in self.letters or not 0 < num < 4:
            return -3
        index = self.letters.index(let) + (num - 1) * 3
        if self.cells[index] != '_':
            return -4
        return index + 1

    def start_game(self):
        count = 0
        work = True
        self.show_board()
        while work and count < 9:
            index = False
            while index < 1:
                text = input("Введите номер ячейки вида 'a1'\n")
                index = self.validate_input(text)
                self.print_err(index)
            index -= 1
            self.cells[index] = 'X' if count % 2 == 0 else '0'
            self.move = self.cells[index]
            self.show_board()
            work = not self.check_winner()
            count += 1
        if not work:
            print(f"Игра окончена. \"{self.move}\" победили")
        else:
            print("Игра окончена. Ничья")

    def check_winner(self):
        result = False
        for j in range(9):
            if not self.equal(j):
                continue
            for k in range(j + 1, 9):
                diff = k - j
                if self.equal(k) and (diff + k) < 9 and self.equal(diff + k):
                    if diff == 1 and j % 3 == 0:
                        result = True
                    elif diff == 2 and j == 2:
                        result = True
                    elif diff == 3:
                        result = True
        return result

    def equal(self, index):
        return self.cells[index] == self.move

    @staticmethod
    def print_err(err_num):
        match err_num:
            case -1:
                print("Неверное количество символов")
            case -2:
                print("Введен символ вместа числа")
            case -3:
                print("Такой ячейки не существует")
            case -4:
                print("Данная ячейка занята")


if __name__ == "__main__":
    GAME = TicTacGame()
    GAME.start_game()

