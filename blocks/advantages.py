from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc
from functions.image import generateImage


def generate_and_insert_content(name, theme, city, about):

    head_advant, advantage1, advantage2, advantage3 = gptThreads([f"создай краткое, 25-30 символов, описание компании {name} для блока 'О нас' для сайта на тему {theme} в городе {city}. Описание должно содержать кликбэйт и информацию о наилучших ценах",
                                                        f'''Сделай описание преимущества '{about[0]}' от 45 до 50 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным''',
                                                        f'''Сделай описание преимущества '{about[1]}' от 45 до 50 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным''',
                                                        f'''Сделай описание преимущества '{about[2]}' от 45 до 50 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным'''])

    return head_advant, advantage1, advantage2, advantage3


def advantages_write(name, theme, city, path, img_lib, opt, about):
    head_advant, advantage1, advantage2, advantage3 = generate_and_insert_content(name, theme, city, about)

    return head_advant, advantage1, advantage2, advantage3
