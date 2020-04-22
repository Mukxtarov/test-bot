import os
import sys
import pathlib
import datetime
import json
from telethon import Button
from orator import DatabaseManager

path = os.path.join(os.path.abspath(sys.path[0]), 'data', 'database.db')
print(path)

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': path,
        'foreign_keys': False
    }
}

db = DatabaseManager(config)

""" message.json file ichidagi so'zlarni chaqirish massiv holatida """
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'messages.json'), 'r',
          encoding='utf-8') as file:
    message = json.load(file)


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'config.json'), 'r',
          encoding='utf-8') as file:
    config = json.load(file)

class Database(object):
    def __init__(self):
        super(Database, self).__init__()
        self.db = db

    def showUserInfo(user_id):
        return db.table("users").where("user_id", "=", user_id).first()


    def InsertUser(user_id, userinfo):
        user = Database.showUserInfo(user_id)

        if str(user) == "None":
            db.table("users").insert(userinfo)
            return "done"
        Database.UpdateUserInfo(user_id, {
            'updated_at': datetime.datetime.today()
        })
        return


    def UpdateUserInfo(user_id, userinfo):
        return db.table('users').where("user_id", "=", user_id).update(userinfo)


    def UsersCount():
        return db.table("users").count()


    def AllUsers():
        return db.table('users').get()


    def showQuestionInfo(question_id):
        return db.table("questions").where("number", "=", question_id).where("active", "=", True).first()


    def showQuestionInfoActive(question_id):
        return db.table("questions").where("number", "=", question_id).first()


    def InsertQuestion(question_id, question):
        questioninfo = Database.showQuestionInfo(question_id)
        questioninfoactive = Database.showQuestionInfoActive(question_id)

        if str(questioninfo) == "None" and str(questioninfoactive) == "None":
            db.table('questions').insert(question)
            return message['test_create']

        return message['test_exists']


    def DeleteQuestion(user_id, question_id):
        return db.table("questions").where("user_id", "=", user_id).where("number", "=", question_id).update({
            'active': False
            })


    def ActiveQuestionsCount():
        return db.table("questions").where("active", "=", True).count()


    def NoActiveQuestionsCount():
        return db.table("questions").where("active", "=", False).count()

    def showAnswerInfo(user_id, question_id):
        return db.table("answers").where("user_id", "=", user_id).where("number", "=", question_id).first()


    def InsertAnswer(answer):
        return db.table('answers').insert(answer)


    def showRatingInfo(number):
        return db.table('rating').where("number", "=", number).first()


    def showRatingInfoCount(number):
        return db.table('rating').where("number", "=", number).count()


    def showRatingInfoAll(number, offset, limit):
        return db.table('rating')\
                .join("users", "users.user_id", '=', "rating.user_id")\
                .select("rating.total_score", "users.first_name", "users.last_name")\
                .where("rating.number", "=", number)\
                .order_by('rating.total_score', 'desc')\
                .offset(offset)\
                .limit(limit)\
                .get()

    def ForExportRatingInfoAll(number):
        return db.table('rating')\
                .join("users", "users.user_id", '=', "rating.user_id")\
                .select("rating.total_score", "users.first_name", "users.last_name")\
                .where("rating.number", "=", number)\
                .order_by('rating.total_score', 'desc')\
                .get()


    def showRatingInfoCount(number):
        return db.table('rating')\
                .join("users", "users.user_id", '=', "rating.user_id")\
                .select("rating.total_score", "users.first_name", "users.last_name")\
                .where("rating.number", "=", number)\
                .count()


    def InsertRating(rating):
        return db.table('rating').insert(rating)





class Helper(object):
    def __init__(self):
        super(Helper, self).__init__()

    def CheckUserActive(user_id):
        return db.table('users').where('user_id', '=', user_id).first()

    def AnswerFactory(answer, question):
        i = 0
        done = 0
        wrong = 0
        ball = 0
        text = ""

        for ans in answer:
            if ans == question['answer'][i]:
                done += 1
                ball += 1
                text += "{}.    {} ✅\n".format(i + 1, ans)
            else:
                wrong += 1
                text += "{}.    {} ❌ \n".format(i + 1, ans)

            i += 1

        button_result = [Button.inline(message['home'], data="back")]

        return {
            'button': button_result, 'text': text,
            'i': i, 'done': done, 'wrong': wrong, 'ball': ball
        }

    def the_best(number):
        if number == 1:
            return "🥇"
        elif number == 2:
            return "🥈"
        elif number == 3:
            return "🥉"
        else:
            return number


    #def Pagination():
