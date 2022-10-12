import logging
from forex_python.converter import CurrencyRates
from google_trans_new import google_translator
from aiogram import Bot, Dispatcher, types, executor
from asyncio import sleep


logging.basicConfig(level=logging.INFO, filename='bot.log', format='%(asctime)s - %(levelname)s - %(funcName)s: - %(message)s')
bot = Bot('TOKEN HEREgit')
dp = Dispatcher(bot)
translator = google_translator()
currency = CurrencyRates()


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer(f"Привет, {message.from_user.username}")
    logging.info(f"{message.from_user.username}@{message.from_user.id} применил START")


@dp.message_handler(commands=['game'])
async def game(message: types.Message):
    logging.info(f"{message.from_user.username}@{message.from_user.id} применил GAME")
    await message.answer(f"Что же, давай сыграем! Я кидаю два кубика.")
    await sleep(0.5)
    score_bot = await bot.send_dice(chat_id=message.chat.id)
    score_player = await bot.send_dice(chat_id=message.chat.id)
    await sleep(6)
    await message.answer(f"Посмотрим...")
    await sleep(1)
    if score_bot.dice.value > score_player.dice.value:
        await message.answer(f"Ха, мне выпало {score_bot.dice.value}, а тебе, похоже, {score_player.dice.value}. \nЯ победил!")
    elif score_bot.dice.value == score_player.dice.value:
        await message.answer(f"У нас обоих {score_bot.dice.value}, победителей нет :D")
    else:
        await message.answer(f"Черт, мне выпало {score_bot.dice.value}... А тебе {score_player.dice.value}. \nТы победил!")


@dp.message_handler(commands=['currency'])
async def get_currency(message: types.Message):
    await message.answer(f"Текущий курс валют по отнощению к швейцарскому франку:"
                         f"\nCFH -> USD {'%.3f' % currency.get_rate('CHF', 'USD')}"
                         f"\nCFH -> EUR {'%.3f' % currency.get_rate('CHF', 'EUR')}")
    logging.info(f"{message.from_user.username}@{message.from_user.id} применил CURRENCY")


@dp.message_handler(commands=['translate'])
async def get_translation(message: types.Message):
    trequest = ' '.join(message.text.split()[1:])
    result = translator.translate(trequest, lang_tgt='ru')
    await message.reply(result)
    logging.info(f"{message.from_user.username}@{message.from_user.id} применил TRANSLATE, {trequest}, {result}")


@dp.message_handler(commands=['sticker'])
async def sticker_reply(message: types.Message):
    await message.reply_sticker('CAACAgQAAxkBAAIBX2MnodBWtn5peM25RyoDmxIg5B-bAAK_AAORf_kLeKJU86lmYpwpBA')
    logging.info(f"{message.from_user.username}@{message.from_user.id} попросил меня отправить стикер!")


@dp.message_handler(content_types=['sticker'])
async def sticker_check(message: types.Message):
    logging.info(f"{message.from_user.username}@{message.from_user.id} отправил стикер, ID = {message.sticker.file_id}")


@dp.message_handler()
async def chitchat(message: types.Message):
    logging.info(f"{message.from_user.username}@{message.from_user.id} написал '{message.text}'")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
