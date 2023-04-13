import model


if __name__ == '__main__':
    # parameters = model.get_start_parameters()
    parameters = [10, 1, 3, 'books.csv']
    if parameters:
        bookshop = model.System(*parameters)
        bookshop.start_system()