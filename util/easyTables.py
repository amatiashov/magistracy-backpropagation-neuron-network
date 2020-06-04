# coding: UTF-8;
from sys import stdout


class EasyTables(object):
    def __init__(self, titles=[], header= True, rows_count= 0):
        if not header:
            self.rows_count = rows_count
        else:
            self.rows_count = 0
        self.max_leng_in_row = []
        self.title_of_rows = []
        self.data_in_rows = []
        self.head = header
        if titles and header:
            self.add_title(titles)
        if not header:
            self.max_leng_in_row.extend([0] * rows_count)

    def add_title(self, titles):
        for word in titles:
            word = str(word).rstrip().lstrip()
            self.title_of_rows.append(word)
            self.rows_count += 1
            self.max_leng_in_row.append(len(word))

    def add_row(self, value):
        if self.rows_count < 1 and self.head:
            print ('Firs, add headers!')
        else:
            if len(value) != self.rows_count:
                print ('Wrong number of columns!')
                print ('requires: ', self.rows_count)
                print ('received: ', len(value))
            else:
                self.data_in_rows.append([])
                for i in range(len(value)):
                    data = str(value[i])
                    if len(data) > self.max_leng_in_row[i]:
                        self.max_leng_in_row[i] = len(data)
                    self.data_in_rows[-1].append(data)

    def print_title(self):
        for i in range(len(self.title_of_rows)):
            stdout.write('+' + '-' * (self.max_leng_in_row[i] + 2))
        stdout.write('+\n')

        for i in range(len(self.title_of_rows)):
            stdout.write('| ' + self.title_of_rows[i] + ' ' * (self.max_leng_in_row[i] - len(self.title_of_rows[i]) + 1))
        stdout.write('|\n')

        for i in range(len(self.title_of_rows)):
            stdout.write('+' + '-' * (self.max_leng_in_row[i] + 2))
        stdout.write('+\n')

    def get_column(self, column_name):
        column = []
        index_column_in_table = self.title_of_rows.index(column_name)
        for word in self.data_in_rows:
            column.append(word[index_column_in_table])
        return column

    def print_data(self):
        if not self.head:
            for i in range(self.rows_count):
                stdout.write('+' + '-' * (self.max_leng_in_row[i] + 2))
            stdout.write('+\n')

        for string in self.data_in_rows:
            for i in range(len(string)):
                stdout.write('| ' + string[i] + ' ' * (self.max_leng_in_row[i] - len(string[i]) + 1))
            stdout.write('|\n')

        for i in range(self.rows_count):
            stdout.write('+' + '-' * (self.max_leng_in_row[i] + 2))
        stdout.write('+\n')

    def display(self):
        if self.rows_count > 0:
            if self.head:
                self.print_title()
                self.print_data()
            else:
                self.print_data()