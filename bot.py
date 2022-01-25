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
        "Если что, то обработка в среднем занимает не больше 30 секунд."
    )


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Привет! Давайте попробуем разобраться, что у Вас не получается. Вы можете прислать два изображения и бот "
        "с первой фотографии перенесёт стиль на вторую, после чего отправит получившееся изображение Вам. "
        "Если что, то обработка в среднем занимает не больше 30 секунд, но может и больше, поэтому если изображение "
        "не приходит быстро, пожалуйста подождите чуть больше. Также не стоит отправлять новые изображения пока бот не"
        " обработал предыдущие. Чтобы проверить, что бот работает, Вы можете написать "
        "любое сообщение и бот пришлет его Вам в ответ."
    )


a = []
dct = {}


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(msg):
    random_number = random.randint(0, 10000)
    # await bot.send_message(msg.from_user.id, 'Зашел в функцию')
    if len(a) == 2:
        a.clear()
        await bot.send_message(msg.from_user.id, 'Очистил массив')

    download_dir = './img/'
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        await bot.send_message(msg.from_user.id, 'Создал папку  ' + str(os.getcwd()))
    os.chdir(download_dir)
    await bot.send_message(msg.from_user.id, 'В директории я сейчас  ' + str(os.getcwd()))
    img_name = 'img' + str(msg.from_user.id) + str(random_number) + '.jpg'
    path_to_img = os.getcwd() + '\\img\\' + img_name
    a.append(path_to_img)
    await msg.photo[-1].download('./img/' + img_name)
    if len(a) == 2:
        await bot.send_message(msg.from_user.id, 'Зашел в обработку')

        # output = transforming(a)

        await bot.send_message(msg.from_user.id, 'Начал обработку')
        out = transfering_style(a)
        await bot.send_message(msg.from_user.id, 'Изобр ' + str(out.shape))
        await bot.send_message(msg.from_user.id, 'Закончил обработку')
        # end_time_2 = time.time()

        # print('Inference 1st model is:', end_time_1-start_time_1)
        # print('Inference 2st model is:', end_time_2 - start_time_2)

        # print('begin saving')
        # print(output.shape)
        # print(out.shape)

        # output = output.cpu().clone().detach()
        out = out.cpu().clone().detach()

        # img1 = output[0]
        # save_image(img1, './img/' + 'saving_photo_1.jpg')
        # path_save_img_1 = './img/' + 'saving_photo_1.jpg'

        img1 = out[0]
        save_image(img1, './img/' + 'saving_photo_2.jpg')
        path_save_img_2 = './img/' + 'saving_photo_2.jpg'

        # print('end saving')
        # photo(path_save_img)
        # await bot.send_photo(msg.from_user.id, types.InputFile(path_save_img_1))
        await bot.send_photo(msg.from_user.id, types.InputFile(path_save_img_2))
        # await msg.answer('Фото прислано')
        await bot.send_message(msg.from_user.id, 'Фото готово и прислано Вам')
        # print('end of working')
        # print('begin removing')
        try:
            os.remove(a[0])
            os.remove(a[1])
            os.remove('./img/' + 'saving_photo_2.jpg')
        except:
            FileNotFoundError
        # print('end removing')


@dp.message_handler()
async def echo(message: types.Message):
    if message.text == 'Привет' or message.text == 'привет':
        await message.reply("И Вам привет! "
                            "Если хотите узнать, что я могу напишите '/start' или '/help'. "
                            "Либо можем просто поболтать, Вы отправляйте сообщение, а я буду повторять!")
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
