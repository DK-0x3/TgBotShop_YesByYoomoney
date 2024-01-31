import aiogram
from aiogram import types, Dispatcher, executor, Bot
import Config
import SQLite_db
import sqlite3 as sq
from aiogram.dispatcher import filters
import requests
import re
import os
import sqlite3 as sq
from datetime import timedelta, datetime
from aiogram.types import Message

bot = Bot(Config.Settings['TOKEN_BOT'])
dp = Dispatcher(bot)

id_db = 0
role_db = 1
money_db = 2
total_buy_db = 3
AddProduct1 = [0]
DelProduct = [0]
WriteProduct = [0, 0, 0]
SandAll = [0]
CryptoPrice = [0, 0]
SetAdmin = [0]
DelCategory = [0]
Promo = [0]
Setpromo = [0]
DelPromo = [0]
ClearPromo = [0]
SearchUser = [0, 0]
DelUser = [0, 0]
UpPriceAll = [0]
DownPriceAll = [0]
UpPriceAllCent = [0]
DownPriceAllCent = [0]


async def AdminKeyboard():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    buttons = ["Каталог",
               "Профиль", "Купить", "Настройки", "Админ Панель", "Курс Crypto"]
    keyboard.add(*buttons)
    return keyboard


async def Keyboard():
    keyboard = types.ReplyKeyboardMarkup(
        row_width=2, resize_keyboard=True)
    buttons = ["Каталог",
               "Профиль", "Купить", "Настройки"]
    keyboard.add(*buttons)
    return keyboard


async def ListAdmin():
    Count = list(await SQLite_db.db_read_admin())
    CountZ = []
    for adm in Count:
        CountZ.append(adm[0])
        CountZ.append(adm[4])
        CountZ.append(adm[1])
    StrCountZ = ""
    Atr = 0
    while True:
        try:
            if CountZ[Atr+2] == "Admin":
                StrCountZ = StrCountZ + \
                    f"\nid: {CountZ[Atr]} | @{CountZ[Atr+1]}"
            elif CountZ[Atr+2] == "SuperAdmin":
                StrCountZ = StrCountZ + \
                    f"\n<b>id: {CountZ[Atr]} | @{CountZ[Atr+1]}</b> 😎"
            Atr += 3
        except:
            break
    return StrCountZ


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    try:
        if await SQLite_db.Add_user(message.from_id, str(message.from_user['username']).upper()):

            keyboard = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            buttons = ["Каталог",
                       "Профиль", "Купить", "Настройки"]
            keyboard.add(*buttons)
            await message.answer(f"Привет!\nВоспользуйся кнопками ниже для работы", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    except:
        keyboard = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        buttons = ["Каталог",
                   "Профиль", "Купить", "Настройки"]
        keyboard.add(*buttons)
        await message.answer(f"Привет!\nВоспользуйся кнопками ниже для работы", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Regexp(regexp=r"(Меню)"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    await SQLite_db.Write_username(str(message_from.from_user['username']).upper(), int(message_from.from_id))

    if await SQLite_db.db_read_id(message_from.from_id, role_db) == "Admin" or await SQLite_db.db_read_id(message_from.from_id, role_db) == "SuperAdmin":

        await message_from.answer(f"Привет!\nВоспользуйся кнопками ниже для работы", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
    else:
        await message_from.answer(f"Привет!\nВоспользуйся кнопками ниже для работы", reply_markup=await Keyboard(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Regexp(regexp=r"(Каталог)"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)
    try:
        messag = (
            f"{await SQLite_db.db_read_product()}"
        )
        await message_from.answer(f"{messag}", parse_mode=types.ParseMode.HTML)
    except:
        await message_from.answer(f"🥲Нет товаров", parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(text="ReadProduct_All")
async def send_random_value(call: types.CallbackQuery):
    messag = (
        f"{await SQLite_db.db_read_product_Admin()}"
    )
    await call.message.answer(f"{messag}", parse_mode=types.ParseMode.HTML)


@dp.message_handler(filters.Regexp(regexp=r"(Профиль)"))
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)

    buttons = [types.InlineKeyboardButton(
        text="Ввести Промокод", callback_data="InputPromo")]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    messag = (
        "➖➖➖➖ПРОФИЛЬ➖➖➖➖"
        f"\n\n💰Баланс: {await SQLite_db.db_read_id(message_from.from_id, money_db)}"
        f"\n\n🏦Покупок на сумму: {await SQLite_db.db_read_id(message_from.from_id, total_buy_db)}"
        f"\n\nID {await SQLite_db.db_read_id(message_from.from_id, id_db)}\n"
        "➖➖➖➖➖➖➖➖➖➖➖"
    )
    await message_from.answer(messag, reply_markup=keyboard)


@dp.callback_query_handler(text="InputPromo")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Введи Промокод")
    global Promo
    Promo[0] = 1


@dp.message_handler(filters.Regexp(regexp=r"(Админ Панель)"))
async def bot_commands_handler(message_from: types.Message) -> None:
    if await SQLite_db.db_read_id(message_from.from_id, role_db) == "Admin":
        buttons = [types.InlineKeyboardButton(text="Добавить товар", callback_data="AddProduct"), types.InlineKeyboardButton(
            text="Изменить товар", callback_data="WriteProduct"), types.InlineKeyboardButton(
            text="Удалить товар", callback_data="DelProduct"), types.InlineKeyboardButton(
            text="Удалить Категорию", callback_data="DelCategory"), types.InlineKeyboardButton(
            text="Просмотр товаров", callback_data="ReadProduct_All"), types.InlineKeyboardButton(
            text="Управление Промокодами", callback_data="SetPromo"), types.InlineKeyboardButton(
            text="Управление Поль-ми", callback_data="SetUser"), types.InlineKeyboardButton(
            text="Цена Крипты", callback_data="PriceCrypto")]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message_from.answer(f"<b>💎Админ Панель</b>\n\nВремя сервера: {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    if await SQLite_db.db_read_id(message_from.from_id, role_db) == "SuperAdmin":
        buttons = [types.InlineKeyboardButton(text="Добавить товар", callback_data="AddProduct"), types.InlineKeyboardButton(
            text="Изменить товар", callback_data="WriteProduct"), types.InlineKeyboardButton(
            text="Удалить товар", callback_data="DelProduct"), types.InlineKeyboardButton(
            text="Удалить Категорию", callback_data="DelCategory"), types.InlineKeyboardButton(
            text="Просмотр товаров", callback_data="ReadProduct_All"), types.InlineKeyboardButton(
            text="Управление Админ-ми", callback_data="SetAdmin"), types.InlineKeyboardButton(
            text="Управление Промокодами", callback_data="SetPromo"), types.InlineKeyboardButton(
            text="Управление Поль-ми", callback_data="SetUser"), types.InlineKeyboardButton(
            text="Цена Крипты", callback_data="PriceCrypto"), types.InlineKeyboardButton(
            text="Скачать БД", callback_data="Download_db"), types.InlineKeyboardButton(
            text="Сделать рассылку", callback_data="SendingAll")]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message_from.answer(f"<b>😎Супер Админ Панель</b>\n\nВремя сервера: {datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.message_handler(lambda msg: msg.text.lower() == "chat_gpt")
async def bot_commands_handler(message_from: types.Message):

    buttons = [types.InlineKeyboardButton(
        text="Изменить AI", callback_data="WriteAI")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message_from.answer(f"<b>Введи запрос</b>\n\n<u>Используемая AI:</u> {await SQLite_db.AI_Active()}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global gpt
    gpt[0] = 1


@dp.callback_query_handler(text="SetUser")
async def send_random_value(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(
        text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(
        text="Удалить Пользователя", callback_data="DelUser")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    user, admin, superadmin = await SQLite_db.Count_All_User()
    await call.message.edit_text(f"<b>Управление Пользователями</b>\n\n😀Пользователей: {user}\n\n💎Админов: {admin}\n\n😎СуперАдминов: {superadmin}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(text="SetPromo")
async def send_random_value(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(
        text="Активные Промокоды", callback_data="ActivPromo"), types.InlineKeyboardButton(text="Создать Промокод", callback_data="SetNewPromo"), types.InlineKeyboardButton(
        text="Удалить Промокод", callback_data="DelPromo"), types.InlineKeyboardButton(
        text="Очистить Все Промокоды", callback_data="ClearPromo")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text("Управление Промокодами", reply_markup=keyboard)


@dp.callback_query_handler(text="SearchUser")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.answer(f"<b>Поиск пользователя</b>\n\nВведи ID \nили\n @username", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global SearchUser
    SearchUser[0] = 1


@dp.callback_query_handler(text="DelUser")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.answer(f"<b>❌Удаление пользователя(ей)</b>\n\nВведи ID \nили\n @username\n\n*<i>Для удаления сразу нескольких пользователей введи данные через запятую</i>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DelUser
    DelUser[0] = 1


@dp.callback_query_handler(text="ClearPromo")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ("ОЧИСТИТЬ", "Отмена")
    keyboard.add(*buttons)
    message = []
    for prom in list(await SQLite_db.db_read_all_promo()):
        if prom[2] > 0:
            message.append(str(f"<b>{prom[1]}</b>  |  {prom[2]}  🟢\n"))
        elif prom[2] <= 0:
            message.append(str(f"<b>{prom[1]}</b>  |  {prom[2]}  🔴\n"))
    string = "\n".join(message)
    await call.message.answer(f"Все Промокоды:\n\n{string}\n\nТочно Очистить все промокоды?\n\n⚠️<b>Очистятся ВСЕ данные о промокодах и их активациях!</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global ClearPromo
    ClearPromo[0] = 1


@dp.callback_query_handler(text="DelPromo")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ("Отмена")
    keyboard.add(buttons)
    message = []
    for prom in list(await SQLite_db.db_read_all_promo()):
        if prom[2] > 0:
            message.append(str(f"<b>{prom[1]}</b>  |  {prom[2]}  🟢\n"))
        elif prom[2] <= 0:
            message.append(str(f"<b>{prom[1]}</b>  |  {prom[2]}  🔴\n"))
    string = "\n".join(message)
    await call.message.answer(f"Все Промокоды:\n\n{string}\n\n<b><i>Введи промокод который нужно удалить</i></b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DelPromo
    DelPromo[0] = 1


@dp.callback_query_handler(text="ActivPromo")
async def send_random_value(call: types.CallbackQuery):
    message = []
    for prom in list(await SQLite_db.db_read_activ_promo()):
        message.append(str(f"<b>{prom[1]}</b>  |  {prom[2]}\n"))
    string = "\n".join(message)
    if string == "":
        string = "<b>Нет промокодов</b>"
    await call.message.answer(f"<i>Активные Промокоды:</i>\n\n{string}", parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(text="SetNewPromo")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ("Отмена")
    keyboard.add(buttons)
    await call.message.answer("<b>Введи Название промокода</b>\n\n*Введи сначало буквенное значение, затем СЛИТНО введи цифровое значение(например:DLK100)", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global Setpromo
    Setpromo[0] = 1


@dp.callback_query_handler(text="Download_db")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("⏳Загрузка...")
    with open('TG_db_1.db', 'rb') as db_file:
        # Отправляем файл в чат
        await call.message.answer_document(db_file)


@dp.callback_query_handler(text="DelCategory")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await SQLite_db.search_all_category()
    keyboard.add(*buttons)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>Для удаления <i>КАТЕГОРИИ</i> введи её название\n\n*Для удаления сразу нескольких <i>КАТЕГОРИЙ</i> введи их названия через запятую</b>\n\n{await SQLite_db.db_read_delete_product()}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DelCategory
    DelCategory[0] = 1


@dp.callback_query_handler(text="SetAdmin")
async def send_random_value(call: types.CallbackQuery):
    buttons = [types.InlineKeyboardButton(
        text="Назначить/удалить админа", callback_data="SetNewAdmin")]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await call.message.edit_text(f"<b>Админы</b>\n\n{await ListAdmin()}\n\n*😎 СуперАдмин", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(text="SetNewAdmin")
async def send_random_value(call: types.CallbackQuery):
    await call.message.answer("Введи @username пользователя")
    global SetAdmin
    SetAdmin[0] = 1


@dp.message_handler(lambda msg: msg.text.lower() == "назначить/удалить админа")
async def bot_commands_handler(message_from: types.Message) -> None:
    if await SQLite_db.db_read_id(message_from.from_id, role_db) == "SuperAdmin":
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ("Отмена")
        keyboard.add(*buttons)
        await message_from.answer("Введи @username пользователя")
        global SetAdmin
        SetAdmin[0] = 1


@dp.callback_query_handler(text="PriceCrypto")
async def send_random_value(call: types.CallbackQuery):
    global CryptoPrice
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (
        "BTC",
        "TRX",
        "BNB",
        "ETH",
        "LTC",
        "TON",
        "XRP",
        "SOL",
        "MATIC",
        "DOGE",
        "Сигналы",
        "Меню"
    )
    keyboard.add(*buttons)
    await call.message.delete()
    await call.message.answer("Введи или выбери <b>Крипту</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    CryptoPrice[0] = 1


@dp.message_handler(lambda msg: msg.text.lower() == "курс crypto")
async def bot_commands_handler(message_from: types.Message) -> None:
    global CryptoPrice
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (
        "BTC",
        "TRX",
        "BNB",
        "ETH",
        "LTC",
        "TON",
        "XRP",
        "SOL",
        "MATIC",
        "DOGE",
        "Меню"
    )
    keyboard.add(*buttons)
    await message_from.answer("Введи или выбери <b>Крипту</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    CryptoPrice[0] = 1


@dp.callback_query_handler(text="AddProduct")
async def send_random_value(call: types.CallbackQuery):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await SQLite_db.search_all_category()
    keyboard.add(*buttons)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer("Введи или выбери <b>КАТЕГОРИЮ</b> товара", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global AddProduct1
    AddProduct1[0] = 1


@dp.callback_query_handler(text="DelProduct")
async def send_random_value(call: types.CallbackQuery):

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>Для удаления <i>ТОВАРА</i> введи его id\n\n*Для удаления сразу нескольких товаров введи их id через запятую</b>\n\n{await SQLite_db.db_read_delete_product()}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DelProduct
    DelProduct[0] = 1


@dp.callback_query_handler(text="SendingAll")
async def send_random_value(call: types.CallbackQuery):
    if await SQLite_db.db_read_id(call.from_user.id, role_db) == "Admin" or await SQLite_db.db_read_id(call.from_user.id, role_db) == "SuperAdmin":
        await call.message.answer('Введи текст рассылки\n\n*Для форматирования используй следующие HTML теги:\n\n<b>жирный</b>\n<i>курсив</i>\n<u>подчеркнутый</u>\n<s>зачеркнутый</s>\n<tg-spoiler>скрытый текст, на который надо нажать, чтобы он отобразился</tg-spoiler>\n<a href="ссылка">ссылка в тексте</a>\n<a href="tg://user?id=1040628188">Упоминание пользователя с id 1040628188</a>\n<code>блок кода</code>')
        global SandAll
        SandAll[0] = 1


@dp.callback_query_handler(text="WriteProduct")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Массовое изменение цен", "Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>Для <i>ИЗМЕНЕНИЯ</i> товара введи его id\n\n*Для удаления сразу нескольких товаров введи их id через запятую</b>\n\n{await SQLite_db.db_read_delete_product()}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global WriteProduct
    WriteProduct[0] = 1


@dp.callback_query_handler(text="UpPriceAll")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>На сколько Увеличить цены <u>ВСЕХ</u> товаров?\n\n</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global UpPriceAll
    UpPriceAll[0] = 1


@dp.callback_query_handler(text="UpPriceAllCent")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>На сколько % ПРОЦЕНТОВ % увеличить цены <u>ВСЕХ</u> товаров?\n\n</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global UpPriceAllCent
    UpPriceAllCent[0] = 1


@dp.callback_query_handler(text="DownPriceAll")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>На сколько Снизить цены <u>ВСЕХ</u> товаров?\n\n</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DownPriceAll
    DownPriceAll[0] = 1


@dp.callback_query_handler(text="DownPriceAllCent")
async def send_random_value(call: types.CallbackQuery):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Отмена")
    await call.message.delete()
    await call.message.answer(f"<b>На сколько % ПРОЦЕНТОВ % Снизить цены <u>ВСЕХ</u> товаров?\n\n</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    global DownPriceAllCent
    DownPriceAllCent[0] = 1


@dp.message_handler(content_types="text")
async def bot_commands_handler(message_from: types.Message) -> None:
    user_id: str = str(message_from.from_id)

    global AddProduct1, DelProduct, WriteProduct, SandAll, CryptoPrice, SetAdmin, DelCategory, Promo, Setpromo, DelPromo, ClearPromo, SearchUser, DelUser, UpPriceAll, DownPriceAll, UpPriceAllCent, DownPriceAllCent

    if AddProduct1[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            AddProduct1 = [0]
        else:
            AddProduct1.append(message_from.text)
            await message_from.answer("Введи <b>НАЗВАНИЕ</b> товара", parse_mode=types.ParseMode.HTML)
            AddProduct1[0] = 2
    elif AddProduct1[0] == 2:
        AddProduct1.append(message_from.text)
        await message_from.answer("Введи <b>ОПИСАНИЕ</b> товара", parse_mode=types.ParseMode.HTML)
        AddProduct1[0] = 3
    elif AddProduct1[0] == 3:
        AddProduct1.append(message_from.text)
        await message_from.answer("Введи <b>ЦЕНУ</b> товара", parse_mode=types.ParseMode.HTML)
        AddProduct1[0] = 4
    elif AddProduct1[0] == 4:
        try:
            AddProduct1.append(int(message_from.text))
            await message_from.answer("Введи <b>КОЛИЧЕСТВО</b> товара", parse_mode=types.ParseMode.HTML)
            AddProduct1[0] = 5
        except:
            await message_from.answer("🛑Ошибка введено не число!\n\nВведи ЧИСЛО еще раз")
            AddProduct1[0] = 4
    elif AddProduct1[0] == 5:
        try:
            await message_from.answer(await SQLite_db.db_add_product(AddProduct1[1], AddProduct1[2], AddProduct1[3], int(message_from.text), AddProduct1[4]), reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            AddProduct1 = [0]
        except:
            await message_from.answer("🛑Ошибка введено не число!\n\nВведи ЧИСЛО еще раз")
            AddProduct1[0] = 5

    if DelProduct[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelProduct = [0]
        else:
            try:
                a = int(message_from.text)
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["Да", "Нет"]
                keyboard.add(*buttons)
                await message_from.answer(f"<b>Точно удалить этот товар?</b>\n\nid:<b>{await SQLite_db.db_read_id_product(int(message_from.text),0)}</b>\n\nКатегория:<b>{await SQLite_db.db_read_id_product(int(message_from.text),1)}</b>\n\nНазвание:<b>{await SQLite_db.db_read_id_product(int(message_from.text),2)}</b>\n\nОписание:<i>{await SQLite_db.db_read_id_product(int(message_from.text),3)}</i>\n\nЦена:<u>{await SQLite_db.db_read_id_product(int(message_from.text),4)}</u>\n\n", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                DelProduct[0] = 2
                DelProduct.append(int(message_from.text))
            except:
                try:
                    ListId = [int(x.strip())
                              for x in message_from.text.split(",")]
                    keyboard = types.ReplyKeyboardMarkup(
                        row_width=2, resize_keyboard=True)
                    buttons = ["Да", "Нет"]
                    keyboard.add(*buttons)
                    for id in ListId:
                        await message_from.answer(f"<b>Точно удалить этот товар?<b>\n\nid:<b>{await SQLite_db.db_read_id_product(int(id),0)}</b>\n\nКатегория:<b>{await SQLite_db.db_read_id_product(int(id),1)}</b>\n\nНазвание:<b>{await SQLite_db.db_read_id_product(int(id),2)}</b>\n\nОписание:<i>{await SQLite_db.db_read_id_product(int(id),3)}</i>\n\nЦена:<u>{await SQLite_db.db_read_id_product(int(id),4)}</u>\n\n", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    DelProduct[0] = 3
                    DelProduct.append(ListId)
                except:
                    await message_from.answer(f"<b>🛑Ошибка<b>, введен не список чисел или не число, введи СПИСОК ЧИСЕЛ через запятую ИЛИ ЧИСЛО еще раз\n\n*или таких id нет", parse_mode=types.ParseMode.HTML)
    elif DelProduct[0] == 2:
        if message_from.text == "Да":
            try:
                await SQLite_db.delete_product(DelProduct[1])
                await message_from.answer("🗑️Товар успешно удален!", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
                DelProduct = [0]
            except:
                await message_from.answer("🛑Ошибка\n\nВведено не число, или нет такого товара id")
        else:
            await message_from.answer("❌Удаление <b>ОТМЕНЕНО</b>", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelProduct = [0]
    elif DelProduct[0] == 3:
        if message_from.text == "Да":
            for id in DelProduct[1]:
                await SQLite_db.delete_product(id)
            await message_from.answer("🗑️Товар успешно удален!", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelProduct = [0]
        else:
            await message_from.answer("❌Удаление <b>ОТМЕНЕНО</b>", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelProduct = [0]

    if WriteProduct[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            WriteProduct = [0]
        elif message_from.text == "Массовое изменение цен":
            buttons = [types.InlineKeyboardButton(
                text="Поднять цены", callback_data="UpPriceAll"), types.InlineKeyboardButton(
                text="Снизить цены", callback_data="DownPriceAll"), types.InlineKeyboardButton(
                text="Поднять цены на %", callback_data="UpPriceAllCent"), types.InlineKeyboardButton(
                text="Снизить цены на %", callback_data="DownPriceAllCent")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            WriteProduct = [0]
            await message_from.answer("<b>Изменение цены ВСЕХ товаров</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            try:
                a = int(message_from.text)
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["Да", "Нет"]
                keyboard.add(*buttons)
                await message_from.answer(f"<b>Точно ИЗМЕНИТЬ этот товар?</b>\n\nid: <b>{await SQLite_db.db_read_id_product(int(message_from.text),0)}</b>\n\nКатегория: <b>{await SQLite_db.db_read_id_product(int(message_from.text),1)}</b>\n\nНазвание: <b>{await SQLite_db.db_read_id_product(int(message_from.text),2)}</b>\n\nОписание: <i>{await SQLite_db.db_read_id_product(int(message_from.text),3)}</i>\n\nЦена: <u>{await SQLite_db.db_read_id_product(int(message_from.text),4)}</u>\n\nКол-во: <u>{await SQLite_db.db_read_id_product(int(message_from.text),5)}</u>\n\n", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                WriteProduct[0] = 2
                WriteProduct[1] = int(message_from.text)
            except:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["Отмена"]
                keyboard.add(*buttons)
                await message_from.answer("🛑<b>Ошибка введено не число!</b>\n\nВведите ЧИСЛО еще раз или отмените операцию", reply_markup=keyboard)
                WriteProduct[0] = 1
    elif WriteProduct[0] == 2:
        if message_from.text == "Да":
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            buttons = ["Категорию", "Название",
                       "Описание", "Цену", "Количество"]
            keyboard.add(*buttons)
            await message_from.answer("Какие параметры ИЗМЕНИТЬ у товара?", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

            WriteProduct[0] = 3
        else:
            await message_from.answer("❌ИЗМЕНЕНИЕ <b>ОТМЕНЕНО</b>", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            WriteProduct = [0]
    elif WriteProduct[0] == 3:
        if message_from.text == "Категорию":
            await message_from.answer("Введи новую <b>Категорию</b> товара", parse_mode=types.ParseMode.HTML)
            WriteProduct[2] = 1
            WriteProduct[0] = 4
        elif message_from.text == "Название":
            await message_from.answer("Введи новое <b>Название</b> товара", parse_mode=types.ParseMode.HTML)
            WriteProduct[2] = 2
            WriteProduct[0] = 4
        elif message_from.text == "Описание":
            await message_from.answer("Введи новое <b>Описание</b> товара", parse_mode=types.ParseMode.HTML)
            WriteProduct[2] = 3
            WriteProduct[0] = 4
        elif message_from.text == "Цену":
            await message_from.answer("Введи новую <b>Цену</b> товара", parse_mode=types.ParseMode.HTML)
            WriteProduct[2] = 4
            WriteProduct[0] = 4
        elif message_from.text == "Количество":
            await message_from.answer("Введи новое <b>Количество</b> товара", parse_mode=types.ParseMode.HTML)
            WriteProduct[2] = 5
            WriteProduct[0] = 4
        elif message_from.text == "Меню":
            await message_from.answer("Главное меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            WriteProduct = [0, 0, 0]
    elif WriteProduct[0] == 4:
        keyboard = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        buttons = ["Категорию", "Название",
                   "Описание", "Цену", "Количество", "Меню"]
        keyboard.add(*buttons)
        try:
            if WriteProduct[2] == 1:
                await SQLite_db.db_write_product_category(message_from.text, WriteProduct[1])
            elif WriteProduct[2] == 2:
                await SQLite_db.db_write_product_name(message_from.text, WriteProduct[1])
            elif WriteProduct[2] == 3:
                await SQLite_db.db_write_product_descript(message_from.text, WriteProduct[1])
            elif WriteProduct[2] == 4:
                await SQLite_db.db_write_product_price(message_from.text, WriteProduct[1])
            elif WriteProduct[2] == 5:
                await SQLite_db.db_write_product_count(message_from.text, WriteProduct[1])

            await message_from.answer(f"<b>Товар успешно изменен!</b>\n\nid: <b>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),0)}</b>\n\nКатегория: <b>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),1)}</b>\n\nНазвание: <b>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),2)}</b>\n\nОписание: <i>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),3)}</i>\n\nЦена: <u>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),4)}</u>\n\nКол-во: <u>{await SQLite_db.db_read_id_product(int(WriteProduct[1]),5)}</u>\n\n", parse_mode=types.ParseMode.HTML)
            await message_from.answer("Изменить что-то еще в этом товаре?", reply_markup=keyboard)
            WriteProduct[0] = 3
        except:
            await message_from.answer("🛑Ошибка\n\nВведено не число(а)")

    if SandAll[0] == 1:
        keyboard = types.ReplyKeyboardMarkup(
            row_width=2, resize_keyboard=True)
        buttons = ["Разослать", "Отмена"]
        keyboard.add(*buttons)
        await message_from.answer(f"<b>Будет произведена рассылка следующего сообщения:</b>\n\n{message_from.text}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        SandAll.append(message_from.text)
        SandAll[0] = 2
    elif SandAll[0] == 2:
        if message_from.text == "Отмена":
            await message_from.answer("Рассылка отменена", reply_markup=await AdminKeyboard())
            SandAll = [0]
        else:

            NotUsers = []
            users = await SQLite_db.db_read_all_id()
            for row in users:
                try:
                    await bot.send_message(row[0], SandAll[1], parse_mode=types.ParseMode.HTML)
                except:
                    NotUsers.append(row[0])
            string = "\n".join(NotUsers)
            if string == "":
                string = "нет таких пользователей"
            await message_from.answer(f"✅<b>Рассылка завершена!</b>\n\nНе удалось отправить сообщения:\n<i>{string}</i>", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            SandAll = [0]

    if CryptoPrice[0] == 1:
        if message_from.text == "Сигналы":
            pass
        else:
            # Парсер цены доллара
            async def get_currency_price(currency):
                url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req="
                response = requests.get(url)
                if response.status_code == 200:
                    pattern = fr"<CharCode>{currency}</CharCode>.+?<Value>(.*?)</Value>"
                    result = re.search(pattern, response.text, re.DOTALL)
                    if result:
                        return result.group(1).replace(",", ".")
                    else:
                        return "Цена не найдена"
                else:
                    return "🛑Ошибка при получении данных"

            if CryptoPrice[1] == 0:
                url = f'https://api.bybit.com/v2/public/symbols'

                try:
                    # Отправляем GET-запрос к API ByBit
                    response = requests.get(url)
                    data = response.json()
                    pairs = [pair['name'] for pair in data['result']]
                    # pairs_text = '\n'.join(pairs)

                    pairs2 = list(
                        filter(lambda x: message_from.text.upper() in x, pairs))

                    countis = 0
                    keyboard = types.ReplyKeyboardMarkup(
                        row_width=2, resize_keyboard=True)
                    buttons = ["Да", "Отмена"]
                    keyboard.add(*buttons)

                    for item in pairs2:
                        url = f'https://api.bybit.com/v2/public/tickers?symbol={item}'
                        try:
                            response = requests.get(url)
                            data = response.json()
                            # выбор из словаря данных, сначало обращение к ключу в котором список в котором словарь
                            price = data['result'][0]['last_price']
                            cent = data['result'][0]['price_24h_pcnt']
                            if cent[0] == "-":
                                cent2 = str(round(float(cent)*100, 2)
                                            ).replace('-', '🟥 ')
                            elif cent[0] != "-":
                                cent2 = "🟢 " + str(round(float(cent)*100, 2))
                            await message_from.answer(f"Цена {str(item).replace('USDT', '')}: <b>{format(float(price), ',.3f')} $</b>  =>  <i>{format(round(float(await get_currency_price('USD'))*float(price), 2), ',.2f')} ₽</i>\n<u>{cent2} %</u>", parse_mode=types.ParseMode.HTML)
                            countis += 1
                            pairs2.pop(0)
                            if countis >= 10:
                                await message_from.answer(f"Продолжить вывод данных?\n*Их еще много", reply_markup=keyboard)
                                CryptoPrice[1] = 1
                                CryptoPrice.append(pairs2)
                                break
                        except Exception as e:
                            await message_from.reply(f'Произошла 🛑Ошибка: {e}')

                except Exception as e:
                    await message_from.reply(f"🛑Ошибка, Введи поиск еще раз\n\n{e}")

            elif CryptoPrice[1] == 1:
                if message_from.text == "Отмена":
                    CryptoPrice = [0, 0]
                    await message_from.answer(f"Отменено", reply_markup=await AdminKeyboard())
                else:
                    for item in CryptoPrice[2]:
                        url = f'https://api.bybit.com/v2/public/tickers?symbol={item}'
                        try:
                            response = requests.get(url)
                            data = response.json()
                            price = data['result'][0]['last_price']
                            await message_from.answer(f"Цена {str(item).replace('USDT', '').replace('USD', '')}: <b>{format(float(price), ',.2f')} $</b>  =>  <i>{format(round(float(await get_currency_price('USD'))*float(price), 2), ',.2f')} ₽</i>", parse_mode=types.ParseMode.HTML)
                            if CryptoPrice == [0, 0]:
                                break
                        except Exception as e:
                            await message_from.reply(f'Произошла 🛑Ошибка: {e}')
                    else:
                        keyboard = types.ReplyKeyboardMarkup(
                            resize_keyboard=True)
                        buttons = (
                            "BTC",
                            "TRX",
                            "BNB",
                            "ETH",
                            "LTC",
                            "TON",
                            "XRP",
                            "SOL",
                            "MATIC",
                            "DOGE",
                            "Меню"
                        )
                        keyboard.add(*buttons)
                        await message_from.answer("Введи или выбери <b>Крипту</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

    if SetAdmin[0] == 1:
        if message_from.text == "Отмена":
            SetAdmin = [0]
            await message_from.answer(f"Отменено", reply_markup=await AdminKeyboard())
        else:
            try:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = []
                if list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1] == "user":
                    buttons = ["Назначить Админом", "Назначить Супер Админом"]
                elif list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1] == "Admin":
                    buttons = ["Понизить до Пользователя",
                               "Назначить Супер Админом"]
                elif list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1] == "SuperAdmin":
                    buttons = ["Понизить до Пользователя",
                               "Понизить до Админа"]
                buttons.append("Отмена")
                keyboard.add(*buttons)
                await message_from.answer(f"id: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1]}]\n\nНик @{list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][4]}", reply_markup=keyboard)
                SetAdmin.append(
                    list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][0])
                SetAdmin[0] = 2
            except Exception as e:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["Отмена"]
                keyboard.add(*buttons)
                await message_from.answer(f"<b>Пользователь с таким ником не найден</b>, попробуй ввести ник еще раз\n\n*{e}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
    elif SetAdmin[0] == 2:
        if message_from.text == "Отмена":
            SetAdmin = [0]
            await message_from.answer(f"Отменено", reply_markup=await AdminKeyboard())
        elif message_from.text == "Назначить Админом" or message_from.text == "Понизить до Админа":
            if message_from.text == "Назначить Админом":
                await bot.send_message(SetAdmin[1], "💎Вы назначены <b>Админом</b>", parse_mode=types.ParseMode.HTML)
            elif message_from.text == "Понизить до Админа":
                await bot.send_message(SetAdmin[1], "⬇️Вы понижены до <b>Админа</b>", parse_mode=types.ParseMode.HTML)
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            buttons = ["Назначить/удалить админа", "Меню"]
            keyboard.add(*buttons)
            await SQLite_db.db_write_Admin("Admin", SetAdmin[1])
            await message_from.answer(f"Админы{await ListAdmin()}\n\n*😎 СуперАдмин", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            SetAdmin = [0]
        elif message_from.text == "Назначить Супер Админом":
            await bot.send_message(SetAdmin[1], "💎Вы назначены <b>Супер Админом</b>", parse_mode=types.ParseMode.HTML)
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            buttons = ["Назначить/удалить админа", "Меню"]
            keyboard.add(*buttons)
            await SQLite_db.db_write_Admin("SuperAdmin", SetAdmin[1])
            await message_from.answer(f"Админы{await ListAdmin()}\n\n*😎 СуперАдмин", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            SetAdmin = [0]
        elif message_from.text == "Понизить до Пользователя":
            await bot.send_message(SetAdmin[1], "❌Вы сняты с должности <b>Админа</b>", parse_mode=types.ParseMode.HTML)
            keyboard = types.ReplyKeyboardMarkup(
                row_width=2, resize_keyboard=True)
            buttons = ["Назначить/удалить админа", "Меню"]
            keyboard.add(*buttons)
            await SQLite_db.db_write_Admin("user", SetAdmin[1])
            await message_from.answer(f"Админы\n{await ListAdmin()}\n\n*😎 СуперАдмин", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            SetAdmin = [0]

    if DelCategory[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelCategory = [0]
        else:
            try:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["Да", "Отмена"]
                keyboard.add(*buttons)
                await message_from.answer(f"<b>Точно удалить эту КАТЕГОРИЮ?</b>\n\n<b>{message_from.text.upper()}</b>\n\n{await SQLite_db.db_read_product_Category(message_from.text)}\n\n⚠️Все товары данной категории будут безвозвратно удалены!", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                DelCategory[0] = 2
                DelCategory.append(message_from.text)
            except Exception as e:
                await message_from.answer(f"🛑Ошибка\n\n*{e}")
    elif DelCategory[0] == 2:
        if message_from.text == "Да":
            try:
                await SQLite_db.delete_category(DelCategory[1])
                await message_from.answer("🗑️Категория успешно удалена!", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
                DelCategory = [0]
            except Exception as e:
                await message_from.answer(f"🛑Ошибка\n\n*{e}")
        else:
            await message_from.answer("❌Удаление <b>ОТМЕНЕНО</b>", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelCategory = [0]

    if Promo[0] == 1:
        try:
            if int(await SQLite_db.db_read_promo(message_from.text, 2)) > 0:
                string = str(await SQLite_db.db_read_id(message_from.from_id, 5)).split()
                num = 1

                for x in string:
                    if x == message_from.text:
                        num = 0

                if num == 0:
                    await message_from.answer("❌Вы уже активировали этот промокод")
                else:
                    num = int(re.search(r'\d+', message_from.text).group())
                    money = int(await SQLite_db.db_read_id(message_from.from_id, money_db))
                    await SQLite_db.db_write_money(money+num, message_from.from_id)
                    await message_from.answer("✅Промокод успешно активирован")
                    string2 = f"{str(await SQLite_db.db_read_id(message_from.from_id, 5))} {str(message_from.text)}"
                    await SQLite_db.db_write_promo(string2, message_from.from_id)
                    await SQLite_db.db_write_promo_count(int(await SQLite_db.db_read_promo(message_from.text, 2))-1, message_from.text)
                    Promo = [0]
            else:
                await message_from.answer("☹️Промокод закончился")
                Promo = [0]
        except Exception as e:
            await message_from.answer(f"Промокода не существует \n\n*{e}")
            Promo = [0]

    if Setpromo[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            Setpromo = [0]
        else:
            Setpromo.append(message_from.text)
            await message_from.answer("Введи <b>Количество</b> промокодов", parse_mode=types.ParseMode.HTML)
            Setpromo[0] = 2
    elif Setpromo[0] == 2:
        count = int(message_from.text)
        await SQLite_db.Add_promo(count, Setpromo[1])
        NumPromo = int(re.search(r'\d+', Setpromo[1]).group())
        await message_from.answer(f"<b>Промокод успешно создан!</b>\n\nСумма промокода: {NumPromo}\n\nКоличество активаций: {count}", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
        Setpromo = [0]

    if DelPromo[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelPromo = [0]
        else:
            try:
                await SQLite_db.delete_promo(message_from.text)
                await message_from.answer("🗑️Промокод успешно удален!", parse_mode=types.ParseMode.HTML)

                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                buttons = ("Отмена")
                keyboard.add(buttons)
                message = []
                for prom in list(await SQLite_db.db_read_all_promo()):
                    if prom[2] > 0:
                        message.append(
                            str(f"<b>{prom[1]}</b>  |  {prom[2]}   🟢\n"))
                    elif prom[2] <= 0:
                        message.append(
                            str(f"<b>{prom[1]}</b>  |  {prom[2]}   🔴\n"))
                string = "\n".join(message)
                await message_from.answer(f"<b>Все Промокоды:</b>\n\n{string}\n\n<u>Введи промокод который нужно удалить</u>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            except Exception as e:
                await message_from.answer(f"🛑Ошибка\n\n*{e}")

    if ClearPromo[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            ClearPromo = [0]
        else:
            await SQLite_db.Clear_promo()
            await message_from.answer(f"✅Все данные о промокодах ОЧИЩЕНЫ", reply_markup=await AdminKeyboard())
            ClearPromo = [0]

    if SearchUser[0] == 1:
        if message_from.text == "Отмена":
            buttons = [types.InlineKeyboardButton(
                text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                text="Удалить Пользователя", callback_data="DelUser")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            SearchUser = [0, 0]
            await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
        else:
            try:
                try:
                    a = int(message_from.text)
                    keyboard = types.ReplyKeyboardMarkup(
                        row_width=2, resize_keyboard=True)
                    buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                    keyboard.add(*buttons)
                    await message_from.answer(f"ID: {message_from.text}\n\nРоль: {await SQLite_db.db_read_id(message_from.text, 1)}\n\nБаланс: {await SQLite_db.db_read_id(message_from.text, 2)} \n\nПокупок на суммму: {await SQLite_db.db_read_id(message_from.text, 3)}\n\nНик: @{await SQLite_db.db_read_id(message_from.text, 4)}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    SearchUser[0] = 2
                    SearchUser[1] = int(message_from.text)
                except:
                    keyboard = types.ReplyKeyboardMarkup(
                        row_width=2, resize_keyboard=True)
                    buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                    keyboard.add(*buttons)
                    await message_from.answer(f"ID: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1]}]\n\nБаланс: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][2]} \n\nПокупок на суммму: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][3]}\n\nНик: {message_from.text}", reply_markup=keyboard)
                    SearchUser[0] = 2
                    SearchUser[1] = str(message_from.text)
            except:
                await message_from.answer("🛑Ошибка, не найдено значений\n\nПопробуйте ввести данные еще раз")
    elif SearchUser[0] == 2:
        if message_from.text == "Отмена":
            buttons = [types.InlineKeyboardButton(
                text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                text="Удалить Пользователя", callback_data="DelUser")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            SearchUser = [0, 0]
            await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
        elif message_from.text == "➕ баланс":
            await message_from.answer(f"<b>Введи сколько начислить баланса</b>", parse_mode=types.ParseMode.HTML)
            SearchUser[0] = 3
        elif message_from.text == "➖ баланс":
            await message_from.answer(f"<b>Введи сколько отнять баланса</b>", parse_mode=types.ParseMode.HTML)
            SearchUser[0] = 4
    elif SearchUser[0] == 3:
        try:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                a = int(SearchUser[1])
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                keyboard.add(*buttons)
                plusMoney = int(await SQLite_db.db_read_id(SearchUser[1], 2)) + int(message_from.text)
                await SQLite_db.db_write_money(int(plusMoney), SearchUser[1])
                await message_from.answer(f"ID: {SearchUser[1]}\n\nРоль: {await SQLite_db.db_read_id(SearchUser[1], 1)}\n\nБаланс: {await SQLite_db.db_read_id(SearchUser[1], 2)} \n\nПокупок на суммму: {await SQLite_db.db_read_id(SearchUser[1], 3)}\n\nНик: @{await SQLite_db.db_read_id(SearchUser[1], 4)}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser[0] = 2
        except:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                keyboard.add(*buttons)
                plusMoney2 = int(list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][2]) + int(message_from.text)
                await SQLite_db.db_write_money(int(plusMoney2), int(list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][0]))
                await message_from.answer(f"ID: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][1]}]\n\nБаланс: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][2]} \n\nПокупок на суммму: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][3]}\n\nНик: {SearchUser[1]}", reply_markup=keyboard)
                SearchUser[0] = 2
    elif SearchUser[0] == 4:
        try:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                a = int(SearchUser[1])
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                keyboard.add(*buttons)
                plusMoney = int(await SQLite_db.db_read_id(SearchUser[1], 2)) - int(message_from.text)
                if plusMoney < 0:
                    plusMoney = 0
                await SQLite_db.db_write_money(int(plusMoney), SearchUser[1])
                await message_from.answer(f"ID: {SearchUser[1]}\n\nРоль: {await SQLite_db.db_read_id(SearchUser[1], 1)}\n\nБаланс: {await SQLite_db.db_read_id(SearchUser[1], 2)} \n\nПокупок на суммму: {await SQLite_db.db_read_id(SearchUser[1], 3)}\n\nНик: @{await SQLite_db.db_read_id(SearchUser[1], 4)}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser[0] = 2
        except:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                buttons = ["➕ баланс", "➖ баланс", "Отмена"]
                keyboard.add(*buttons)
                plusMoney2 = int(list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][2]) - int(message_from.text)
                if plusMoney2 < 0:
                    plusMoney2 = 0
                await SQLite_db.db_write_money(int(plusMoney2), int(list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][0]))
                await message_from.answer(f"ID: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][1]}]\n\nБаланс: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][2]} \n\nПокупок на суммму: {list(await SQLite_db.db_read_username(str(SearchUser[1]).upper().replace('@', '')))[0][3]}\n\nНик: {SearchUser[1]}", reply_markup=keyboard)
                SearchUser[0] = 2

    if DelUser[0] == 1:
        if message_from.text == "Отмена":
            buttons = [types.InlineKeyboardButton(
                text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                text="Удалить Пользователя", callback_data="DelUser")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            DelUser = [0, 0]
            await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
        else:
            try:
                try:
                    keyboard = types.ReplyKeyboardMarkup(
                        row_width=2, resize_keyboard=True)
                    buttons = ["Да", "Отмена"]
                    keyboard.add(*buttons)
                    a = int(message_from.text)
                    a = a + a
                    await message_from.answer(f"<b>Точно удалить этого пользователя?</b>\n\nID: {message_from.text}\n\nРоль: {await SQLite_db.db_read_id(message_from.text, 1)}\n\nБаланс: {await SQLite_db.db_read_id(message_from.text, 2)} \n\nПокупок на суммму: {await SQLite_db.db_read_id(message_from.text, 3)}\n\nНик: @{await SQLite_db.db_read_id(message_from.text, 4)}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    DelUser[0] = 2
                    DelUser[1] = int(message_from.text)
                except:
                    try:
                        keyboard = types.ReplyKeyboardMarkup(
                            row_width=2, resize_keyboard=True)
                        buttons = ["Да", "Отмена"]
                        keyboard.add(*buttons)
                        await message_from.answer(f"<b>Точно удалить этого пользователя?</b>\n\nID: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][1]}]\n\nБаланс: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][2]} \n\nПокупок на суммму: {list(await SQLite_db.db_read_username(str(message_from.text).upper().replace('@', '')))[0][3]}\n\nНик: {message_from.text}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                        DelUser[0] = 2
                        DelUser[1] = str(message_from.text)
                    except:
                        try:
                            ListId = [x.strip()
                                      for x in message_from.text.split(",")]
                            keyboard = types.ReplyKeyboardMarkup(
                                row_width=2, resize_keyboard=True)
                            buttons = ["Да", "Отмена"]
                            keyboard.add(*buttons)
                            ListID2 = []
                            for id in ListId:
                                try:
                                    try:
                                        await message_from.answer(f"ID: {id}\n\nРоль: {await SQLite_db.db_read_id(id, 1)}\n\nБаланс: {await SQLite_db.db_read_id(id, 2)} \n\nПокупок на суммму: {await SQLite_db.db_read_id(id, 3)}\n\nНик: @{await SQLite_db.db_read_id(id, 4)}", parse_mode=types.ParseMode.HTML)
                                        ListID2.append(id)
                                    except:
                                        await message_from.answer(f"ID: {list(await SQLite_db.db_read_username(str(id).upper().replace('@', '')))[0][0]}\n\nРоль: [{list(await SQLite_db.db_read_username(str(id).upper().replace('@', '')))[0][1]}]\n\nБаланс: {list(await SQLite_db.db_read_username(str(id).upper().replace('@', '')))[0][2]} \n\nПокупок на суммму: {list(await SQLite_db.db_read_username(str(id).upper().replace('@', '')))[0][3]}\n\nНик: {id}", reply_markup=keyboard)
                                        ListID2.append(list(await SQLite_db.db_read_username(str(id).upper().replace('@', '')))[0][0])
                                except:
                                    await message_from.answer(f"Пользователь <b>{id}</b> НЕ НАЙДЕН", parse_mode=types.ParseMode.HTML)

                            if not ListID2:
                                buttons = [types.InlineKeyboardButton(
                                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(
                                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                                    text="Поиск по условию", callback_data="SearchIfUser")]
                                keyboard2 = types.InlineKeyboardMarkup(
                                    row_width=1)
                                keyboard2.add(*buttons)
                                user, admin, superadmin = await SQLite_db.Count_All_User()
                                await message_from.answer(f"<b>Управление Пользователями</b>\n\n😀Пользователей: {user}\n\n💎Админов: {admin}\n\n😎СуперАдминов: {superadmin}", reply_markup=keyboard2, parse_mode=types.ParseMode.HTML)
                                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
                                DelUser = [0, 0]
                            else:
                                DelUser[0] = 3
                                DelUser[1] = (ListID2)
                                await message_from.answer(f"<b>Точно удалить ВСЕХ этих пользователей?</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                        except:
                            await message_from.answer(f"🛑Ошибка, введен не список чисел или не число, введи СПИСОК ЧИСЕЛ через запятую ИЛИ ЧИСЛО еще раз\n\n*или таких id нет")
            except:
                await message_from.answer("🛑Ошибка, не найдено значений\n\nПопробуйте ввести данные еще раз")
    elif DelUser[0] == 2:
        try:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                DelUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                a = int(DelUser[1])

                await SQLite_db.delete_user(DelUser[1])
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                user, admin, superadmin = await SQLite_db.Count_All_User()
                await message_from.answer(f"🗑️<b>Пользователь успешно удален!</b>", parse_mode=types.ParseMode.HTML)
                await message_from.answer(f"<b>Управление Пользователями</b>\n\n😀Пользователей: {user}\n\nn💎Админов: {admin}\\nnn😎СуперАдминов: {superadmin}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
                DelUser = [0, 0]
        except:
            if message_from.text == "Отмена":
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                SearchUser = [0, 0]
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            else:
                await SQLite_db.delete_user(list(await SQLite_db.db_read_username(str(DelUser[1]).upper().replace('@', '')))[0][0])
                buttons = [types.InlineKeyboardButton(
                    text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(
                    text="Удалить Пользователя", callback_data="DelUser"), types.InlineKeyboardButton(
                    text="Поиск по условию", callback_data="SearchIfUser")]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                user, admin, superadmin = await SQLite_db.Count_All_User()
                await message_from.answer(f"<b>Пользователь успешно удален!</b>", parse_mode=types.ParseMode.HTML)
                await message_from.answer(f"<b>Управление Пользователями</b>\n\n😀Пользователей: {user}\n\nn💎Админов: {admin}\nn\n😎СуперАдминов: {superadmin}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
                DelUser = [0]
    elif DelUser[0] == 3:
        if message_from.text == "Отмена":
            buttons = [types.InlineKeyboardButton(
                text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(text="Кол-во пользователей", callback_data="CountUser"), types.InlineKeyboardButton(
                text="Удалить Пользователя", callback_data="DelUser")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            await message_from.answer("❌Действие отменено", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            DelUser = [0, 0]
            await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
        else:
            for id in DelUser[1]:
                await SQLite_db.delete_user(id)

            buttons = [types.InlineKeyboardButton(
                text="Поиск Пользователя", callback_data="SearchUser"), types.InlineKeyboardButton(
                text="Удалить Пользователя", callback_data="DelUser")]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            user, admin, superadmin = await SQLite_db.Count_All_User()
            await message_from.answer(f"<b>Пользователи успешно удалены!</b>", parse_mode=types.ParseMode.HTML)
            await message_from.answer(f"<b>Управление Пользователями</b>\n\n😀Пользователей: {user}\n\n💎Админов: {admin}\n\n😎СуперАдминов: {superadmin}", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            await message_from.answer("Меню", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DelUser = [0, 0]

    if UpPriceAll[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            UpPriceAll = [0]
        else:
            try:
                UpPricePlus = int(message_from.text)
                await SQLite_db.UpPrice("+", UpPricePlus)
                await message_from.answer(f"Цены на ВСЕ товары успешно ПОДНЯТЫ на {UpPricePlus}", reply_markup=await AdminKeyboard())
                UpPriceAll = [0]
            except:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                keyboard.add("Отмена")
                await message_from.answer("🛑<b>Ошибка</b>, введите число еще раз", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                UpPriceAll[0] = 1

    if DownPriceAll[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DownPriceAll = [0]
        else:
            try:
                DownPriceAlMinus = int(message_from.text)
                await SQLite_db.UpPrice("-", DownPriceAlMinus)
                await message_from.answer(f"Цены на ВСЕ товары успешно СНИЖЕНЫ на {DownPriceAlMinus}", reply_markup=await AdminKeyboard())
                DownPriceAll = [0]
            except:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                keyboard.add("Отмена")
                await message_from.answer("🛑<b>Ошибка</b>, введите число еще раз", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                DownPriceAll[0] = 1

    if UpPriceAllCent[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            UpPriceAllCent = [0]
        else:
            try:
                UpPriceAllCentMulti = int(message_from.text)
                await SQLite_db.UpPrice("*", UpPriceAllCentMulti)
                await message_from.answer(f"Цены на ВСЕ товары успешно ПОДНЯТЫ на {UpPriceAllCentMulti} %", reply_markup=await AdminKeyboard())
                UpPriceAllCent = [0]
            except:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                keyboard.add("Отмена")
                await message_from.answer("🛑<b>Ошибка</b>, введите число еще раз", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                UpPriceAllCent[0] = 1

    if DownPriceAllCent[0] == 1:
        if message_from.text == "Отмена":
            await message_from.answer("❌Действие отменено", reply_markup=await AdminKeyboard(), parse_mode=types.ParseMode.HTML)
            DownPriceAllCent = [0]
        else:
            try:
                DownPriceAllCentDiv = int(message_from.text)
                await SQLite_db.UpPrice("/", DownPriceAllCentDiv)
                await message_from.answer(f"Цены на ВСЕ товары успешно СНИЖЕНЫ на {DownPriceAllCentDiv} %", reply_markup=await AdminKeyboard())
                DownPriceAllCent = [0]
            except:
                keyboard = types.ReplyKeyboardMarkup(
                    row_width=2, resize_keyboard=True)
                keyboard.add("Отмена")
                await message_from.answer("🛑<b>Ошибка</b>, введите число еще раз", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                DownPriceAllCent[0] = 1


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
