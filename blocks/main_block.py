from functions.GPT import gptThreads
import functions.functions as fc
from functions.image import generateImage


def generate_and_insert_content(name, theme, city):

    h_main, text_main = gptThreads([f'''Создай заголовок для сайта, который занимается этим направлением деятельности: {theme} в городе {city}, он должен состоять не более чем из 4 слов, без ковычек. Заголовок будет использоваться для SEO. Заголовок должен содержать кликбэйт''', f'''Напиши текст для SEO 130-150 символов, который будет раскрывать тему "{theme} в городе {city}" и основную деятельность сайта «{theme}», название компании «{name}». Он будет использовать в главном блоке на главной странице и должен привлекать покупателей. Текст должен содержать кликбэйт в начале. Приветствия не надо.'''])

    return h_main, text_main

def main_write(name, theme, city, path, img_lib, opt):
    h_main, text_main = generate_and_insert_content(name, theme, city)

    return h_main, text_main
