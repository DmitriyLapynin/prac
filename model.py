from bookShop import BookShop
from book import Partition
from typing import List
from order import BookOrder

import tkinter as tk
from tkinter import ttk
import random


'''class Model:

    def __init__(self, period, step, file_name):
        self.period: int  # период моделирования
        self.step: int  # шаг моделирования
        self.stat: dict  # статистика
        self.file: str  # названия файла с книгами
        self.book_shop: BookShop  # книжный магазин


    # 1) Функция начала отрисовки экрана при запуске приложения
    def start(self):
        pass

    # 2) Начать заново
    def restart(self):
        pass

    # 3) Сделать один шаг
    def make_step(self):
        pass

    # 4) Посчитать статистику
    def calc_stat(self):
        pass

    # 5) Вывести статистику
    def show_stat(self):
        pass

    # 6) Генерация списка закаызваемых книг
    def generate_books(self) -> List[Book] :
        pass

    # 6) Выполнение заявки на книгу и обновление ассортимента книжного магазина
    def make_book_order(self):
        pass

    # 7) Выполнение заявки в издательство и обновление ассортимента книжного магазина
    def make_publish_order(self):
        pass'''




class Model:
    publishing_days = range(1, 6)  # диапазон кол-ва дней, в течении которого выполняется заявка в издательство
    books_num = range(1, 5)  # диапазон кол-ва заказываемых книг одним заказчиком
    books_copies = range(1, 4)  # диапазон кол-ва копий при заказе конкретной книги

    def __init__(self, period=10, step=1, orders_num=1, file_name="book_shop.csv"):
        self.system_period = period  # период моделирования работы
        self.system_step = step  # шаг моделирования
        self.current_day = 0  # текущий день моделирования
        self.orders_num = range(1, orders_num + 1)
        random.seed(1)
        self.customers = ["Петров", "Сидоров", "Кузнецова", "Лямкина", "Андреев", "Фёдорова"]
        self.book_file = file_name
        self.book_shop = BookShop(self.book_file)
        self.book_list = self.book_shop.book_list
        self.statistics = {}
        self.button_flag = True

    # герерируем список книг
    def generate_book_orders(self, day: int) -> List[BookOrder]:
        orders = []
        for k in range(random.choice(self.orders_num)):
            books_num = random.choice(self.books_num)
            books_indexes = random.sample(range(len(self.book_list)), books_num)
            book_list = [None] * books_num
            for i, j in enumerate(books_indexes):
                book_list[i] = Partition(random.choice(self.books_copies))
                is_None = random.choices([0, 1, 2], [0.6, 0.2, 0.2])[0]
                if is_None == 0:
                    book_list[i].book.name = self.book_list[j].book.name
                elif is_None == 1:
                    book_list[i].book.author = self.book_list[j].book.author
                else:
                    book_list[i].book.name = self.book_list[j].book.name
                    book_list[i].book.author = self.book_list[j].book.author
            customer = random.choice(self.customers)
            phone = '+79' + ''.join(random.choices([str(i) for i in range(10)], k=9))
            orders.append(BookOrder(day, customer, phone, book_list))
            orders[k].books_num = orders[k].get_books_num()
        return orders

    # Отрисовка интерфейса
    def start(self):
        labels = ["Дни моделирования:",
                  "Шаг моделирования:",
                  "Кол-во заказов в один день:"
                  ]

        entry = [None] * len(labels)

        window = tk.Tk()
        window.title("Книжный магазин")
        window.geometry("1030x800")
        window.resizable(width=False, height=False)
        window['bg'] = '#AFEEEE'
        self.window = window

        frame_5 = tk.Frame(window, bg='#AFEEEE')  # '#ded7bf')
        frame_5.grid(row=0, column=0, padx=10, pady=1, sticky="nsew")

        parameters = tk.Frame(frame_5, bg='#AFEEEE')
        parameters.grid(row=0, column=0, padx=10, pady=1, sticky="nsew")
        for i, text in enumerate(labels):
            label = tk.Label(parameters, text=text,
                             bg='#AFEEEE', font="calibri 14")
            from_ = 1 if i > 0 else 10
            to = 10 if i > 0 else 30
            entry[i] = tk.Spinbox(parameters, from_=from_, to=to, width=20, font="calibri 14")
            label.grid(row=i, column=0, sticky="w")
            entry[i].grid(row=i, column=1)
        res = tk.Frame(frame_5, bg='#AFEEEE')
        res.grid(row=0, column=1, padx=20, pady=15, sticky="nsew")
        res_1 = tk.Label(res, text='Число проданных книг',
                             bg='#AFEEEE', font="calibri 14")
        res_1.grid(row=0, column=0)
        en_1 = tk.Entry(res, width=7, font="calibri 14")
        en_1.grid(row=0, column=1)
        res_2 = tk.Label(res, text='Прибыль',
                         bg='#AFEEEE', font="calibri 14")
        res_2.grid(row=1, column=0)
        en_2 = tk.Entry(res, width=12, font="calibri 14")
        en_2.grid(row=1, column=1)
        frame_buttons = tk.Frame(bg='#AFEEEE')
        # frame_buttons.pack(fill=tk.X, ipadx=5, ipady=5)
        self.entry = entry
        self.en_1 = en_1
        self.en_2 = en_2




        frame_1 = tk.Frame(window)
        frame_1.grid(row=1, column=0, padx=10, pady=20, sticky="nsew")

        title = tk.Label(frame_1, text='Коллекция магазина', bg='#F4A460', font=('Calibri', 10, 'bold'))
        title.grid(row=0, column=0, sticky="nwes")
        frame_books = tk.Frame(frame_1)
        frame_books.grid(row=1, column=0, sticky="s")

        book_scroll = tk.Scrollbar(frame_books)
        book_scroll.pack(side=tk.RIGHT, fill=tk.Y)  # vertical scrollbar

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 9))  # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 10))  # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders

        book_table = ttk.Treeview(frame_books, yscrollcommand=book_scroll.set, style="mystyle.Treeview", height=7)
        book_scroll.config(command=book_table.yview)
        book_table.pack()

        book_table['columns'] = self.book_shop.headers + ["Цена", "Кол-во"]

        book_table.column("#0", width=0, stretch=tk.NO)
        for i, column in enumerate(book_table['columns']):
            if i == 0:
                w = 200
            elif i < 7:
                w = 120
            else:
                w = 70
            book_table.column(column, anchor="w", width=w)

        book_table.heading("#0", text="", anchor=tk.CENTER)
        for column in book_table['columns']:
            book_table.heading(column, text=column, anchor=tk.CENTER)

        self.book_table = book_table
        self.fill_book_table()


        frame_2 = tk.Frame(window, bg='#AFEEEE')
        frame_2.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

        for k, text_title in enumerate(["Заказы на книги", "Заявки в издательства"]):
            frame_22 = tk.Frame(frame_2)
            frame_22.grid(row=k, column=0, padx=10)

            title = tk.Label(frame_22, text=text_title, bg='#F4A460', font=('Calibri', 10, 'bold'))
            title.grid(row=0, column=0, sticky="nwes")
            frame_order = tk.Frame(frame_22)
            frame_order.grid(row=1, column=0, sticky="s")

            scroll = tk.Scrollbar(frame_order)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

            order_table = ttk.Treeview(frame_order, yscrollcommand=scroll.set, style="mystyle.Treeview", height=7)
            scroll.config(command=order_table.yview)
            order_table.pack()

            if k == 0:
                order_table['columns'] = ["Клиент", "Книги", "Кол-во", "Статус", "День"]
            else:
                order_table['columns'] = ["Издательство", "Книги", "Кол-во", "Статус", "День"]

            order_table.column("#0", width=0, stretch=tk.NO)
            for i, column in enumerate(order_table['columns']):
                w = 70 if i >= 2 else 110
                w = 180 if i == 1 else w
                order_table.column(column, anchor="w", width=w)

            order_table.heading("#0", text="", anchor=tk.CENTER)
            for column in order_table['columns']:
                order_table.heading(column, text=column, anchor=tk.CENTER)

            if k == 0:
                self.order_table = order_table
            else:
                self.applic_table = order_table


        frame_buttons = tk.Frame(frame_2, bg='#AFEEEE', bd=5)
        frame_buttons.grid(row=1, column=1, padx=10, pady=40)

        buttons = [None] * 3
        button_text = ["Сделать шаг", "До конца", "Начать заново"]
        button_command = [self.make_system_step, self.make_all_steps, self.restart]
        for i in range(3):
            buttons[i] = tk.Button(frame_buttons, text=button_text[i], background="#AA0000", foreground="black",
                                   activebackground="#483D8B", justify="center", padx="5", pady="5", font="calibri 12",
                                   width=16, command=button_command[i])
            # buttons[i].pack()
            # buttons[i].place(x=5, y=50*i)
            buttons[i].grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
            if i == 0:
                self.next_button = buttons[i]
        self.but_1 = buttons[1]
        window.mainloop()


    # Действие для кнопки нажать заново
    def restart(self):
        self.current_day = 0
        self.book_shop = BookShop(self.book_file)
        self.statistics = {}
        self.show_stats()

        self.next_button['text'] = "Сделать шаг"
        self.button_flag = True

        self.book_table.delete(*self.book_table.get_children())
        self.fill_book_table()

        self.order_table.delete(*self.order_table.get_children())
        self.applic_table.delete(*self.applic_table.get_children())

    # Сделать один шаг
    def make_step(self):
        if self.button_flag:
            if self.current_day == self.system_period:
                self.window.destroy()
                return

            self.current_day += 1

            # generated_orders = self.randomizer.generate_book_orders(self.current_day)
            generated_orders = self.generate_book_orders(self.current_day)
            prev_odd = len(self.book_shop.orders) % 2 != 0
            self.add_new_orders_to_table(generated_orders, self.order_table, prev_odd)

            self.book_shop.orders.extend(generated_orders)

            self.next_button['text'] = "Выполнить заказы"
            self.button_flag = False

        else:
            self.deal_with_book_orders()
            self.calc_stats()

            self.next_button['text'] = "Сделать шаг"
            self.button_flag = True

        self.show_stats()

    # Действие для кнопки Сделать шаг
    def make_system_step(self):
        self.system_period = int(self.entry[0].get())
        self.system_step = int(self.entry[1].get())
        self.orders_num = range(1, int(self.entry[2].get()) + 1)
        if self.current_day == self.system_period:
            self.window.destroy()
            return
        elif self.current_day > self.system_period:
            return

        for i in range(self.system_step):
            if self.current_day == self.system_period:
                # self.but_1.pack_forget()
                return
            else:
                self.make_step()

    # Действие для кнопки завершить
    def make_all_steps(self):
        self.system_period = int(self.entry[0].get())
        self.system_step = int(self.entry[1].get())
        self.orders_num = range(1, int(self.entry[2].get()) + 1)
        if self.current_day == self.system_period:
            self.window.destroy()
            return
        elif self.current_day > self.system_period:
            return

        if not self.button_flag: self.make_step()
        for i in range(self.current_day, self.system_period):
            self.make_step()
            self.make_step()


    def deal_with_book_orders(self):
        new_applications = self.book_shop.try_to_execute_orders(self.current_day)

        prev_odd = len(self.book_shop.applications) % 2 != 0
        self.add_new_orders_to_table(new_applications, self.applic_table, prev_odd)

        self.check_publishing_applications()
        self.book_shop.get_arrived_books_from_publishing()

        self.change_orders_in_table(self.book_shop.orders[::-1], self.order_table)
        self.change_orders_in_table(self.book_shop.applications[::-1], self.applic_table)
        self.change_book_table()

    def check_publishing_applications(self):
        for application in self.book_shop.applications:
            # publishing_days = random.choice(self.randomizer.publishing_days)
            publishing_days = random.choice(self.publishing_days)
            if application.day + publishing_days <= self.current_day:
                application.status = next(next(application.status))

    def add_new_orders_to_table(self, orders, order_table, prev_odd):
        for i, order in enumerate(orders):
            tag = ('even',) if (prev_odd + i) % 2 == 0 else ('odd',)
            id_order = order_table.insert(parent='', index=0, text='', open=False,
                                          values=(order.name, "Щёлкните 2 раза, чтобы увидеть", order.books_num, order.status.value, order.day),
                                          tags=tag)
            for j, part in enumerate(order.book_list):
                tag = ('even',) if (i + j + 1) % 2 == 0 else ('odd',)
                info = order.phone if j == 0 and order.__class__ == BookOrder else ""
                order_table.insert(parent=id_order, index='end', text='',
                                   values=(info, part.book.get_name(), part.cnt_copy, "", ""), tags=tag)
            order_table.tag_configure('odd', background='#d5e0eb')
            order_table.tag_configure('even', background='#c8d2db')

    def change_orders_in_table(self, orders, order_table):
        for i, order in enumerate(orders):
            order_to_change = order_table.get_children()[i]
            # print(order_to_change, order_table.item(order_to_change, 'values'))
            if int(order_table.item(order_to_change, 'values')[2]) != 0:
                order_table.item(order_to_change,
                                 values=(order.name, "Щёлкните 2 раза, чтобы увидеть", order.books_num, order.status.value, order.day))
                for j, part in enumerate(order.book_list):
                    book_to_change = order_table.get_children(order_to_change)[j]
                    info = order.phone if j == 0 and order.__class__ == BookOrder else ""
                    order_table.item(book_to_change, values=(info, part.book.get_name(), part.cnt_copy, "", ""))

    def fill_book_table(self):
        for i, part in enumerate(self.book_shop.book_list):
            tag = ('even',) if i % 2 == 0 else ('odd',)
            self.book_table.insert(parent='', index='end', iid=i, text='',
                                   values=part.book.get_args() + (part.cnt_copy,), tags=tag)
            self.book_table.tag_configure('odd', background='#d5e0eb')
            self.book_table.tag_configure('even', background='#c8d2db')

    def change_book_table(self):
        for i, part in enumerate(self.book_shop.book_list):
            book_to_change = self.book_table.get_children()[i]
            self.book_table.item(book_to_change, text='', values=part.book.get_args() + (part.cnt_copy,))

    def calc_stats(self):
        """ Функция подсчета статистики """
        self.statistics["Кол-во проданных книг"] = sum(map(lambda b: b.cnt_copy, self.book_shop.sold))
        self.statistics["Прибыль"] = self.book_shop.income

    def show_stats(self):
        for i, (key, value) in enumerate(self.statistics.items()):
            if i == 0:
                self.en_1.delete(0, last='end')
                self.en_1.insert(0, str(value) + " штук")
            elif i == 1:
                self.en_2.delete(0, last='end')
                self.en_2.insert(0, str(value) + " руб.")