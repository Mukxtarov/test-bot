import json
import re
import time
import os
import sys
import datetime
import xlsxwriter as excel
from telethon import TelegramClient, events
from telethon import functions, types
from telethon import Button
from database import Database as db
from database import Helper as helper


""" config.json file ichidagi sozlamarni chaqirish massiv holatida """
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'config.json'), 'r',
          encoding='utf-8') as file:
    config = json.load(file)

""" search massivni ishlatish uchun """
route = {"status": ""}


""" Bot sessiya saqlaydigan faylni joyini korsatish """
session_bot = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'bot')

""" Telegram Clientga ulanish """
bot = TelegramClient(session_bot, config['api_id'], config['api_hash']).start(bot_token=config['token'])

""" message.json file ichidagi so'zlarni chaqirish massiv holatida """
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'messages.json'), 'r',
          encoding='utf-8') as file:
    message = json.load(file)


number_session = {"question": 0}





@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    route['status'] = "start"

    db.InsertUser(event.sender.id, {
        'user_id': event.sender.id,
        'first_name': str(event.sender.first_name),
        'last_name': str(event.sender.last_name),
        'username': str(event.sender.username),
        'updated_at': datetime.datetime.today()
    })

    try:
        buttons_check = [
            [Button.url(message['azo_boling'], url=config['channel_url'])],
            [Button.inline(message['check_azo'], data="check_channel")]
        ]

        check = await bot(functions.channels.GetParticipantRequest(channel=config['channel_id'], user_id=event.sender.id))

        if check.users[0].id != event.sender.id:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation
    except Exception as e:
        if e:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation

    buttons = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    await event.reply(message['welcome'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation








@bot.on(events.CallbackQuery(pattern='check_channel'))
async def create_test(event):
    try:
        buttons_check = [
            [Button.url(message['azo_boling'], url=config['channel_url'])],
            [Button.inline(message['check_azo'], data="check_channel")]
        ]

        check = await bot(functions.channels.GetParticipantRequest(channel=config['channel_id'], user_id=event.sender.id))

        if check.users[0].id != event.sender.id:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation
    except Exception as e:
        if e:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation

    buttons = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    await event.edit(message['welcome'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation






@bot.on(events.CallbackQuery(pattern='create_test'))
async def create_test(event):
    route['status'] = "create_test"

    buttons = [Button.inline(message['home'], data="back")]

    await event.edit(message['create_test_text'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation







@bot.on(events.CallbackQuery(pattern='answer_the_test'))
async def answer_test(event):
    route['status'] = "answer_the_test"

    buttons = [Button.inline(message['home'], data="back")]

    await event.edit(message['answer_test_text'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation








@bot.on(events.CallbackQuery(pattern='back'))
async def back(event):
    route['status'] = "start"

    db.InsertUser(event.sender.id, {
        'user_id': event.sender.id,
        'first_name': str(event.sender.first_name),
        'last_name': str(event.sender.last_name),
        'username': str(event.sender.username),
        'updated_at': datetime.datetime.today()
    })

    buttons = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    await event.edit(message['welcome'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation










@bot.on(events.NewMessage(pattern=r'savol=+[0-9]+-+[a-zA-Z]'))
async def create_test_full(event):

    try:
        buttons_check = [
            [Button.url(message['azo_boling'], url=config['channel_url'])],
            [Button.inline(message['check_azo'], data="check_channel")]
        ]

        check = await bot(functions.channels.GetParticipantRequest(channel=config['channel_id'], user_id=event.sender.id))

        if check.users[0].id != event.sender.id:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation
    except Exception as e:
        if e:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation




    buttons_create = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    buttons = [Button.inline(message['home'], data="back")]

    if route['status'] != "create_test":
        await event.reply(message['welcome'], buttons=buttons_create, parse_mode="HTML")
        raise events.StopPropagation

    data = event.message.message.split('-')

    number = int(data[0].split('=')[1])
    answer = str(data[1].replace(" ", ""))
    if len(answer) > 50 or len(str(number)) > 10:
        await event.reply("Savollar soni maksimal 50 ta va Maxsus ID raqamlari soni maksimal 10 ta bo'lishi kerak !")
        raise events.StopPropagation


    question = db.InsertQuestion(number, {
                    'user_id': event.sender.id,
                    'number': number,
                    'answer': answer,
                    'active': True
                })

    await event.reply(question.replace('<b>{ID}</b>', str(number)), buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation










@bot.on(events.NewMessage(pattern=r'[0-9]+-+[a-zA-Z]'))
async def answer_test_full(event):

    try:
        buttons_check = [
            [Button.url(message['azo_boling'], url=config['channel_url'])],
            [Button.inline(message['check_azo'], data="check_channel")]
        ]

        check = await bot(functions.channels.GetParticipantRequest(channel=config['channel_id'], user_id=event.sender.id))

        if check.users[0].id != event.sender.id:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation
    except Exception as e:
        if e:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation



    buttons_answer = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    buttons = [Button.inline(message['home'], data="back")]

    if route['status'] != "answer_the_test":
        await event.reply(message['welcome'], buttons=buttons_answer, parse_mode="HTML")
        raise events.StopPropagation



    data = event.message.message.split('-')

    number = int(data[0])
    answer = str(data[1].replace(" ", "")).lower()

    print(answer)
    answers = db.showAnswerInfo(event.sender.id, number)

    if str(answers) != "None":
        await event.reply("Kechirasiz siz bu testga oldin javob bergansiz.", buttons=buttons, parse_mode="HTML")
        raise events.StopPropagation


    question = db.showQuestionInfo(number)

    if str(question) == "None":
        await event.reply("Siz javob bermoqchi bo'lgan test mavjud emas yoki o'chirilgan.", buttons=buttons, parse_mode="HTML")
        raise events.StopPropagation


    if len(answer) != len(question['answer']):
        await event.reply("Savolning soniga siz bergan javoblar soni to'g'ri kelmaydi.", buttons=buttons, parse_mode="HTML")
        raise events.StopPropagation

    db.InsertAnswer({
        'user_id': event.sender.id,
        'number': number,
        'answer': answer
    })

    result = helper.AnswerFactory(answer, question)

    db.InsertRating({
        'user_id': event.sender.id,
        'number': number,
        'correct_answer': result['done'],
        'wrong_answer': result['wrong'],
        'total_score': result['ball']
    })

    await event.reply("<b>Test soni: {} ta\n\n{}\nTo'g'ri javoblar: {} ta\nNoto'g'ri javoblar: {} ta\n\nTo'plangan ball: {} ball</b>".format(result['i'], result['text'], result['done'], result['wrong'], result['ball']), buttons=result['button'], parse_mode="HTML")

    raise events.StopPropagation









@bot.on(events.NewMessage(pattern=r'natija=+[0-9]'))
async def rating(event):

    data = event.message.message.split('=')
    number = data[1]
    number_session['question'] = number
    try:
        buttons_check = [
            [Button.url(message['azo_boling'], url=config['channel_url'])],
            [Button.inline(message['check_azo'], data="check_channel")]
        ]

        check = await bot(functions.channels.GetParticipantRequest(channel=config['channel_id'], user_id=event.sender.id))

        if check.users[0].id != event.sender.id:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation
    except Exception as e:
        if e:
            await event.reply(message['subs_channel'], buttons=buttons_check, parse_mode="HTML")
            return
            raise events.StopPropagation

    question = db.showQuestionInfo(number)

    ratinginfo = db.showRatingInfo(number)

    if str(ratinginfo) == "None" or str(question) == "None":
        button = [Button.inline(message['home'], data="back")]
        await event.reply("Siz kiritgan test raqami bo'yicha reyting mavjud emas!", buttons=button, parse_mode="HTML")
        raise events.StopPropagation

    if question['user_id'] == event.sender.id and str(ratinginfo) != "None":
        buttons = [
            [Button.inline(message['back_page'], data="page=2"),
                Button.inline(message['next_page'], data="page={}".format(config['rating_show_limit']))],
            [Button.inline(message['natija_export_excel'], data="natija_export_excel={}".format(number))],
            [Button.inline(message['home'], data="back")],
            [Button.inline(message['stop_test'],
                           data="stop_test={}".format(question['number']))]

        ]

        await event.reply("<b>📌 Testni yakunlashdan oldin natijani saqlab oling test yakunlangandan so'ng natija ko'rsatilmaydi.</b>", parse_mode="HTML")

    else:
        buttons = [
                [Button.inline(message['back_page'], data="page=2={}".format(number)),
                Button.inline(message['next_page'], data="page={}={}".format(config['rating_show_limit'], number))],
                [Button.inline(message['natija_export_excel'], data="natija_export_excel={}".format(number))],
                [Button.inline(message['home'], data="back")]
            ]

    offset = 0
    limit = config['rating_show_limit']
    rating = db.showRatingInfoAll(number, offset, limit)

    ratingcount = db.showRatingInfoCount(number)

    i = offset
    text = "<b>🤓 Test {} natijalari:</b>\n<b>Javob berganlar soni: {} ta | {} - {}</b>\n\n"\
                    .format(number, ratingcount, offset, ratingcount)

    for rate in rating:
        i += 1
        first_name = rate['first_name'].replace("'", "`")
        last_name  = rate['last_name'].replace("'", "`")
        score = rate['total_score']

        text += "<b>{}</b>. {} {}- <b>{} ball</b>\n".format(
                    helper.the_best(i), first_name, last_name.replace("None", ""), score
                    )

    async with bot.action(event.sender.id, "typing"):
        await event.reply("{}".format(text), buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation








@bot.on(events.CallbackQuery(pattern=r'stop_test=+[0-9]'))
async def stop_test(event):
    route['status'] = "stop_test"
    data = event.data.decode('UTF-8').split("=")
    number = data[1]

    delete = db.DeleteQuestion(event.sender.id, number)


    if delete == 1:
        await event.answer(message['test_stop'].replace("{ID}", number), alert=True)
    else:
        await event.answer("Test yakunlanmadi qayta urinib ko'ring!", alert=True)

    buttons = [
        [Button.inline(message['create_test'], data="create_test")],
        [Button.inline(message['answer_the_test'], data="answer_the_test")]
    ]

    await event.edit(message['welcome'], buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation








@bot.on(events.CallbackQuery(pattern=r'page=+[0-9]+=+[0-9]'))
async def pagination(event):
    route['status'] = "pagination"

    data = event.data.decode('UTF-8').split("=")
    page = int(data[1])
    number = int(data[2])

    if page == 2:
        await event.answer(message['page_home_not_back'], alert=True)
        raise events.StopPropagation
    elif page == 0:
        back = "page=2={}".format(number)
        next = "page={}={}".format(config['rating_show_limit'], number)
    else:
        back = "page={}={}".format(int(page) - int(config['rating_show_limit']), number)
        next = "page={}={}".format(int(page) + int(config['rating_show_limit']), number)

    question = db.showQuestionInfo(number)

    ratinginfo = db.showRatingInfo(number)

    if question['user_id'] == event.sender.id and str(ratinginfo) != "None":
        buttons = [
            [Button.inline(message['back_page'], data=back),
                Button.inline(message['next_page'], data=next)],
            [Button.inline(message['natija_export_excel'], data="natija_export_excel={}".format(number))],
            [Button.inline(message['home'], data="back")],
            [Button.inline(message['stop_test'],
                           data="stop_test={}".format(question['number']))]

        ]

    else:
        buttons = [
                [Button.inline(message['back_page'], data=back),
                Button.inline(message['next_page'], data=next)],
                [Button.inline(message['natija_export_excel'], data="natija_export_excel={}".format(number))],
                [Button.inline(message['home'], data="back")]
            ]


    offset = page
    limit = config['rating_show_limit']

    rating = db.showRatingInfoAll(number, offset, limit)
    ratingcount = db.showRatingInfoCount(number)

    if not rating:
        await event.answer(message['page_stop_not_next'], alert=True)
        raise events.StopPropagation

    i = offset
    text = "<b>🤓 Test {} natijalari:</b>\n<b>Javob berganlar soni: {} ta | {} - {}</b>\n\n"\
                    .format(number, ratingcount, offset, ratingcount)

    for rate in rating:
        i += 1
        first_name = rate['first_name'].replace("'", "`")
        last_name  = rate['last_name'].replace("'", "`")
        score = rate['total_score']

        text += "<b>{}</b>. {} {}- <b>{} ball</b>\n".format(
                    helper.the_best(i), first_name, last_name.replace("None", ""), score
                    )

    async with bot.action(event.sender.id, "typing"):
        await event.edit("{}".format(text), buttons=buttons, parse_mode="HTML")


    raise events.StopPropagation




@bot.on(events.CallbackQuery(pattern=r'javob_export_excel=+[0-9]'))
async def javob_export_excel(event):
    data = event.data.decode('UTF-8').split("=")
    number = int(data[1])
    try:
        results = db.showAnswerInfo(event.sender.id, number)
        filename = "Test-{}-sizning-natijangiz.xlsx".format(number)
        workbook = excel.Workbook('file/{}'.format(filename))
        worksheet = workbook.add_worksheet()
        i = 0
        for result in results:
            i += 1
            first_name = result['first_name'].replace("'", "`")
            last_name  = result['last_name'].replace("'", "`")
            total_score = result['total_score']

            worksheet.write_number('A{}'.format(i), i)
            worksheet.write_string('B{}'.format(i), "{} {}".format(first_name, last_name.replace("None", "")))
            worksheet.write_string('F{}'.format(i), "{} ball".format(total_score))

        workbook.close()

        async with bot.action(event.sender.id, 'document') as action:
            await event.answer("Yuborilmoqda...")
            await bot.send_file(event.sender.id, file="file/{}".format(filename),
                            buttons=[Button.inline(message['home'], data="back")],
                            parse_mode="HTML", progress_callback=action.progress)
        os.remove("file/{}".format(filename))
    except Exception as e:
        print(e)

    raise events.StopPropagation




@bot.on(events.CallbackQuery(pattern=r'natija_export_excel=+[0-9]'))
async def natija_export_excel(event):
    data = event.data.decode('UTF-8').split("=")
    number = int(data[1])
    try:
        results = db.ForExportRatingInfoAll(number)
        filename = "Test-{}-natijalari.xlsx".format(number)
        workbook = excel.Workbook('file/{}'.format(filename))
        worksheet = workbook.add_worksheet()
        i = 0
        for result in results:
            i += 1
            first_name = result['first_name'].replace("'", "`")
            last_name  = result['last_name'].replace("'", "`")
            total_score = result['total_score']

            worksheet.write_number('A{}'.format(i), i)
            worksheet.write_string('B{}'.format(i), "{} {}".format(first_name, last_name.replace("None", "")))
            worksheet.write_string('F{}'.format(i), "{} ball".format(total_score))

        workbook.close()

        async with bot.action(event.sender.id, 'document') as action:
            await event.answer("Yuborilmoqda...")
            await bot.send_file(event.sender.id, file="file/{}".format(filename),
                            buttons=[Button.inline(message['home'], data="back")],
                            parse_mode="HTML", progress_callback=action.progress)
        os.remove("file/{}".format(filename))
    except Exception as e:
        print(e)

    raise events.StopPropagation









@bot.on(events.NewMessage(pattern="/users"))
async def stop_test(event):
    route['status'] = "users"
    users = db.UsersCount()

    buttons = [Button.inline(message['home'], data="back")]

    await event.reply("Bot foydalanuvchilari soni: {} ta".format(users), buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation



@bot.on(events.NewMessage(pattern="/questions"))
async def stop_test(event):
    route['status'] = "questions"
    active = db.ActiveQuestionsCount()

    noactive = active = db.NoActiveQuestionsCount()

    buttons = [Button.inline(message['home'], data="back")]

    await event.reply("Barcha yaratilgan testlar soni: {} ta\n\nAktiv xolatdagi testlar soni: {} ta\nYakunlangan testlar soni: {} ta".format(active + noactive, active, noactive), buttons=buttons, parse_mode="HTML")

    raise events.StopPropagation
















































def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
