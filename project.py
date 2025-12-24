import random
import tkinter
import yaml
from PIL import ImageGrab
from docx import *
from docx.shared import Inches, Cm, Pt

with open('config.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

trajectory_list = []  # cписок для записи траекторий
trajectory_coords = []
answer = []
Document_Name = ''
Task_Description = ''
WINDOW_WIDTH = configuration['WINDOW_WIDTH']
WINDOW_HEIGHT = configuration['WINDOW_HEIGHT']
CELLSIZE = configuration['CELLSIZE']
TRAJECTORY_LENGTH = configuration['TRAJECTORY_LENGTH']
TRAJECTORY_AMOUNT = configuration['TRAJECTORY_AMOUNT']
TRAJECTORY_STEP = configuration['TRAJECTORY_STEP']
TASK_START_POINT_X = configuration['TASK_START_POINT_X']
TASK_START_POINT_Y = configuration['TASK_START_POINT_Y']
DIFFICULTY = configuration['DIFFICULTY']

WINDOW_COORD_X = 0
WINDOW_COORD_Y = 0


# --------------------------------------------FUNCTIONS-----------------------------------------------------------------
def CellSizing(n):
    return n * CELLSIZE


def TrajectoryRotater(n):
    angle = random.choice([0, 90, 180, 270])
    l = ['up', 'right', 'down', 'left', 'up', 'right', 'down', 'left']
    rotated = []

    for i in trajectory_list[n]:
        if angle == 0:
            rotated.append(l[l.index(i) + 0])
        elif angle == 90:
            rotated.append(l[l.index(i) + 1])
        elif angle == 180:
            rotated.append(l[l.index(i) + 2])
        elif angle == 270:
            rotated.append(l[l.index(i) + 3])

    return rotated


def MakeField():
    Document_Name = input('Введите название документа: \n')
    Task_Description = input('Введите описание задания: \n')

    if input('Создать новый документ/открыть существующий? (1/2): \n') == '1':
        document = Document()
    else:
        document = Document(Document_Name + '.docx')

    document.add_paragraph('Задание "Траектория"')
    document.add_paragraph(Task_Description)

    master = tkinter.Tk()
    canvas = tkinter.Canvas(master, bg='white', height=WINDOW_HEIGHT, width=WINDOW_WIDTH)  # Cоздание холста
    master.attributes('-fullscreen', False)
    for i in range(CELLSIZE, WINDOW_WIDTH, CELLSIZE):
        canvas.create_line((i, 0), (i, WINDOW_HEIGHT), fill='black')
    for i in range(CELLSIZE, WINDOW_WIDTH, CELLSIZE):
        canvas.create_line((0, i), (WINDOW_WIDTH, i), fill='black')
    # Рисование клеток

    DefaultPoint = [CellSizing(8), CellSizing(6)]
    TrajectoryStartPoint = [CellSizing(8), CellSizing(6)]  # Исходная точка траектории

    for i in range(TRAJECTORY_AMOUNT):
        trajectory_list.append([])
        trajectory_coords.append([])

    # Генерация траекторий

    for j in range(TRAJECTORY_AMOUNT):
        canvas.create_oval((TrajectoryStartPoint[0], TrajectoryStartPoint[1]),
                           (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=7,
                           outline='red')  # рисуем точку начала траектории

        PreviousRandomNumber = 0
        trajectory_coords[j].append(TrajectoryStartPoint)

        for i in range(TRAJECTORY_LENGTH):
            RandomNumber = random.randint(1, 4)  # Случайное число для генерации поворотов
            lenght = 1  # длина поворота
            while abs(PreviousRandomNumber - RandomNumber) == 2:
                # while (
                # RandomNumber == 4 and [TrajectoryStartPoint[0], TrajectoryStartPoint[1] - CellSizing(1)] in
                # trajectory_coords[j]) or (
                # RandomNumber == 2 and [TrajectoryStartPoint[0], TrajectoryStartPoint[1] + CellSizing(1)] in
                # trajectory_coords[j]) or (
                # RandomNumber == 1 and [TrajectoryStartPoint[0] + CellSizing(1), TrajectoryStartPoint[1]] in
                # trajectory_coords[j]) or (
                # RandomNumber == 3 and [TrajectoryStartPoint[0] - CellSizing(1), TrajectoryStartPoint[1]] in
                # trajectory_coords[j]):
                RandomNumber = random.randint(1, 4)

            if RandomNumber == 4:
                canvas.create_line((TrajectoryStartPoint[0], TrajectoryStartPoint[1] - CellSizing(1)),
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)

                TrajectoryStartPoint[1] = TrajectoryStartPoint[1] - CellSizing(1)
                trajectory_list[j].append('up')

            elif RandomNumber == 2:
                canvas.create_line((TrajectoryStartPoint[0], TrajectoryStartPoint[1] + CellSizing(1)),
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)

                TrajectoryStartPoint[1] = TrajectoryStartPoint[1] + CellSizing(1)
                trajectory_list[j].append('down')

            else:
                match RandomNumber:
                    case 3:
                        Step = CellSizing(-lenght)
                        trajectory_list[j].append('left')
                    case 1:
                        Step = CellSizing(lenght)
                        trajectory_list[j].append('right')
                canvas.create_line((TrajectoryStartPoint[0], TrajectoryStartPoint[1]),
                                   (TrajectoryStartPoint[0] + Step, TrajectoryStartPoint[1]), fill='red',
                                   width=3)  # рисуем линию
                TrajectoryStartPoint[0] = TrajectoryStartPoint[0] + Step

            trajectory_coords[j].append(TrajectoryStartPoint)
            PreviousRandomNumber = RandomNumber
        TrajectoryStartPoint = [DefaultPoint[0] + CellSizing((j + 1) * TRAJECTORY_STEP), DefaultPoint[1]]

    # Генерация задачи

    TrajectoryStartPoint = [CellSizing(TASK_START_POINT_X), CellSizing(TASK_START_POINT_Y)]
    canvas.create_oval((TrajectoryStartPoint[0], TrajectoryStartPoint[1]),
                       (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=7,
                       outline='red')

    for n in range(DIFFICULTY):
        trajectory_num = random.randint(0, TRAJECTORY_AMOUNT - 1)
        for i in TrajectoryRotater(trajectory_num):
            if i == 'up':
                canvas.create_line((TrajectoryStartPoint[0], TrajectoryStartPoint[1] - CellSizing(1)),
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)

                TrajectoryStartPoint[1] = TrajectoryStartPoint[1] - CellSizing(1)

            elif i == 'right':
                canvas.create_line((TrajectoryStartPoint[0] + CellSizing(1)), TrajectoryStartPoint[1],
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)

                TrajectoryStartPoint[0] = TrajectoryStartPoint[0] + CellSizing(1)

            elif i == 'down':
                canvas.create_line((TrajectoryStartPoint[0], TrajectoryStartPoint[1] + CellSizing(1)),
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)
                TrajectoryStartPoint[1] = TrajectoryStartPoint[1] + CellSizing(1)

            elif i == 'left':
                canvas.create_line((TrajectoryStartPoint[0] - CellSizing(1)), TrajectoryStartPoint[1],
                                   (TrajectoryStartPoint[0], TrajectoryStartPoint[1]), fill='red', width=3)

                TrajectoryStartPoint[0] = TrajectoryStartPoint[0] - CellSizing(1)

        answer.append(trajectory_num)

    # Сохранение файла

    label = tkinter.Label(master, text="Генератор задач с роботом", relief='raised')
    label.pack()
    canvas.pack()
    master.mainloop()
    screenshot = ImageGrab.grab(
        bbox=(15, 70, 1000, 1000))
    screenshot.save('screenshot.jpg')
    document.add_picture('screenshot.jpg', width=Cm(15), height=Cm(15))

    answer_str = ''
    for i in answer:
        answer_str += str(i + 1)

    document.add_paragraph(answer_str)
    document.save(Document_Name + '.docx')
    return trajectory_list


# ----------------------------------------------MAIN--------------------------------------------------------------------


MakeField()
