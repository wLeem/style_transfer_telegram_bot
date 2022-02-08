# Style transfer telegram bot

### Telegram bot + AdaIn neural network + Heroku


## Neural network

Firstly, I used [code from pytorch documentation](https://pytorch.org/tutorials/advanced/neural_style_tutorial.html),
where the transfer of styles is implemented using the gram matrix. Such a network processes photos for a very long time 
(several minutes for a 512x512 photo). I decided to use other networks and approaches to style transfer and found Adain for myself.
[Model presentation ](https://www.youtube.com/watch?v=IIRxJvW6bE4&t=304s)

In my work I use piece of irasin implementation: [original implementation ](https://github.com/irasin/Pytorch_AdaIN)
[My code of training NN ](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/training/training_adain.ipynb)
This model processes photos many times faster (inference isn't more than 25 seconds) and the size of the resulting photo is larger than 512x512.

### Results

![image](https://github.com/wLeem/style_transfer_telegram_bot/tree/main/img/collage_1.png)
![image](https://github.com/wLeem/style_transfer_telegram_bot/tree/main/img/collage_2.png)
![image](https://github.com/wLeem/style_transfer_telegram_bot/tree/main/img/collage_3.png)
![image](https://github.com/wLeem/style_transfer_telegram_bot/tree/main/img/collage_4.png)


## Telegram bot + Heroku

A [simple bot ](https://github.com/wLeem/style_transfer_telegram_bot/blob/main/telegram_bot/bot.py) with asynchronous functions on webhook.
Processes sent photos, reacts only to some messages in a special way, the rest is simply forwarded (echo).