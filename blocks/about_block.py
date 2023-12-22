from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc
from functions.image import generateImage
import shutil


def about_list(name, theme, city):
    about = []
    for i in range(3):
            characteristic = gptGenerate(f'''Напиши одно преимущество из 2-4 слов, не содержащее ковычек и двоеточий, с заглавной буквы, оно не должно совпадать с другими в этом массиве характеристик (Может быть пустым): {about} . Это преимущество компании '{name}', которая занимается следующей деятельностью: "{theme} в {city}"''')
            about.append(characteristic)
    return about
    # characteristics = gptGenerate(f'''Пришли через запятую три различных преимущества из 2-4 слов, не содержащих ковычек и двоеточий, с заглавной буквы. Это преимущества компании '{name}', которая занимается следующей деятельностью: "{theme} в {city}"''')
    # ch1, ch2, ch3 = characteristics.split(', ')
    # return ch1, ch2, ch3


def about_page(path, name, theme, city):
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/about.css', path)
    soup = fc.load_html_template(f"html/templates/main_template/about.html")

    head_tag = soup.find(id="about").find(id="text")
    head_text = gptGenerate(f"создай описание в 100-150 символов компании под названием {name} для для страницы 'О нас' для сайта на тему {theme} в городе {city}. Описание должно подходить для SEO и рассказывать о команде компании")
    head_tag.string = head_text

    image_tag = soup.find('img', {'id': 'about_image'})
    if image_tag:
        image_tag['src'] = f'public/about_page.jpeg'
    else:
        print('IMAGE ABOUT')
    
    fc.save_html_template(soup, f"{path}/about.html")


def generate_and_insert_content(name, theme, city, about):

    head_about, about1, about2, about3 = gptThreads([f"создай краткое, 40-50 символов, описание компании {name} для блока 'О нас' для сайта на тему {theme} в городе {city}. Описание должно содержать кликбэйт и информацию о наилучших ценах",
                                                        f'''Сделай описание преимущества '{about[0]}' в 90-120 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным''',
                                                        f'''Сделай описание преимущества '{about[1]}' в 90-120 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным''',
                                                        f'''Сделай описание преимущества '{about[2]}' в 90-120 символов, в одном абзаце. Это преимущество компании, которая занимается следующей деятельностью: "{theme} в {city}". Описание должно быть реалистичным'''])
    

    return head_about, about1, about2, about3


def about_write(name, theme, city, path, img_lib, opt, about):
    head_about, about1, about2, about3 = generate_and_insert_content(name, theme, city, about)

    return head_about, about1, about2, about3
