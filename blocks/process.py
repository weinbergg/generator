from functions.GPT import gptGenerate, gptThreads
# import functions.functions as fc
# from functions.image import generateImage
from bs4 import BeautifulSoup as bs

    


def generate_and_insert_content(name, theme, city):
    data_about = []

    # text_process = gptGenerate(f"Напиши текст в html-разметке, который разделяется новыми строчками. Надо написать этапы работы для компании, которая занимается этой деятельностью: {theme}. 3 пункта, образцы этапов: «1 этап - Оставьте заявку на сайте. 2 этап - Наш менеджер свяжется с вами…». Каждый этап это заголовок, а всё после дефиса - описание снизу. Нужно написать только html разметку которая используется внутри body не считая body. Для этапов используй h3. Для описания этапа p. не помещай ответ в ковычки и не подписывай его как html")

    step1, step2, step3 = "Оставьте заявку на сайте", "Наш менеджер свяжется с вами", gptGenerate(f"составь заголовок для этапа связи с клиентом для сайта компании, занимающейся следующей деятельностью: {theme}. образец заголовка: 'получение услуги'")
    step1_text, step2_text, step3_text = gptThreads([f"подробнее в 60-70  символов опиши следующий этам взаимодействия с клиентом с точки зрения клиента: {step1}", f"подробнее в 25-40 символов опиши следующий этам взаимодействия с клиентом с точки зрения клиента: {step2}", f"подробнее в 25-40 символов опиши следующий этам взаимодействия с клиентом с точки зрения клиента: {step3}"])
    # Напиши текст в html-разметке, который разделяется новыми строчками. 
    # Надо написать этапы работы для компании, которая занимается этой деятельностью: {theme}. 
    # 3 пункта, образцы этапов: «1 этап - Оставьте заявку на сайте. 
    #                           2 этап - Наш менеджер свяжется с вами…». Каждый этап это заголовок, а всё после дефиса - описание снизу. Нужно написать только html разметку которая используется внутри body не считая body. Для этапов используй h3. Для описания этапа p. не помещай ответ в ковычки и не подписывай его как html"

    return step1, step2, step3, step1_text, step2_text, step3_text


def process_write(name, theme, city, path, img_lib, opt):
    step1, step2, step3, step1_text, step2_text, step3_text = generate_and_insert_content(name, theme, city)

    return step1, step2, step3, step1_text, step2_text, step3_text

