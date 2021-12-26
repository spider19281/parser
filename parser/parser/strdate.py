from datetime import date

class CustomDate():

    month_list = [
        'января', 'февралья', 'марта', 'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
    ]

    def __new__(self, str_date):
        if ('Сегодня' in str_date):        
            self.year = date.today().year
            self.month = date.today().month
            self.day = date.today().day
        else:
            split_str = str_date.split(' ')
            self.year = date.today().year
            self.month = CustomDate.month_list.index(split_str[1].lower()) + 1
            self.day = int(split_str[0])
        return date(self.year, self.month, self.day)
