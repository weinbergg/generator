from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc
from functions.image import generateImage
import shutil
from bs4 import BeautifulSoup as bs



def works_list(name, theme, city):
    works = []
    for i in range(1, 4):
        work = gptGenerate(f'''Напиши одну услугу (услуга должна быть не вымышленной, а реально оказывающейся и распространненой в подобных по деятельности компаниях) на русском языке для компании, которая занимается следующим видом деятельность: «{theme}». Название должно быть максимум до 15 символов. услуга не должна содержаться в списке (Может быть пустым): {works}".''')
        works.append(work)
    return works
    # works = gptGenerate(f'''Пришли три услуги через запятые, оказываемые компанией, занимающейся следующей деятельностью: {theme}. услуги должна быть не вымышленными, а реально оказываемыми и распространными в подобных по деятельности компаниях. например для клининга: Поддерживающая уборка, Генеральная уборка, Уборка офиса''')
    # work1, work2, work3 =  works.split(', ')

    # return work1, work2, work3



def work_page(i, path, work_name, work_text, name, theme, city):
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/service.css', path)
    soup = fc.load_html_template("html/templates/main_template/service.html")

    try:
        title_tag, title_tag1 = soup.find(id="work").find(id="name"), soup.find(id="work").find(id="name1")
        title_tag.string, title_tag1.string = work_name, work_name

        short_tag = soup.find(id="work").find(id="short_text")
        short_text = gptGenerate(f'''Напиши текст на 150 символов, описывающий услугу под названием "{work_name}"''')
        short_tag.string = short_text 

        text_tag = soup.find(id="work").find(id="work_text")
        print('WORK')
        work_text = gptGenerate(f'''Заполни html код SEO текстом (общая длина 1000-1200 символов), описывающим услугу под названием "{work_name}", компания занимается следующим видом деятельности «{theme} в городе {city}», название компании: «{name}». В ответе пришли только данный заполненный код html без коментариев и ковычек
        ///<div class="">
        <h1 class="page-text15-h1 margin20"></h1>
        <p class="page-text16 margin20"></p>
        <p class="page-text16 margin20"></p>
        <h2 class="page-text15-h2 margin20"></h2>
        <p class="page-text16 margin20"></p>
        <p class="page-text16 margin20"></p>
        <h2 class="page-text15-h2 margin20">/h2>
        <ul>
        <li class="page-text16 margin20"></li>
        <li class="page-text16 margin20"></li>
        <li class="page-text16 margin20"></li>
        </ul>
        <h2 class="page-text15-h2"></h2>
        <p class="page-text16 margin20"></p>
        <p class="page-text16 margin20"></p>
        </div>///''', "gpt-3.5-turbo") #f'''Пришли SEO текст в html разметке, описывающий услугу под названием "{work_name}", компания занимается следующим видом деятельности «{theme} в городе {city}», название компании: «{name}». пришли только содержимое тэга <body> полностью, без пропусков и комментариев и ковычек в начале и конце, в тэги <div> вставь class="page-text16 Body", в тэг h1 добавь class="page-text15"'''

        insert_soup = bs(work_text, "html.parser")
        text_tag.append(insert_soup)
        # text_tag.string = work_text

        image_tag = soup.find('img', {'id': 'work_image'})
        image_tag1 = soup.find('img', {'id': 'work_image1'})
        if image_tag:
            image_tag['src'] = f'public/service{i}.jpeg'
            image_tag1['src'] = f'public/example{i}.jpeg'
        else:
            print('IMAGE work')
    except Exception as e:
        print('process error:',str(e))
    
    fc.save_html_template(soup, f"{path}/service{i}.html")


def generate_and_insert_content(name, theme, city, opt, img_lib, path, works, work_text1, work_text2, work_text3):

    # work_text1, work_text2, work_text3 = gptThreads([f'''Опиши в один абзац 35-40 символов услугу под названием "{works[0]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
    #                                                     f'''Опиши в один абзац 35-40 символов услугу под названием "{works[1]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
    #                                                     f'''Опиши в один абзац 35-40 символов услугу под названием "{works[2]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»'''])

    return work_text1, work_text2, work_text3
    

def works_write(name, theme, city, path, img_lib, opt, works, work_text1, work_text2, work_text3):
    generate_and_insert_content(name, theme, city, opt, img_lib, path, works, work_text1, work_text2, work_text3)

    # return work_text1, work_text2, work_text3
    
