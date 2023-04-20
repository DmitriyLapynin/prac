import tkinter as tk
from tkinter import ttk
from model import Model

class Gui:


    def __init__(self):
        self.model = Model()
        self.key = False
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
            entry[i] = tk.Spinbox(parameters, from_=from_, to=to, width=20, state='readonly', font="calibri 14")
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

        book_table['columns'] = self.model.book_shop.headers + ["Цена", "Кол-во"]

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
        self.fill_books(self.model.book_list)

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
                order_table['columns'] = ["Клиент", "Книги", "Кол-во", "Выдано", "Статус", "День"]
            else:
                order_table['columns'] = ["Издательство", "Книги", "Кол-во", "Выдано", "Статус", "День"]

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

        res_day = tk.Label(frame_2, text='Текущий день',
                         bg='#AFEEEE', font="calibri 14")
        res_day.grid(row=0, column=1, padx=10, pady=40)
        en_3 = tk.Entry(frame_2, width=5, font="calibri 14")
        en_3.grid(row=0, column=2)
        self.en_3 = en_3
        self.en_3.insert(0, '0')
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
        self.text_box = None
        window.mainloop()


    def fill_books(self, book_list):
        for i, part in enumerate(book_list):
            tag = ('even',) if i % 2 == 0 else ('odd',)
            self.book_table.insert(parent='', index='end', iid=i, text='',
                                   values=part.book.get_args() + (part.cnt_copy,), tags=tag)
            self.book_table.tag_configure('odd', background='#d5e0eb')
            self.book_table.tag_configure('even', background='#c8d2db')


    # Действие для кнопки нажать заново
    def restart(self):
        '''self.window_2.protocol('WM_DELETE_WINDOW', self.change_state)
        if not self.key:
            self.window_2.destroy()'''
        self.model.restart()
        self.show_stats()
        self.en_3.delete(0, last='end')
        self.en_3.insert(0, '0')


        self.book_table.delete(*self.book_table.get_children())
        self.fill_books(self.model.book_list)

        self.order_table.delete(*self.order_table.get_children())
        self.applic_table.delete(*self.applic_table.get_children())
        self.entry[0].config(state='readonly')
        self.entry[2].config(state='readonly')

    def change_state(self):
        self.key = True


    def make_step(self):
        if self.model.current_day == self.model.system_period:
            self.window.destroy()
            return

        self.model.current_day += 1

        generated_orders = self.model.generate_book_orders(self.model.current_day)
        prev_odd = len(self.model.book_shop.orders) % 2 != 0

        self.draw_new_orders(generated_orders, self.order_table, prev_odd)
        self.model.book_shop.orders.extend(generated_orders)
        # self.next_button['text'] = "Выполнить заказы"
        self.deal_with_book_orders()
        self.model.calc_stats()
        self.show_stats()
        self.en_3.delete(0, last='end')
        self.en_3.insert(0, str(self.model.current_day))
        if self.model.current_day == self.model.system_period:
            self.end_stats()

    def make_system_step(self):
        if self.model.current_day == 0:
            self.model.system_period = int(self.entry[0].get())
            self.model.system_step = int(self.entry[1].get())
            self.model.orders_num = range(1, int(self.entry[2].get()) + 1)
            self.entry[0].config(state='disabled')
            self.entry[2].config(state='disabled')
        else:
            self.model.system_step = int(self.entry[1].get())
        if self.model.current_day == self.model.system_period:
            self.window.destroy()
            # self.inter.destroy()
            return
        elif self.model.current_day > self.model.system_period:
            return

        for i in range(self.model.system_step):
            if self.model.current_day == self.model.system_period:
                return
            else:
                self.make_step()

    def make_all_steps(self):
        if self.model.current_day == 0:
            self.model.system_period = int(self.entry[0].get())
            self.model.system_step = int(self.entry[1].get())
            self.model.orders_num = range(1, int(self.entry[2].get()) + 1)
            self.entry[0].config(state='disabled')
            self.entry[2].config(state='disabled')
        else:
            self.model.system_step = int(self.entry[1].get())
        if self.model.current_day == self.model.system_period:
            self.window.destroy()
            return
        elif self.model.current_day > self.model.system_period:
            return
        for i in range(self.model.current_day, self.model.system_period):
            self.make_step()

    def draw_restart(self):
        self.book_table.delete(*self.book_table.get_children())
        self.fill_books(self.model.book_list)

        self.order_table.delete(*self.order_table.get_children())
        self.applic_table.delete(*self.applic_table.get_children())

    def draw_new_orders(self, orders,  table, prev_odd):
        for i, order in enumerate(orders):
            tag = ('even',) if (prev_odd + i) % 2 == 0 else ('odd',)
            id_order = table.insert(parent='', index=0, text='', open=False,
                                          values=(order.name, "Щёлкните 2 раза, чтобы увидеть", order.books_num, "", order.status.value, order.day),
                                          tags=tag)
            for j, part in enumerate(order.book_list):
                tag = ('even',) if (i + j + 1) % 2 == 0 else ('odd',)
                # info = order.phone if j == 0 and order.__class__ == BookOrder else ""
                info = ""
                table.insert(parent=id_order, index='end', text='',
                                   values=(info, part.book.get_name(), part.tmp_copy, part.cnt_done, "", ""), tags=tag)
            table.tag_configure('odd', background='#d5e0eb')
            table.tag_configure('even', background='#c8d2db')

    def deal_with_book_orders(self):
        new_applications = self.model.book_shop.try_to_execute_orders(self.model.current_day)

        prev_odd = len(self.model.book_shop.applications) % 2 != 0
        self.draw_new_orders(new_applications, self.applic_table, prev_odd)

        self.model.check_publishing_applications()
        self.model.book_shop.get_arrived_books_from_publishing()

        self.change_orders_in_table(self.model.book_shop.orders[::-1], self.order_table)
        self.change_orders_in_table(self.model.book_shop.applications[::-1], self.applic_table)
        self.change_book_table()


    def change_orders_in_table(self, orders, order_table):
        for i, order in enumerate(orders):
            order_to_change = order_table.get_children()[i]
            if int(order_table.item(order_to_change, 'values')[2]) != 0:
                order_table.item(order_to_change,
                                 values=(order.name, "Щёлкните 2 раза, чтобы увидеть", order.books_num, "", order.status.value, order.day))
                for j, part in enumerate(order.book_list):
                    book_to_change = order_table.get_children(order_to_change)[j]
                    info = ""
                    order_table.item(book_to_change, values=(info, part.book.get_name(), part.tmp_copy, part.cnt_done, "", ""))

    def change_book_table(self):
        for i, part in enumerate(self.model.book_shop.book_list):
            book_to_change = self.book_table.get_children()[i]
            self.book_table.item(book_to_change, text='', values=part.book.get_args() + (part.cnt_copy,))

    def show_stats(self):
        for i, (key, value) in enumerate(self.model.statistics.items()):
            if i == 1:
                self.en_1.delete(0, last='end')
                self.en_1.insert(0, str(value) + " штук")
            elif i == 6:
                self.en_2.delete(0, last='end')
                self.en_2.insert(0, str(value) + " руб.")
            else:
                print(key, value)

    def end_stats(self):
        window_2 = tk.Tk()
        window_2.title("Статистика")
        window_2.geometry("645x470")
        window_2.resizable(width=False, height=False)
        window_2['bg'] = '#AFEEEE'
        self.window_2 = window_2
        '''frame_3 = tk.Frame(window_2, bg='#e8e1ca')  # '#ded7bf')
        frame_3.grid(row=0, column=0, sticky="nsew")'''
        text_box = tk.Text(window_2, wrap='word', font='calibri 12')
        text_box.pack(fill='both', expand=1)
        self.text_box = text_box
        self.text_box.config(state='normal')
        self.text_box.delete(1.0, 'end')
        self.text_box.insert(tk.END, f"День: {self.model.current_day}\n")
        for i, (key, value) in enumerate(self.model.statistics.items()):
            if i < 3:
                self.text_box.insert(tk.END, f"{key}: {value} шт.\n")
                if i == 2: self.text_box.insert(tk.END, "\n")
            elif i == 6:
                self.text_box.insert(tk.END, f"{key}: {value} руб.")
            else:
                self.text_box.insert(tk.END, f"{key}:\n" + '\n'.join([f"{i + 1}. {k} ({v})"
                                                                      for i, (k, v) in
                                                                      enumerate(value.items())]) + '\n\n')
        self.text_box.config(state='disabled')

