from bookShop import BookShop
from book import Partition
from typing import List
from order import BookOrder
import random





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
        # self.inter = Gui(self.book_shop)

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



    # Действие для кнопки нажать заново
    def restart(self):
        self.current_day = 0
        self.book_shop = BookShop(self.book_file)
        self.statistics = {}




    def check_publishing_applications(self):
        for application in self.book_shop.applications:
            # publishing_days = random.choice(self.randomizer.publishing_days)
            publishing_days = random.choice(self.publishing_days)
            if application.day + publishing_days <= self.current_day:
                application.status = next(next(application.status))

    def calc_stats(self):
        """ Функция подсчета статистики """
        self.statistics["Кол-во проданных различных книг"] = len(
            list(filter(lambda b: b.cnt_copy != 0, self.book_shop.sold)))
        self.statistics["Кол-во проданных экземпляров книг"] = sum(map(lambda b: b.cnt_copy, self.book_shop.sold))
        self.statistics["Кол-во выполненных заказов"] = len(
            list(filter(lambda o: o.status.is_done(), self.book_shop.orders)))
        self.statistics["Топ самых продаваемых книг"] = self.book_shop.top_sold()
        self.statistics["Топ самых читаемых авторов"] = self.book_shop.top_sold(groupby="author")
        self.statistics["Топ самых популярных категорий"] = self.book_shop.top_sold(groupby="category")
        self.statistics["Прибыль магазина"] = self.book_shop.income

    '''def calc_stats(self):
        """ Функция подсчета статистики """
        self.statistics["Кол-во проданных книг"] = sum(map(lambda b: b.cnt_copy, self.book_shop.sold))
        self.statistics["Прибыль"] = self.book_shop.income'''
