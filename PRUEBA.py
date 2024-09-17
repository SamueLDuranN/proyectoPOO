import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time


class CasinoGames:
    def __init__(self, root):
        self.root = root
        self.root.title("Casino Games")
        self.root.geometry("600x600")
        self.root.configure(bg="#2c3e50")

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        title = tk.Label(self.root, text="¡Bienvenido al Casino de Juegos!", font=('Arial', 24, 'bold'), bg="#2c3e50",
                         fg="#ecf0f1")
        title.pack(pady=20)

        button_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 20,
            'height': 2,
            'bg': '#e74c3c',
            'fg': '#ecf0f1',
            'bd': 2,
            'relief': 'raised'
        }

        self.btn_triki = tk.Button(self.root, text="Triki", **button_style, command=self.jugar_triki)
        self.btn_triki.pack(pady=10)

        self.btn_serpiente = tk.Button(self.root, text="Serpiente", **button_style, command=self.jugar_serpiente)
        self.btn_serpiente.pack(pady=10)

        self.btn_adivina = tk.Button(self.root, text="Adivina el Número", **button_style, command=self.jugar_adivina)
        self.btn_adivina.pack(pady=10)

        self.btn_piedra_papel = tk.Button(self.root, text="Piedra, Papel o Tijeras", **button_style,
                                          command=self.jugar_piedra_papel)
        self.btn_piedra_papel.pack(pady=10)

        self.btn_buscaminas = tk.Button(self.root, text="Buscaminas", **button_style, command=self.jugar_buscaminas)
        self.btn_buscaminas.pack(pady=10)

        self.btn_quien_quiere = tk.Button(self.root, text="Quién Quiere Ser Millonario", **button_style,
                                          command=self.jugar_quien_quiere)
        self.btn_quien_quiere.pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def jugar_triki(self):
        self.clear_frame()
        Triki(self.root)

    def jugar_serpiente(self):
        Serpiente(self.root)

    def jugar_adivina(self):
        AdivinaNumero(self.root)

    def jugar_piedra_papel(self):
        PiedraPapelTijeras(self.root)

    def jugar_buscaminas(self):
        Buscaminas(self.root)

    def jugar_quien_quiere(self):
        QuiereSerMillonario(self.root)


class Triki:
    def __init__(self, root):
        self.root = root
        self.turn = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]

        # Crear un Frame para la interfaz del juego
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(pady=20)

        self.create_game_interface()

    def create_game_interface(self):
        self.botones = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                self.botones[i][j] = tk.Button(self.game_frame, text="", width=10, height=3,
                                               command=lambda i=i, j=j: self.mark_cell(i, j))
                self.botones[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.status_label = tk.Label(self.root, text="Turno de: " + self.turn)
        self.status_label.pack(pady=10)

        restart_button = tk.Button(self.root, text="Reiniciar", command=self.reset_game)
        restart_button.pack(pady=10)

    def mark_cell(self, i, j):
        if self.board[i][j] == "":
            self.board[i][j] = self.turn
            self.botones[i][j].config(text=self.turn, state="disabled")

            if self.check_winner():
                messagebox.showinfo("Ganador", f"¡{self.turn} ha ganado!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Empate", "¡Es un empate!")
                self.reset_game()
            else:
                self.turn = "O" if self.turn == "X" else "X"
                self.status_label.config(text="Turno de: " + self.turn)

    def check_winner(self):
        # Comprobación horizontal, vertical y diagonal
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != "":
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != "":
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            return True
        return False

    def check_draw(self):
        for row in self.board:
            if "" in row:
                return False
        return True

    def reset_game(self):
        self.turn = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text="", state="normal")
        self.status_label.config(text="Turno de: " + self.turn)

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

class Serpiente:
    def __init__(self, root):
        self.root = root
        self.root.title("Serpiente")
        self.root.geometry("400x400")
        self.root.configure(bg="#2c3e50")

        self.create_game_interface()

    def create_game_interface(self):
        self.clear_frame()

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#27ae60")
        self.canvas.pack()

        self.snake = [(20, 20), (20, 40), (20, 60)]
        self.food = (100, 100)
        self.direction = "Right"

        self.draw_snake()
        self.draw_food()

        self.root.bind("<KeyPress>", self.change_direction)
        self.move_snake()

        self.restart_button = tk.Button(self.root, text="Volver al Menú Principal", font=('Arial', 16, 'bold'),
                                        bg='#e74c3c', fg='#ecf0f1', command=self.regresar_al_menu)
        self.restart_button.pack(pady=20)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        if self.direction == "Right":
            head_x += 20
        elif self.direction == "Left":
            head_x -= 20
        elif self.direction == "Up":
            head_y -= 20
        elif self.direction == "Down":
            head_y += 20

        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

        if self.check_collision():
            self.mostrar_mensaje("¡Has perdido!")
            return

        if new_head == self.food:
            self.snake.append(self.snake[-1])
            self.food = (random.randint(0, 19) * 20, random.randint(0, 19) * 20)
            self.draw_food()

        self.draw_snake()
        self.root.after(100, self.move_snake)

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="#3498db",
                                         tag="snake")

    def draw_food(self):
        self.canvas.delete("food")
        self.canvas.create_rectangle(self.food[0], self.food[1], self.food[0] + 20, self.food[1] + 20, fill="#e74c3c",
                                     tag="food")

    def change_direction(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            self.direction = event.keysym

    def check_collision(self):
        head_x, head_y = self.snake[0]
        if (head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or
                len(self.snake) != len(set(self.snake))):
            return True
        return False

    def mostrar_mensaje(self, mensaje):
        if messagebox.askyesno("Fin del juego", mensaje + "\n¿Quieres jugar de nuevo?"):
            self.create_game_interface()
        else:
            self.regresar_al_menu()

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class AdivinaNumero:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina el Número")
        self.root.geometry("300x200")
        self.root.configure(bg="#2c3e50")

        self.create_game_interface()

    def create_game_interface(self):
        self.clear_frame()

        self.number_to_guess = random.randint(1, 100)
        self.guesses = 0

        title = tk.Label(self.root, text="Adivina el Número", font=('Arial', 24, 'bold'), bg="#2c3e50", fg="#ecf0f1")
        title.pack(pady=20)

        self.entry = tk.Entry(self.root, font=('Arial', 16))
        self.entry.pack(pady=10)

        self.button = tk.Button(self.root, text="Adivinar", font=('Arial', 16, 'bold'), bg='#e74c3c', fg='#ecf0f1',
                                command=self.check_guess)
        self.button.pack(pady=10)

        self.restart_button = tk.Button(self.root, text="Volver al Menú Principal", font=('Arial', 16, 'bold'),
                                        bg='#e74c3c', fg='#ecf0f1', command=self.regresar_al_menu)
        self.restart_button.pack(pady=20)

    def check_guess(self):
        guess = int(self.entry.get())
        self.guesses += 1
        if guess < self.number_to_guess:
            messagebox.showinfo("Resultado", "Demasiado bajo!")
        elif guess > self.number_to_guess:
            messagebox.showinfo("Resultado", "Demasiado alto!")
        else:
            self.mostrar_mensaje(f"¡Correcto! Adivinaste en {self.guesses} intentos.")

    def mostrar_mensaje(self, mensaje):
        if messagebox.askyesno("Fin del juego", mensaje + "\n¿Quieres jugar de nuevo?"):
            self.create_game_interface()
        else:
            self.regresar_al_menu()

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class PiedraPapelTijeras:
    def __init__(self, root):
        self.root = root
        self.root.title("Piedra, Papel o Tijeras")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        self.create_game_interface()

    def create_game_interface(self):
        self.clear_frame()

        self.user_choice = None

        title = tk.Label(self.root, text="Piedra, Papel o Tijeras", font=('Arial', 24, 'bold'), bg="#2c3e50",
                         fg="#ecf0f1")
        title.pack(pady=20)

        button_style = {
            'font': ('Arial', 16, 'bold'),
            'width': 15,
            'height': 2,
            'bg': '#3498db',
            'fg': '#ecf0f1',
            'bd': 2,
            'relief': 'raised'
        }

        self.btn_piedra = tk.Button(self.root, text="Piedra", **button_style, command=lambda: self.jugar("Piedra"))
        self.btn_piedra.pack(pady=5)

        self.btn_papel = tk.Button(self.root, text="Papel", **button_style, command=lambda: self.jugar("Papel"))
        self.btn_papel.pack(pady=5)

        self.btn_tijeras = tk.Button(self.root, text="Tijeras", **button_style, command=lambda: self.jugar("Tijeras"))
        self.btn_tijeras.pack(pady=5)

        self.restart_button = tk.Button(self.root, text="Volver al Menú Principal", font=('Arial', 16, 'bold'),
                                        bg='#e74c3c', fg='#ecf0f1', command=self.regresar_al_menu)
        self.restart_button.pack(pady=20)

    def jugar(self, user_choice):
        choices = ["Piedra", "Papel", "Tijeras"]
        computer_choice = random.choice(choices)

        result = self.determine_winner(user_choice, computer_choice)
        message = f"Tu elección: {user_choice}\nElección de la máquina: {computer_choice}\n{result}"

        if messagebox.askyesno("Resultado", message + "\n¿Quieres jugar de nuevo?"):
            self.create_game_interface()
        else:
            self.regresar_al_menu()

    def determine_winner(self, user, computer):
        if user == computer:
            return "Es un empate!"
        elif (user == "Piedra" and computer == "Tijeras") or \
                (user == "Papel" and computer == "Piedra") or \
                (user == "Tijeras" and computer == "Papel"):
            return "¡Ganaste!"
        else:
            return "¡La máquina gana!"

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class Buscaminas:
    def __init__(self, root):
        self.root = root
        self.root.title("Buscaminas")
        self.root.geometry("400x400")
        self.root.configure(bg="#2c3e50")

        self.create_game_interface()

    def create_game_interface(self):
        self.clear_frame()

        self.grid_size = 10
        self.bomb_count = 10
        self.buttons = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.bombs = set()
        self.revealed = set()

        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#27ae60")
        self.canvas.pack()

        self.restart_button = tk.Button(self.root, text="Volver al Menú Principal", font=('Arial', 16, 'bold'),
                                        bg='#e74c3c', fg='#ecf0f1', command=self.regresar_al_menu)
        self.restart_button.pack(pady=20)

        self.place_bombs()
        self.create_buttons()

    def place_bombs(self):
        while len(self.bombs) < self.bomb_count:
            bomb = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
            self.bombs.add(bomb)

    def create_buttons(self):
        button_style = {
            'font': ('Arial', 10, 'bold'),
            'width': 4,
            'height': 2,
            'bg': '#3498db',
            'fg': '#ecf0f1',
            'bd': 2,
            'relief': 'raised'
        }

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                btn = tk.Button(self.canvas, text=" ", **button_style, command=lambda x=i, y=j: self.reveal(x, y))
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.buttons[i][j] = btn

    def reveal(self, x, y):
        if (x, y) in self.bombs:
            self.show_bombs()
            self.mostrar_mensaje("¡Boom! Has perdido.")
            return

        self.revealed.add((x, y))
        self.update_button(x, y)
        # Todo: implement more logic for revealing cells, checking win conditions, etc.

    def update_button(self, x, y):
        self.buttons[x][y].config(bg='#95a5a6', text="0")

    def show_bombs(self):
        for (x, y) in self.bombs:
            self.buttons[x][y].config(bg='#e74c3c', text="X")

    def mostrar_mensaje(self, mensaje):
        if messagebox.askyesno("Fin del juego", mensaje + "\n¿Quieres jugar de nuevo?"):
            self.create_game_interface()
        else:
            self.regresar_al_menu()

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class QuiereSerMillonario:
    def __init__(self, root):
        self.root = root
        self.root.title("Quién Quiere Ser Millonario")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")

        self.create_game_interface()

    def create_game_interface(self):
        self.clear_frame()

        self.questions = [
            ("¿Cuál es la capital de Francia?", "París", ["Londres", "Berlín", "Madrid", "París"]),
            ("¿Qué es la fotosíntesis?", "Proceso por el cual las plantas producen su alimento",
             ["Un tipo de energía", "Proceso por el cual las plantas producen su alimento", "Un tipo de tejido",
              "Un sistema de riego"]),
            ("¿Quién escribió 'Cien años de soledad'?", "Gabriel García Márquez",
             ["Miguel de Cervantes", "Gabriel García Márquez", "Pablo Neruda", "Julio Cortázar"]),
            # Agrega más preguntas aquí
        ]
        self.current_question_index = 0

        self.title = tk.Label(self.root, text="Quién Quiere Ser Millonario", font=('Arial', 24, 'bold'), bg="#2c3e50",
                              fg="#ecf0f1")
        self.title.pack(pady=20)

        self.question_label = tk.Label(self.root, text="", font=('Arial', 16), bg="#2c3e50", fg="#ecf0f1")
        self.question_label.pack(pady=20)

        self.options = []
        for i in range(4):
            btn = tk.Button(self.root, text="", font=('Arial', 14), bg='#3498db', fg='#ecf0f1',
                            command=lambda i=i: self.check_answer(i))
            btn.pack(pady=5)
            self.options.append(btn)

        self.next_button = tk.Button(self.root, text="Siguiente Pregunta", font=('Arial', 16, 'bold'), bg='#e74c3c',
                                     fg='#ecf0f1', command=self.next_question)
        self.next_button.pack(pady=20)

        self.restart_button = tk.Button(self.root, text="Volver al Menú Principal", font=('Arial', 16, 'bold'),
                                        bg='#e74c3c', fg='#ecf0f1', command=self.regresar_al_menu)
        self.restart_button.pack(pady=20)

        self.next_question()

    def next_question(self):
        if self.current_question_index >= len(self.questions):
            self.mostrar_mensaje("¡Ganaste! Has respondido todas las preguntas.")
            return

        question, correct_answer, options = self.questions[self.current_question_index]
        self.question_label.config(text=question)

        random.shuffle(options)
        for i, option in enumerate(options):
            self.options[i].config(text=option, command=lambda opt=option: self.check_answer(opt))

    def check_answer(self, answer):
        question, correct_answer, _ = self.questions[self.current_question_index]
        if answer == correct_answer:
            self.mostrar_mensaje("¡Correcto!")
        else:
            self.mostrar_mensaje("Incorrecto. ¡Has perdido!")
        self.current_question_index += 1

    def mostrar_mensaje(self, mensaje):
        if messagebox.askyesno("Resultado", mensaje + "\n¿Quieres jugar de nuevo?"):
            self.current_question_index = 0
            self.next_question()
        else:
            self.regresar_al_menu()

    def regresar_al_menu(self):
        self.root.destroy()
        main = tk.Tk()
        CasinoGames(main)
        main.mainloop()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    main = tk.Tk()
    CasinoGames(main)
    main.mainloop()
