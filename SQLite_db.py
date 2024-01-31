import sqlite3 as sq


async def AI_Active():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT value FROM gpt WHERE parameter = "Active_GPT"')
    row = cur.fetchone()[0]

    db.commit()
    db.close()
    return row


# добавление нового пользователя
async def Add_user(int, str):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'INSERT INTO users (id, username) VALUES ({int}, "{str}")')
    db.commit()
    db.close()
    return True


async def Add_promo(count, name):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'INSERT INTO promo (name, count) VALUES ("{name}", {count})')
    db.commit()
    db.close()
    return True


# вывести кол-во юзеров админов и суперадминов
async def Count_All_User():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT COUNT(*) FROM users WHERE role = "user"')
    row = cur.fetchone()[0]

    cur.execute(f'SELECT COUNT(*) FROM users WHERE role = "Admin"')
    row2 = cur.fetchone()[0]

    cur.execute(f'SELECT COUNT(*) FROM users WHERE role = "SuperAdmin"')
    row3 = cur.fetchone()[0]

    db.commit()
    db.close()
    return row, row2, row3


# обновление данных username пользователя
async def Write_username(str, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE users SET (username) = ("{str}") WHERE id = {id}')
    db.commit()
    db.close()
    return True


# поиск пользователя по id
async def db_read_id(id, int2):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM users WHERE id = ({id})')

    count = cur.fetchall()
    return count[0][int2]


# поиск активных промокодов
async def db_read_activ_promo():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM promo WHERE count > 0')

    count = cur.fetchall()
    return count


# вывести ВСЕ промокоды
async def db_read_all_promo():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM promo')

    count = cur.fetchall()
    return count


# поиск промокода по значению
async def db_read_promo(str, int2):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM promo WHERE name = ("{str}")')

    count = cur.fetchall()
    return count[0][int2]


# поиск пользователя по username
async def db_read_username(str):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM users WHERE username = ("{str}")')

    count = cur.fetchall()
    return count


# получение всех id пользователей
async def db_read_all_id():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('SELECT id FROM users')
    all = cur.fetchall()
    return all


# поиск продукта по id
async def db_read_id_product(int, int2):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'SELECT * FROM product WHERE id = ({int})')

    count = cur.fetchall()
    return count[0][int2]


async def db_read_admin():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'SELECT * FROM users WHERE role = "Admin" OR role = "SuperAdmin"')

    count = cur.fetchall()
    return count


# чтение всех товаров для каталога (без товаров с кол-вом < 0)
async def db_read_product():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    # ищу все разные варианты категорий товаров
    cur.execute(f'SELECT DISTINCT category FROM product')
    count_category = [count_category[0] for count_category in cur.fetchall()]
    count = []
    count2 = []
    for cate in count_category:
        count2.append(cate)
        cur.execute(
            f'SELECT * FROM product WHERE category = "{cate}" AND count > 0')
        count2.append(cur.fetchall())
        count.append(count2)
    count = count[0]
    messages = []
    i = 1
    while len(count) > i:
        messages.append(f"\n<b>{count[i-1]}</b>\n".upper())
        for product in count[i]:
            messages.append(
                str(f"{product[2]}   <i><u>Цена: {product[4]}</u></i> ₽".capitalize()))
        i += 2
    string = "\n".join(messages)
    cur.close()
    db.close()
    return string


# выбрать все товары по категории
async def db_read_product_Category(cate):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'SELECT * FROM product WHERE category = "{cate}"')

    count = cur.fetchall()
    messages = []
    i = 0
    for product in list(count):
        messages.append(
            str(f"{product[2]}   <i><u>Цена: {product[4]}</u></i> ₽\nКол-во: {product[5]}\n".capitalize()))
        i += 1

    string = "\n".join(messages)

    cur.close()
    db.close()
    return string


# вывод всех продуктов с полныйми характеристиками *ADMIN*
async def db_read_product_Admin():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    # ищу все разные варианты категорий товаров
    cur.execute(f'SELECT DISTINCT category FROM product')
    count_category = [count_category[0] for count_category in cur.fetchall()]
    count = []
    count2 = []
    for cate in count_category:
        count2.append(cate)
        cur.execute(
            f'SELECT * FROM product WHERE category = "{cate}"')
        count2.append(cur.fetchall())
        count.append(count2)
    count = count[0]
    messages = []
    i = 1
    while len(count) > i:
        messages.append(f"\n<b>{count[i-1]}</b>\n".upper())
        for product in count[i]:
            messages.append(
                str(f"{product[2]}   <i><u>Цена: {product[4]}</u></i> ₽\nКол-во: {product[5]}".capitalize()))
        i += 2
    string = "\n".join(messages)
    cur.close()
    db.close()
    return string


# чтение всех продуктов
async def db_read_delete_product():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    # ищу все разные варианты категорий товаров
    cur.execute(f'SELECT DISTINCT category FROM product')
    count_category = [count_category[0] for count_category in cur.fetchall()]

    count = []
    count2 = []
    for cate in count_category:
        count2.append(cate)
        cur.execute(f'SELECT * FROM product WHERE category = "{cate}"')
        count2.append(cur.fetchall())
        count.append(count2)

    count = count[0]

    messages = []
    i = 1
    while len(count) > i:
        messages.append(f"\n<b>{count[i-1]}</b>\n".upper())
        for product in count[i]:
            messages.append(
                str(f"<b>id: {product[0]}</b>\n{product[2]}  |  <i><u>Цена: {product[4]}</u></i> ₽".capitalize()))

        i += 2
    string = "\n".join(messages)
    cur.close()
    db.close()
    return string


# добавление нового продукта
async def db_add_product(categor, name, descript, count, price):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'INSERT INTO product (category, name, descript, price, count) VALUES ("{categor}", "{name}", "{descript}", {price}, {count})')

    mean = (
        f"✅Товар успешно добавлен!\n\n"
        f"💎Категория: {categor}\n\n"
        f"💥Название: {name}\n\n"
        f"🔑Описание: {descript}\n\n"
        f"💰Цена: {price}\n\n"
        f"Кол-во: {count}"
    )
    db.commit()
    db.close()
    return mean


async def db_write_Admin(count, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE users SET (role) = ("{count}") WHERE id = {id}')

    db.commit()
    db.close()
    return True


# обновление баланса по id
async def db_write_money(int, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE users SET (money) = ({int}) WHERE id = {id}')

    db.commit()
    db.close()
    return True


async def db_write_promo(str, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE users SET (promo) = ("{str}") WHERE id = {id}')

    db.commit()
    db.close()
    return True


# изменить количество промокода
async def db_write_promo_count(int, name):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE promo SET (count) = ({int}) WHERE name = "{name}"')

    db.commit()
    db.close()
    return True


# изменение параметров продукта
async def db_write_product(categor, name, descript, price, count, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(
        f'UPDATE product SET (category, name, descript, price, count) = ("{categor}", "{name}", "{descript}", {price}, {count}) WHERE id = {id}')

    mean = (
        f"✅Товар успешно Изменен!\n\n"
        f"💎Категория: {categor}\n\n"
        f"💥Название: {name}\n\n"
        f"🔑Описание: {descript}\n\n"
        f"💰Цена: {price}"
        f"Кол-во: {count}"
    )
    db.commit()
    db.close()
    return mean


async def db_write_product_category(categor, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'UPDATE product SET category = "{categor}" WHERE id = {id}')

    db.commit()
    db.close()
    return True


async def db_write_product_name(name, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'UPDATE product SET name = "{name}" WHERE id = {id}')

    db.commit()
    db.close()
    return True


async def db_write_product_descript(descript, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'UPDATE product SET descript = "{descript}" WHERE id = {id}')

    db.commit()
    db.close()
    return True


async def db_write_product_price(price, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'UPDATE product SET price = "{price}" WHERE id = {id}')

    db.commit()
    db.close()
    return True


async def db_write_product_count(count, id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute(f'UPDATE product SET count = "{count}" WHERE id = {id}')

    db.commit()
    db.close()
    return True


# поиск всех категорий
async def search_all_category():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    # ищу все разные варианты категорий товаров
    cur.execute(f'SELECT DISTINCT category FROM product')
    count_category = [count_category[0] for count_category in cur.fetchall()]
    return count_category


# удаление пользователя по названию
async def delete_user(id):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('DELETE FROM users WHERE id = ?', (id,))
    db.commit()
    db.close()
    return True


# удаление промокода по названию
async def delete_promo(name):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('DELETE FROM promo WHERE name = ?', (name,))
    db.commit()
    db.close()
    return True


# очистка ВСЕХ промокодов
async def Clear_promo():
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('DELETE FROM promo')
    cur.execute('UPDATE users SET promo = "н е т"')
    db.commit()
    db.close()
    return True


# удаление продукта по id
async def delete_product(int):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('DELETE FROM product WHERE id = ?', (int,))
    db.commit()
    db.close()
    return True


# удаление категории
async def delete_category(str):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('DELETE FROM product WHERE category = ?', (str,))
    db.commit()
    db.close()
    return True


async def UpPrice(PM, count):
    db = sq.connect('TG_db_1.db')
    cur = db.cursor()

    cur.execute('SELECT price FROM product')
    values = cur.fetchall()
    if PM == "+":
        for value in values:
            update = value[0] + count
            if update < 0:
                update = 0
            cur.execute(
                f'UPDATE product SET price = {update} WHERE price = {value[0]}')
    elif PM == "-":
        for value in values:
            update = value[0] - count
            if update < 0:
                update = 0
            cur.execute(
                f'UPDATE product SET price = {update} WHERE price = {value[0]}')
    elif PM == "*":
        for value in values:
            update = int((value[0] / 100 * count) + value[0])
            if update < 0:
                update = 0
            cur.execute(
                f'UPDATE product SET price = {update} WHERE price = {value[0]}')
    elif PM == "/":
        for value in values:
            update = int(value[0] - (value[0] / 100 * count))
            if update < 0:
                update = 0
            cur.execute(
                f'UPDATE product SET price = {update} WHERE price = {value[0]}')

    db.commit()
    db.close()
    return True
