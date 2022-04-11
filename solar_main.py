# coding: utf-8
# license: GPLv3

import tkinter
from tkinter.filedialog import *
from solar_vis import *
from solar_model import *
from solar_input import *

# Hello
'''
perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""
'''

class Quantities:
    def __init__(self):
        self.physical_time = 0
        self.displayed_time = None
        self.time_step = None
        self.time_speed = None
        self.space = None
        self.start_button = None
        self.perform_execution = False

def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    #global physical_time
    #global displayed_time
    #global space_objects
    space_objects = recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    print("execute")

    if perform_execution:
        space.after(101 - int(time_speed.get()), execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    #global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    #global space_objects
    #global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if obj.type == 'star':
            create_star_image(space, obj)
        elif obj.type == 'planet':
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def main(quantities_class):
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    physical_time = quantities_class.physical_time
    displayed_time = quantities_class.displayed_time
    time_step = quantities_class.time_step
    time_speed = quantities_class.time_speed
    space = quantities_class.space
    start_button = quantities_class.start_button

    print('Modelling started!')
    quantities_class.physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    quantities_class.space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    quantities_class.space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    quantities_class.start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    quantities_class.start_button.pack(side=tkinter.LEFT)

    quantities_class.time_step = tkinter.DoubleVar()
    quantities_class.time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=quantities_class.time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    quantities_class.time_speed = tkinter.DoubleVar()
    scale = tkinter.Scale(frame, variable=quantities_class.time_speed, orient=tkinter.HORIZONTAL)
    scale.pack(side=tkinter.LEFT)

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    quantities_class.displayed_time = tkinter.StringVar()
    quantities_class.displayed_time.set(str(quantities_class.physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=quantities_class.displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)



    root.mainloop()
    print('Modelling finished!')

quantities = Quantities()

if __name__ == "__main__":
    main(quantities)
