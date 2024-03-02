import tkinter as tk
import tkinter.messagebox
import random

class TicTacToe:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic Tac Toe")
        self.board_size = 3  # Set board size to 3x3
        self.create_gui()

    def create_gui(self):
        self.start_button = tk.Button(self.window, text="Start Game", command=self.start_game)
        self.start_button.grid(row=0, column=0, columnspan=self.board_size)

        self.ai_first_button = tk.Button(self.window, text="AI First", command=self.ai_first)
        self.ai_first_button.grid(row=1, column=0, columnspan=self.board_size)
        self.ai_first_button.grid_remove()  # Hide the "AI first" button initially

    def ai_first(self):
        if not self.is_game_over() and self.current_player == "X":
            self.current_player = "O"
            self.computer_move()

    def start_game(self):
        self.board = [[" " for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "X"
        self.buttons = []
        self.create_board_gui()
        self.ai_first_button.grid()  # Show the "AI first" button after "Start game" is pressed
        if self.current_player == "O":
            self.computer_move()

    def create_board_gui(self):
        for i in range(self.board_size):
            row_buttons = []
            for j in range(self.board_size):
                button = tk.Button(self.window, text=" ", font=('normal', 20), width=6, height=2,
                                   command=lambda row=i, col=j: self.on_click(row, col))
                button.grid(row=i + 2, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def on_click(self, row, col):
        if self.board[row][col] == " " and not self.is_game_over():
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.is_winner(self.current_player):
                self.show_winner(self.current_player)
            elif self.is_board_full():
                self.show_draw()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.computer_move()

    def computer_move(self):
        if not self.is_game_over():
            best_score = float("-inf")
            best_move = None

            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(self.board, 0, False)
                        self.board[i][j] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)

            if best_move:
                row, col = best_move
                self.board[row][col] = "O"
                self.buttons[row][col].config(text="O")
                if self.is_winner("O"):
                    self.show_winner("O")
                elif self.is_board_full():
                    self.show_draw()
                else:
                    self.current_player = "X"

    def minimax(self, board, depth, is_maximizing):
        if self.is_winner("O"):
            return 1
        elif self.is_winner("X"):
            return -1
        elif self.is_board_full():
            return 0

        if is_maximizing:
            best_score = float("-inf")
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def is_winner(self, player):
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        for col in range(self.board_size):
            if all(row[col] == player for row in self.board):
                return True

        for i in range(self.board_size):
            if all(self.board[i][i] == player for i in range(self.board_size)):
                return True

            if all(self.board[i][self.board_size - 1 - i] == player for i in range(self.board_size)):
                return True

        return False

    def is_board_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def is_game_over(self):
        return self.is_winner("X") or self.is_winner("O") or self.is_board_full()

    def show_winner(self, player):
        winner_label = tk.Label(self.window, text=f"Player {player} wins the game!")
        winner_label.grid(row=self.board_size + 1, columnspan=self.board_size)
        self.disable_buttons()
        tk.messagebox.showinfo("Winner", f"Player {player} wins!")

    def show_draw(self):
        draw_label = tk.Label(self.window, text="Match Draw!")
        draw_label.grid(row=self.board_size + 1, columnspan=self.board_size)
        self.disable_buttons()
        tk.messagebox.showinfo("Draw", "The game ends in a draw.")

    def clear_winner_label(self):
        for widget in self.window.winfo_children():
            if isinstance(widget, tk.Label) and "Player" in widget.cget("text"):
                widget.destroy()

    def clear_board_gui(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.grid_forget()
        self.buttons = []

    def disable_buttons(self):
        for row_buttons in self.buttons:
            for button in row_buttons:
                button.config(state=tk.DISABLED)

    def start(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.start()
