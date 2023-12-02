from collections import UserDict
from datetime import datetime
from pickle import dump, load
import cmd

class Field:
    def __init__(self, value):
        self.__value = None                 
        self.value = value                     

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        self.__value = value
    
    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @property
    def value(self):
        return self.__value
 
    @value.setter
    def value(self, value):
        if value.isnumeric() and len(value) == 10:
            self.__value = value
        else:
            raise ValueError('Phone is not valid')
        
class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, '%Y.%m.%d')
        except ValueError:
            raise ValueError('Birthday is not valid')

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))
        
    def add_birthday(self, birthday):
        valid_birthday = Birthday(birthday)
        if not valid_birthday is None:
            self.birthday = birthday
        else:
            return 'Birthday is not valid'
        
    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)

    def edit_phone(self, old_phone_number, new_phone_number):
        phone = self.find_phone(old_phone_number)
        if phone:
            phone.value = new_phone_number
        else:
            raise ValueError('Phone not found')

    def find_phone(self, phone):
        valid_number = Phone(phone)
        for ph in self.phones:
            if ph.value == valid_number.value:
                return ph
            
    def days_to_birthday(self):
        new_day = '2023' + self.birthday[4:]
        birth_day = datetime.strptime(new_day, '%Y.%m.%d')
        if datetime.strptime(new_day, '%Y.%m.%d') < datetime.now():
            new_day = '2024' + self.birthday[4:]
            birth_day = datetime.strptime(new_day, '%Y.%m.%d')
        return f'Birthday will be in {(birth_day - datetime.now()).days + 1} days'



    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        if isinstance(record, Record):
            self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    def find_all(self, info):
        res = None
        res = []
        for record in self.data.values():
            if info.lower() in record.name.value.lower() or bool(list(filter(lambda phone: info in phone.value, record.phones))):
                print(record)
                res.append(record)
        return res
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            print(f"Not found")

    def dump(self, filename='save.bin'):
        with open(filename, 'wb') as fh:
            dump(self.data, fh)

    def load(self, filename='save.bin'):
        book = AddressBook()       
        try:
            with open(filename, 'rb') as fh:
                self.data = load(fh)
        except FileNotFoundError:
            book = AddressBook()
        

    def iterator(self, count_res):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += F'{item}: {record}'
            counter += 1
            if counter >= count_res:
                yield result
                counter = 0
                result = ''

class Controller(cmd.Cmd):
    def exit(self):
        self.book.dump()
        return True

def main():
    book = AddressBook()
    book.load()

if __name__ == '__main__':
    main()

   # Створення нової адресної книги
book = AddressBook()

    # Створення запису для John
john_record = Record("John", '1991.2.2')
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
book.add_record(john_record)

    # Створення та додавання нового запису для Jan
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

    # Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

    # Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555


for name, record in book.data.items():
    print(next(book.iterator(1)))

john_record.add_birthday('1991.11.1')


print(john_record.days_to_birthday())



book.dump()

print('----find_all----')
book.find_all('432')
