Здравствуйте! Оставлю здесь небольшие комментарии по проекту.
Бот - @project_dl_bot, [ссылка ](https://t.me/bird_species_bot)
Что в файлах:
1. [bot.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/bot.py) - основной файл, содержащий всю реализацию функционала бота, из него "вызывается" функция обработки фото
	- а. Реагирует на команды /start, /help - выводит основную основную информацию по функционалу бота
	   ![image](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/report/img1.png)
	- b. Реагирует на присланную фотографию боту, причем по-разному, если это первая, или вторая фотография.
		Фотографии сохраняются на сервере, в массив записываю путь к фото. Когда длина массива == 2, т.е. прислано 2 фото, бот начинает обработку, после чего удаляет фото и очищает массив.
	   ![image](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/report/img2.png)
	   ![image](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/report/img3.png)
	   ![image](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/report/img4.png)
	- с. Реагирует на сообщения "привет", "пока" определенными сообщениями, остальные просто дублирует.
	   ![image](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/report/img5.png)

2. [model_adain.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/model_adain.py) - реализация модели, которая будет переносить стили.

3. [inference_adain.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/inference_adain.py) - инференс модели, все обернуто в одну функцию, на вход подается массив, содержищий пути к двум
			фото, с которыми модель и работает.

4. [nst.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/nst.py) - код с занятий  (матрица Грамма), использовал ее сначала, перед тем, как реализовал AdaIn
	    выбрать, какая сеть будет обрабатывать фото нельзя!

5. [prepare_photo.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/prepare_photo.py) - функция обработки изображения, использовалась в nst.py
		      В конечной версии также как и nst.py не используется.

6. [training_adain.py](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/training/training_adain.ipynb) - 
	ноутбук с обучением сети, там же указаны датасеты, на которых обучалась.

7. /file_in_directory - специальная команда, выводящая все файлы в рабочей директории. Изначально использовалась для отладки, однако
		       решил оставить в конечной версии (пару раз случалось, что то ли из-за сбоя на сервере,
		       то ли, еще чего, конечное фото не отправляется, из-за чего массив не обнуляется и приходится перезапускать бота).
		       Потенциальный пользователь об этой команде не знает.
		       P.s. но сломаться ничего не должно, отлаживал.

8. Воспользовался [Kaffeine](https://kaffeine.herokuapp.com/#!), которая не дает боту заснуть. Не знаю насколько это было правомочно. Единственное бот не будет работать с часу ночи
	до 7 утра (ограничения heroku и Kaffeine). В остальное время бот должен работать бесперебойно.

9. Телеграмм для связи: @meemlop