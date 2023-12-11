import time
from tkinter.constants import CURRENT, S
from turtle import color
import numpy as np
import tkinter as tk
from PIL import ImageTk, Image
from numpy.lib.function_base import delete

np.random.seed(1)
PhotoImage = ImageTk.PhotoImage
UNIT = 100
HEIGHT = 10
WIDTH = 10
CURRENTROUND = 0


class Env(tk.Tk):
    def __init__(self):
        super(Env, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
        self.n_actions = len(self.action_space)
        self.title('Q Learning  Round:' + str(CURRENTROUND + 1))
        self.geometry('{0}x{1}'.format(HEIGHT * UNIT, HEIGHT * UNIT))
        self.shapes = self.load_images()
        self.canvas = self._build_canvas()
        self.currentRound = 0
        self.isDisplayValue = False
        self.isDisplayArrow = False
        # self.isDisplayPause = False
        self.isStar = True
        # self.isPause = False
        self.texts = []
        self.arrows = []

    def changeStatus(self):
        self.isDisplayValue = not self.isDisplayValue

    def changeStatus2(self):
        self.isDisplayArrow = not self.isDisplayArrow

    # def changeStatus3(self):
    #     self.isDisplayPause = not self.isDisplayPause

    def updateRound(self, n):
        CURRENTROUND = n
        self.title('Q Learning')
        temp = 'Round:' + str(CURRENTROUND + 1)
        x_dis = 20
        tk.Label(self, text=temp, font=(
            'Helvetica', '20')).place(x=x_dis, y=100)
        tk.Button(self, text='Show/Hide Values',
                  command=self.changeStatus, font=('Helvetica', '20')).place(x=x_dis, y=200)
        tk.Button(self, text='Show/Hide Arrows',
                  command=self.changeStatus2, font=('Helvetica', '20')).place(x=x_dis, y=300)
        # 游戏暂停
        # tk.Button(self, text='Start/Pause', fg='red',
        #           command=self.changeStatus3, font=('Helvetica', '20')).place(x=x_dis, y=400)

    def _build_canvas(self):
        canvas = tk.Canvas(self, bg='white',
                           height=HEIGHT * UNIT,
                           width=WIDTH * UNIT)
        # create grids
        for c in range(0, WIDTH * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = c, 0, c, HEIGHT * UNIT
            canvas.create_line(x0, y0, x1, y1, fill='black')
        for r in range(0, HEIGHT * UNIT, UNIT):  # 0~400 by 80
            x0, y0, x1, y1 = 0, r, HEIGHT * UNIT, r
            canvas.create_line(x0, y0, x1, y1, fill='black')

        # add img to canvas
        self.mouse = canvas.create_image(50, 50, image=self.shapes[0])
        self.trap1 = canvas.create_image(150, 150, image=self.shapes[1])
        self.trap2 = canvas.create_image(150, 250, image=self.shapes[1])
        self.cat1 = canvas.create_image(250, 350, image=self.shapes[5])
        self.cat2 = canvas.create_image(50, 450, image=self.shapes[5])
        self.trap3 = canvas.create_image(150, 550, image=self.shapes[1])
        self.cat3 = canvas.create_image(450, 50, image=self.shapes[5])
        self.cat4 = canvas.create_image(650, 250, image=self.shapes[5])
        self.trap4 = canvas.create_image(450, 450, image=self.shapes[1])
        self.trap5 = canvas.create_image(550, 650, image=self.shapes[1])
        self.cat5 = canvas.create_image(850, 650, image=self.shapes[5])
        self.cat6 = canvas.create_image(850, 750, image=self.shapes[5])

        # self.star = canvas.create_image(950, 750, image=self.shapes[3])
        # self.circle = canvas.create_image(950, 750, image=self.shapes[2])
        self.cheese = canvas.create_image(950, 750, image=self.shapes[4])

        # pack all
        canvas.pack()

        return canvas

    def load_images(self):
        mouse = PhotoImage(
            Image.open("img/mouse.png").resize((65, 65)))
        trap = PhotoImage(
            Image.open("img/trap.png").resize((65, 65)))
        circle = PhotoImage(
            Image.open("img/circle.png").resize((65, 65)))
        star = PhotoImage(
            Image.open("img/star.png").resize((65, 65)))
        cheese = PhotoImage(
            Image.open("img/cheese.png").resize((65, 65)))
        cat = PhotoImage(
            Image.open("img/cat.png").resize((65, 65)))

        return mouse, trap, circle, star, cheese, cat

    def text_value(self, row, col, contents, action, color, font='Helvetica', size=15,
                   style='normal', anchor="nw"):
        if action == 0:
            origin_x, origin_y = 7, 42
        elif action == 1:
            origin_x, origin_y = 85, 42
        elif action == 2:
            origin_x, origin_y = 42, 5
        else:
            origin_x, origin_y = 42, 77

        x, y = origin_y + (UNIT * col), origin_x + (UNIT * row)
        font = (font, str(size), style)
        text = self.canvas.create_text(x, y, fill=color, text=contents,
                                       font=font, anchor=anchor)
        return self.texts.append(text)

    def arrow_value(self, row, col, action):
        if action == 0:
            # 上
            x, y = (UNIT * col + 50), (UNIT * row - 50)
        elif action == 1:
            # 下
            x, y = (UNIT * col + 50), (UNIT * row + 150)
        elif action == 2:
            # 左
            x, y = (UNIT * col - 50), (UNIT * row + 50)
        else:
            # 右
            x, y = (UNIT * col + 150), (UNIT * row + 50)

        arrow = self.canvas.create_line(
            (UNIT * col + 50), (UNIT * row + 50), x, y, arrow=tk.LAST, fill='black')
        return self.arrows.append(arrow)

    # def pause_value(self):
    #     if self.isDisplayPause:
    #         self.isPause = not self.isPause
    #     return self.isPause

    def print_value_all(self, q_table):
        for i in self.texts:
            self.canvas.delete(i)
        self.texts.clear()

        if self.isDisplayValue:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    for action in range(0, 4):
                        state = [i, j]
                        if str(state) in q_table.keys():
                            temp = q_table[str(state)][action]
                            if temp == max(q_table[str(state)]) and temp != 0:
                                self.text_value(j, i, round(
                                    temp, 2), action, 'red')
                            else:
                                self.text_value(j, i, round(
                                    temp, 2), action, 'black')

    def print_arrows_all(self, q_table):
        for i in self.arrows:
            self.canvas.delete(i)
        self.arrows.clear()

        if self.isDisplayArrow:
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    state = [i, j]
                    if str(state) in q_table.keys():
                        action = np.argmax(q_table[str(state)])
                        if q_table[str(state)][action] == max(q_table[str(state)]) and q_table[str(state)][action] != 0:
                            self.arrow_value(j, i, action)

    def coords_to_state(self, coords):
        x = int((coords[0] - 50) / 100)
        y = int((coords[1] - 50) / 100)
        return [x, y]

    def state_to_coords(self, state):
        x = int(state[0] * 100 + 50)
        y = int(state[1] * 100 + 50)
        return [x, y]

    def reset(self):
        self.update()
        time.sleep(0.5)
        x, y = self.canvas.coords(self.mouse)
        self.canvas.move(self.mouse, UNIT / 2 - x, UNIT / 2 - y)
        self.render()
        # return observation
        return self.coords_to_state(self.canvas.coords(self.mouse))

    def step(self, action):
        state = self.canvas.coords(self.mouse)
        base_action = np.array([0, 0])
        self.render()

        if action == 0:  # up
            if state[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:  # down
            if state[1] < (HEIGHT - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 2:  # left
            if state[0] > UNIT:
                base_action[0] -= UNIT
        elif action == 3:  # right
            if state[0] < (WIDTH - 1) * UNIT:
                base_action[0] += UNIT

        # 移动

        self.canvas.move(self.mouse, base_action[0], base_action[1])
        self.canvas.tag_raise(self.mouse)

        next_state = self.canvas.coords(self.mouse)



        # 判断得分条件
        if next_state == self.canvas.coords(self.cheese):
            reward = 500
            done = True
        # 遇到猫直接被吃，游戏重开
        elif next_state in [self.canvas.coords(self.cat1),
                            self.canvas.coords(self.cat2),
                            self.canvas.coords(self.cat3),
                            self.canvas.coords(self.cat4),
                            self.canvas.coords(self.cat5),
                            self.canvas.coords(self.cat6),
                            ]:
            reward = -100
            done = True
        # 遇到陷阱，不会死，但是要扣分
        elif next_state in [self.canvas.coords(self.trap1),
                            self.canvas.coords(self.trap2),
                            self.canvas.coords(self.trap3),
                            self.canvas.coords(self.trap4),
                            self.canvas.coords(self.trap5),
                            ]:
            reward = -200
            done = False
        else:
            reward = 0
            done = False

        next_state = self.coords_to_state(next_state)
        return next_state, reward, done

    # 渲染环境
    def render(self):
        time.sleep(0.05)
        self.update()
