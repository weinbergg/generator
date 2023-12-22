from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc


def quest_list(name, theme, city):
    questions = []
    for i in range(1, 4):
        quest_text = gptGenerate(
                f'''Придумай вопрос от клиента 85-100 символов для сайта компании «{name}», которая занимается следующим видом деятельности: «{theme} в городе {city}», этот вопрос не должен содержаться в массиве (Массив может быть пустым): {questions}''')
        questions.append(quest_text)
    
    return questions



def generate_and_insert_content(name, theme, city, questions):

    ans1, ans2, ans3 = gptThreads([f'''Напиши ответ до 300 символов на вопрос '{questions[0]}' для сайта компании «{name}», которая занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                    f'''Напиши ответ до 300 символов на вопрос '{questions[1]}' для сайта компании «{name}», которая занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                    f'''Напиши ответ до 300 символов на вопрос '{questions[2]}' для сайта компании «{name}», которая занимается следующим видом деятельности: «{theme} в городе {city}»'''])


    return ans1, ans2, ans3


def quest_write(name, theme, city, path, img_pr, questions):
    ans1, ans2, ans3 = generate_and_insert_content(name, theme, city, questions)

    return ans1, ans2, ans3
