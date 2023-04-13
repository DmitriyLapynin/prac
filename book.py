from enum import Enum



class CategoryLabel(Enum):
    UNKN = 'Неизвестно'
    DETE = 'Детектив'
    FANT = 'Фэнтези'
    ADV = 'Приключения'
    FORC = 'Для детей'
    PROZ = 'Проза'
    ROMA = 'Роман'
    PICT = 'Живопись'

    @classmethod
    def _missing_(cls, value):
        return CategoryLabel.UNKN

class Partition():

    def __init__(self, cnt_copy):
        self.book = Book() # книга
        self.cnt_copy = cnt_copy # кол-во


class Book():
    '''def __init__(self, name, author, publishing, year, pages_num, theme, category, margin, rating):
        self.name : str
        self.author : str
        self.publishing : str
        self.year : int
        self.pages_num : int
        self.theme : str
        self.category : str

        self.margin : int
        self.start_rating : int
        self.rating : int

        self.price : int

    # ежеденвный перерасчёт цены
    def recalс_price(self):
        pass

    # ежеденвный перерасчёт рейтинга
    def recalculate_rating(self, orders_num, all_orders):
        pass'''

    def __init__(self, name=None, author=None, book_args=[None] * 4, margin=None, start_rating=None):
        self.name, self.author = name, author
        self.publishing, self.year, self.pages_num, self.category = book_args
        self.category = CategoryLabel(self.category)

        self.margin, self.start_rating = margin, start_rating
        self.rating = self.start_rating

        if not self.pages_num: self.pages_num = 100
        if not self.margin: self.margin = 0
        self.price = int(self.pages_num * (1 + self.margin / 100))

    def get_args(self):
        return self.name, self.author, self.publishing, self.year, \
               self.pages_num, self.category.value, self.price

    def get_name(self):
        if self.name and self.author:
            *author1, author2 = self.author.split()
            author = author1[0][0] + '.' + author2
            return ", ".join([author, self.name])
        elif self.name:
            return self.name
        elif self.author:
            return self.author
        else:
            return 111

    def recalc_price(self, day_num):
        ''' Функция перерасчет цены с учетом измененной наценки на данный день эксперимента '''
        if (2022 - self.year) < day_num and self.margin != 0:
            self.margin -= 1
            self.price = int(self.pages_num * (1 + self.margin / 100))

    def recalc_rating(self, orders_num, all_orders):  # пересчет рейтинга книги
        ''' Функция пересчет рейтинга книги в зависимости от кол-ва её заказов '''
        self.rating = orders_num / all_orders * 10
        self.rating += self.start_rating
        self.rating = round(self.rating, 2)
        if self.rating > 10: self.rating = 10
