import json
from time import strftime
import hashlib


class File:
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        with open(self.filename, 'r') as file:
            try:
                list_ = json.load(file)
            except:
                list_ = []
        return list_

    def write(self, data) -> None:
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=3)


class User:
    def __init__(self, fullname=None, username=None, password=None):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.myproduct = []

    def save_user(self):
        obj = File('user.json')
        list_ = obj.read()
        list_.append(self.__dict__)
        obj.write(list_)

    def check_username(self):
        obj = File('user.json')
        for i in obj.read():
            if self.username == i['username']:
                return True
        else:
            return False

    def check_login(self):
        obj = File('user.json')
        for i in obj.read():
            if i['username'] == self.username and i['password'] == self.password:
                return True
        else:
            return

    def user_product(self):
        user = File('user.json').read()
        for i in user:
            print(*i['myproduct'], end='')

    def price(self, amount, id):
        a = False
        product = File('product.json').read()
        userss = File('user.json').read()
        my_product = File('my_product.json').read()
        new = {}

        for i in product:
            string = strftime('%Y-%m-%d %H:%M:%S %p')
            if i['id'] == id and i['amount'] >= amount:
                new.update({
                    "name": i['name'],
                    "amount": amount,
                    "id": id,
                    "time": string
                })
                a = True
        if a:
            my_product.append(new)
            File('my_product.json').write(my_product)
            print('Product sotib olindi')
        sum = File('product.json').read()
        for i in sum:
            if i['id'] == id and i['amount'] >= amount:
                i['amount'] -= amount
            elif i['id'] == id and i['amount'] < amount:
                print("We don't have enough product:")
            File('product.json').write(sum)
        for j in userss:
            if j['username'] == username and a:
                j['myproduct'].append(new)
        File('user.json').write(userss)


class Admin:
    def __init__(self, fullname=None, username=None, password=None):
        self.fullname = fullname
        self.username = username
        self.password = password
        self.new_product = []

    def save_user(self):
        obj = File('admin.json')
        list_ = obj.read()
        list_.append(self.__dict__)
        obj.write(list_)

    def check_username(self):
        obj = File('admin.json')
        for i in obj.read():
            if self.username == i['username']:
                return True
        else:
            return False

    def check_login(self):
        obj = File('admin.json')
        for i in obj.read():
            if i['username'] == username and i['password'] == self.password:
                return True
        else:
            return

    def user_product(self):
        user = File('admin.json').read()
        for i in user:
            print(*i['new_product'], end='')

    def add_product(self, name, amount, id):
        new = {}
        a = False
        obj = File('product.json').read()
        if amount <= 0:
            print("Xato")
            return 0
        for i in obj:
            if i['id'] != id:
                new.update({
                    'id': id,
                    'name': name,
                    'amount': amount
                }, )
                a = True
        if a:
            obj.append(new)
            File('product.json').write(obj)
            d = '\t\033[96mPraduct qo''wildi'
            print(d.expandtabs(50))
        data = File('admin.json').read()
        for i in data:
            if username == i['username']:
                i['new_product'].append(new)
        File('admin.json').write(data)


def get_id():
    with open('product.json') as file:
        data = json.load(file)
        count = 1
        for _ in data:
            count += 1
        return count


class Product:
    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount
        self.id = get_id()

    def save_product(self):
        products = File('product.json').read()
        products.append(self.__dict__)
        File('product.json').write(products)

    def take_list(self):
        product = File('product.json').read()
        print(' Praduct information ')
        for i in product:
            print("id  :", i["id"], "  ", "name : ", i["name"], "  ", 'number of products', i["amount"])


while True:



    ch = '\t Restaran Uz'
    print(ch.expandtabs(50))
    text1 = '''    
    \033[96m1) Login 
    2) Register    
    >>>  '''
    check = input(text1)

    if check == '1':
        username = input("\033[98mEnter username  : ")
        password = input("Enter password  : ")
        res = hashlib.sha1(b'password')
        hex = res.hexdigest()
        user = User(username=username, password=hex)
        if user.check_login():
            while True:
                text2 = '''    
                    \033[94m1) Product 
                    2) My product             
                    3) Exit                
                    >>>  '''
                check2 = input(text2)
                if check2 == '1':
                    info = Product()
                    info.take_list()
                    print("_______________Ordering product!_________________")
                    id = int(input("\033[94mProduct id : "))
                    amount = int(input("Product amount : "))

                    if amount > 0 and id > 0:
                        buy = User(username)
                        buy.price(amount, id)
                    else:
                        print("so bo'lasla")

                if check2 == '2':
                    obj = File('user.json').read()
                    for i in obj:
                        if i['username'] == username:
                            print(i['myproduct'])

                if check2 == '3':
                    print("\033[94mSo bo'lasla")
                    break

        user1 = Admin(username=username, password=hex)
        if user1.check_login():
            while True:
                text = """
                 \033[93m1.Praduct qo'shish
                 2.hisobot
                 3.product view
                 4.the products i put
                 5.Exit
                >>>>"""
                admin = input(text)
                if admin == '1':
                    name = input('\033[93mproduct name : ')
                    amount = int(input('product amount : '))
                    buy = Admin(username)
                    buy.add_product(name, amount, get_id())
                if admin == '2':
                    data = File('user.json').read()
                    for i in data:
                        print(i)
                if admin == '3':
                    info = Product()
                    info.take_list()
                if admin == '4':
                    prduct = File('admin.json').read()
                    for i in prduct:
                        if i['username'] == username:
                            print(i['new_product'])
                if admin == '5':
                    print("\033[93mso bo'lasla")
                    break
    elif check == '2':
        name = input("\033[93mEnter fullname : ")
        username = input("Enter username : ")
        password = input("Enter password : ")
        res = hashlib.sha1(b'password')
        hex = res.hexdigest()
        chk = '''MIjozmisiz 1/0 : '''
        chk1 = input(chk)
        if chk1 == '1':
            reg = User(name, username, hex)
            reg1 = Admin(name, username, hex)
            if not reg.check_username() and not reg1.check_username():
                reg.save_user()
                print("\033[91mSuccessful entry!")
            else:
                print("\033[91mBunday username mavjud")
        elif chk1 == '0':
            re = User(name, username, hex)
            re1 = Admin(name, username, hex)
            if not re1.check_username() and not re.check_username():
                re1.save_user()
                print("\033[91mSuccessful entry!")
            else:
                print("\033[91mBunday username mavjud")
