from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc
from functions.image import generateImage


def generate_and_insert_content(name, theme, city, opt, img_lib, works):

    example1, example2, example3 = gptThreads([f'''Опиши в один абзац 90-120 символов реальный пример оказания клиенту услуги под названием "{works[0]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                                        f'''Опиши в один абзац 90-120 символов реальный пример оказания клиенту услуги под названием "{works[1]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                                        f'''Опиши в один абзац 90-120 символов реальный пример оказания клиенту услуги под названием "{works[2]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»'''])
    
    
    return example1, example2, example3


def examples_write(name, theme, city, path, img_lib, opt, works):
    example1, example2, example3 = generate_and_insert_content(name, theme, city, opt, img_lib, works)

    return example1, example2, example3


