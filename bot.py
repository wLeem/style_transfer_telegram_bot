from torchvision.utils import save_image
import logging
from aiogram import Bot, Dispatcher, executor, types
import os
import random
# import cv2
# from nst import transforming
from inference_adain import transfering_style
# import torchvision.transforms as transforms
# from prepare_photo import resize_photo
import time
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):
    # logging.warning('Starting connection. ')
    await bot.set_webhook(config.URL_APP, drop_pending_updates=True)


async def on_shutdown(dp):
    await bot.delete_webhook()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Я могу перенести стиль с одной картинки на другую. "
        "Пришли мне две фотографии: с первой фотографии я попробую перенсти "
        "стиль на вторую, и отправлю получившееся изображение Вам в ответ. "
        "Если что, то обработка может занимать достаточно много времени (но не более 2-3х минут)."
    )


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "Привет! Давайте попробуем разобраться, что у Вас не получается. Вы можете прислать два изображения и бот "
        "с первой фотографии перенесёт стиль на вторую, после чего отправит получившееся изображение Вам. "
        "Если что, то обработка в среднем занимает не больше минуты, но может и больше, поэтому если изображение "
        "не приходит быстро, пожалуйста подождите чуть больше. Также не стоит отправлять новые изображения пока бот не"
        " обработал предыдущие. Чтобы проверить, что бот работает, Вы можете написать "
        "любое сообщение и бот пришлет его Вам в ответ."
    )


@dp.message_handler(commands=['file_in_directory'])
async def handle_docs_dir(message: types.Message):
    await message.reply('Я сейчас в директории: ' + os.getcwd())
    files = os.listdir(os.getcwd())
    for file in files:
        await message.reply('Файл : ' + file)


# async def handle_docs_photo(message: types.Message):
#     if "Удалить файл" in message.text:
#         os.remove(message.text.split(':')[1])


a = []
dct = {}


# @dp.message_handler(commands=['clean_massiv'])
def clean_massiv():
    global a
    a = []
    # await bot.send_message(message.from_user.id, 'Зашел в функцию по удалению элементов')
    files = os.listdir(os.getcwd())
    for file in files:
        if ".jpg" in file:
            # await bot.send_message(message.from_user.id, 'Зашел в цикл в функции по удалению элементов и удалил')
            os.remove('/app/' + file)


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(msg):
    # clean_massiv()
    # if len(a) == 2:
    #     a.clear()
    #     await bot.send_message(msg.from_user.id, 'Очистил массив')

    # '/app'
    await bot.send_message(msg.from_user.id, 'Я сейчас в директории ' + str(os.getcwd()))

    img_name = 'img' + '_' + str(len(a)) + '.jpg'
    path_to_img = os.getcwd() + '/' + img_name
    a.append(path_to_img)
    await msg.photo[-1].download(path_to_img)
    await bot.send_message(msg.from_user.id, 'Длина массива сейчас ' + str(len(a)))
    if len(a) == 2:
        await bot.send_message(msg.from_user.id, 'Зашел в обработку')
        await bot.send_message(msg.from_user.id, 'Начал обработку')
        await bot.send_message(msg.from_user.id, 'Длина массива в цикле при переносе ' + str(len(a)))
        await bot.send_message(msg.from_user.id, 'Первый элемент ' + a[0])
        await bot.send_message(msg.from_user.id, 'Второй элемент  ' + a[1])
        start_time = time.time()
        out = transfering_style(a)
        end_time = time.time()
        await bot.send_message(msg.from_user.id, 'Инференс занял: ' + str(end_time-start_time))
        await bot.send_message(msg.from_user.id, 'Изобр ' + str(out.shape))
        await bot.send_message(msg.from_user.id, 'Закончил обработку')

        out = out.cpu().clone().detach()

        img = out[0]
        path_save_img = '/app/' + 'saving_photo.jpg'
        save_image(img, path_save_img)

        await bot.send_photo(msg.from_user.id, types.InputFile(path_save_img))
        await bot.send_message(msg.from_user.id, 'Фото готово и прислано Вам')
        clean_massiv()
        await bot.send_message(msg.from_user.id, 'Удалил все файлы')
        # try:
        #     os.remove(a[0])
        #     os.remove(a[1])
        #     os.remove('/app/' + 'saving_photo.jpg')
        #     await bot.send_message(msg.from_user.id, 'Удалил все файлы')
        # except:
        #     FileNotFoundError


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Привет' or message.text == 'привет':
        await message.reply("И Вам привет! "
                            "Если хотите узнать, что я могу напишите '/start' или '/help'. "
                            "Либо можем просто поболтать, Вы отправляйте сообщение, а я буду повторять!")
    elif "Удалить файл:" in message.text:
        os.remove(message.text.split(':')[1])
        await message.reply("Удалил")
    elif ".jpg" in message.text:
        await bot.send_photo(message.from_user.id, types.InputFile('/app/' + message.text))
    else:
        await message.reply(message.text)


# async def on_startup(_):
#     print('Бот вышел в онлайн')


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path='',
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
