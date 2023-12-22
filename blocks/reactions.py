from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc
from functions.image import generateImage


def generate_and_insert_content(name, theme, city):

    react1, react2, react3 = gptThreads([f"напиши короткий, 15-20 слов, отзыв для сайта под названием {name} на тему {theme} в городе {city}. отзыв должен содержать кликбэйт и быть реалистичным",
                                                                    f"напиши короткий, 15-20 слов, отзыв для сайта под названием {name} на тему {theme} в городе {city}. отзыв должен содержать кликбэйт и быть реалистичным",
                                                                    f"напиши короткий, 15-20 слов, отзыв для сайта под названием {name} на тему {theme} в городе {city}. отзыв должен содержать кликбэйт и быть реалистичным"])
    

    return react1, react2, react3


def react_write(name, theme, city, path, img_lib, opt):
    react1, react2, react3 = generate_and_insert_content(name, theme, city)

    return react1, react2, react3
