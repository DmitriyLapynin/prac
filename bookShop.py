import csv
from copy import deepcopy
from typing import List, Tuple
from book import Book
from book import Partition
from order import PublishingOrder

class BookShop:
    start_margin = 5
    margin_new = 15
    start_rating = 5
    min_copies = 3
    start_copies = 5

    def __init__(self, books_file: str):
        self.book_list = self.init_books(books_file, self.start_margin, self.margin_new, self.start_rating)
        self.num_books = len(self.book_list) * self.start_copies
        self.orders = []
        self.sold = [deepcopy(part) for part in self.book_list]
        for part in self.sold:
            part.cnt_copy = 0
        self.applications = []
        self.income = 0

    # Получение списка книг из файла
    def init_books(self, books_file: str, margin, margin_new, rating) -> List[Partition]:
        with open(books_file, 'r', encoding='cp1251') as in_file:
            csv_reader = csv.reader(in_file, delimiter=';')  # quoting = csv.QUOTE_NONNUMERIC, quotechar='"')
            self.headers = next(csv_reader)
            book_list = []
            to_int = lambda s: int(s) if s else None
            for row in csv_reader:
                row[-2], row[-3] = to_int(row[-2]), to_int(row[-3])  # год издания и кол-во страниц
                name, author = row[:2]
                part = Partition(self.start_copies)
                if row[-3] >= 2022:
                    part.book = Book(name, author, row[2:], margin_new, rating)
                else:
                    part.book = Book(name, author, row[2:], margin, rating)
                book_list.append(part)
        return book_list

    # Поиск книги в магазине
    def search_book(self, partition: Partition) -> Partition:
        find_book = None
        if partition.book.name is None:
            ind = self.find_the_last(partition.book.author)
        else:
            ind = 0
            for j in self.book_list:
                if j.book.name == partition.book.name:
                    break
                else:
                    ind += 1
        find_book = self.book_list[ind]

        return find_book

    # Нахлждение последней книги автора
    def find_the_last(self, author: str) -> int:
        last_year, last_book = 0, None
        for i, part in enumerate(self.book_list):
            if part.book.author == author and part.book.year > last_year:
                last_year = part.book.year
                last_book = i
        return last_book

    # Вычитание кол-ва книг из магазина
    def remove(self, part: Partition, copies: int):
        need_copies = 0
        part.cnt_copy -= copies
        if part.cnt_copy < 0:
            need_copies = abs(part.cnt_copy)
            part.cnt_copy = 0
        return need_copies

    # Проверка на мин. кол-во копий каждой книги в магазине
    def check_min_copies(self) -> List[Tuple[Partition, int]]:
        refill = []
        for part in self.book_list:
            if part.cnt_copy < self.min_copies:
                refill.append((part, self.min_copies - part.cnt_copy))
        return refill

    # Добавление книги в магазин
    def add(self, books: List[Partition]):
        for part in books:
            ind = 0
            for j in self.book_list:
                if j.book.name == part.book.name:
                    self.book_list[ind].cnt_copy += part.cnt_copy
                    part.cnt_copy = 0
                    break
                else:
                    ind += 1

    # Попытка выполнить заказ
    def try_to_execute_orders(self, day: int) -> List[PublishingOrder]:
        applic_before = len(self.applications)

        for order in filter(lambda o: not o.status.is_done(), self.orders):
            need_order_copies, was_need_copies = 0, 0
            for part in filter(lambda b: b.cnt_copy != 0, order.book_list):
                find_book = self.search_book(part)
                need_copies = self.remove(find_book, part.cnt_copy)

                if need_copies > 0:
                    self.add_application(find_book, need_copies, day)

                self.add_sold(find_book, part.cnt_copy - need_copies)

                need_order_copies += need_copies
                was_need_copies += part.cnt_copy

                part.cnt_copy = need_copies

            if need_order_copies == was_need_copies:
                continue
            if order.status.is_recv() and need_order_copies > 0:
                order.status = next(order.status)
            elif need_order_copies == 0:
                order.status = next(next(order.status))

            order.books_num = order.get_books_num()

        for part, copies in self.check_min_copies():
            self.add_application(part, copies, day)

        sum_sold = sum(map(lambda b: b.cnt_copy, self.sold))
        for part in self.sold:
            part.book.recalc_rating(part.cnt_copy, sum_sold)

        for part in self.book_list:
            part.book.recalc_price(day)

        return self.applications[applic_before:]

    # Добавление заявки в издательство
    def add_application(self, part: Partition, copies: int, day: int):
        need_book = Partition(copies)
        need_book.book = Book(name=part.book.name, author=part.book.author)
        application = PublishingOrder(day, part.book.publishing, [need_book])
        if application in self.applications:
            ind = self.applications.index(application)
            application = self.applications[ind]
            if part in application.book_list:
                ind = application.book_list.index(part)
                need_book = application.book_list[ind]
                need_book.cnt_copy += copies
            else:
                application.book_list.append(need_book)
        else:
            self.applications.append(application)

        application.books_num += copies

    # Добавление книги в список проданных
    def add_sold(self, part: Partition, copies_num: int):
        ind = 0
        for j in self.sold:
            if j.book.name == part.book.name:
                self.sold[ind].cnt_copy += copies_num
                self.income += part.book.price * copies_num
                break
            else:
                ind += 1
        # ind = self.sold.index(part)

    # Пополнение магазина из книг издательства
    def get_arrived_books_from_publishing(self):
        for application in filter(lambda a: a.books_num != 0, self.applications):
            if application.status.is_done():
                self.add(application.book_list)
                application.books_num = 0

