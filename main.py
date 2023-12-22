import os
import traceback
import time
import shutil
import sys
import functions.functions as fc
from functions.image import threads_image, generateImage
from functions.GPT import gptGenerate, gptThreads
from functions.sql import finisher, create_database, img_insert, get_id_number
from functions.threads import threads_tags
from dotenv import load_dotenv
from blocks.main_block import main_write
from blocks.about_block import about_write, about_page, about_list
from blocks.works_block import works_write, work_page, works_list
from blocks.advantages import advantages_write
from blocks.examples import examples_write
from blocks.process import process_write
from blocks.questions import quest_write, quest_list
from blocks.reactions import react_write
from blocks.header_block import headers
from blocks.policy import policy_page
from blocks.contact_page import contact_page
import concurrent.futures
from bot import send_telegram_message
from bs4 import BeautifulSoup as bs


base_names = ["main", "about", "works", "advantages", "process", "reactions", "examples", "questions"]


def archive_folder(path, path_name):
    backup_archive = os.path.join('/root/monocreator/results', path_name)

    shutil.make_archive(backup_archive, 'zip', path)


def yield_function():
    massages = ['Генерирую изображения основной страницы', 'Генерирую изображения услуг', "Генерирую изображения страницы 'О нас'", "Заполняю страницу 'О нас'", "Заполняю страницы услуг"]
    for massage in massages:
        yield massage
        time.sleep(10)


def index(city, name, theme, opt, design, host_opt):
    start = time.time()
    wd = os.getcwd()
    os.path.dirname(wd)
    path_name = f'{get_id_number()}'
    path = f"/root/monocreator/results/{path_name}"
    print(path)
    os.mkdir(path)
    img_lib = path + "/public/"
    os.mkdir(img_lib)
    shutil.copytree(f"{wd}/html/templates/main_template/public", img_lib, dirs_exist_ok=True)

    if opt == "GPT":
        img_pr = 0.0406
    else:
        img_pr = 0.023

    dollar = fc.get_dollar()

    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/index.html', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/style.css', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/index.css', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/postcss.config.js', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/package.json', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/tailwind.config.js', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/404.html', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/404.css', path)
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/.htaccess', path)


    source_folder = f"{wd}/html/templates/main_template/components"
    destination_folder = path + "/components"
    shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

    source_folder = f"{wd}/html/templates/main_template/public"
    shutil.copytree(source_folder, img_lib, dirs_exist_ok=True)

    # source_folder = f"{wd}/html/templates/{design}/css"
    # destination_folder = path + "/css"
    # shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

    # source_folder = f"{wd}/html/php"
    # destination_folder = path + "/php"
    # shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)

    check =  gptGenerate(f'''«Проверь данные "{city}, {name}, {theme}" на релевантность, если тут нецензурный запрос или набор бессмысленных символов, то напиши «FALSE», если всё хорошо, то напиши «TRUE».''')
        
    if check == "FALSE":
        yield 'Некорректные данные'
        sys.exit(1)

    try:
        yield "Создаю базу данных"
        create_database(path, base_names)
        img_insert(path, img_pr, dollar)


        yield "Генерирую основную страницу"    
        for word in [name, theme, city]:
            if word.strip() != '':
                word = word.replace('#', '') #.replace('/', '').replace(':', '')
            else:
                yield "Пусто"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(works_list, name, theme, city)
            future2 = executor.submit(about_list, name, theme, city)
            # future3 = executor.submit(quest_list, name, theme, city)
        
            works = future1.result()
            about = future2.result()
            # questions = future3.result()

        print(time.time() - start)

        work_text1, work_text2, work_text3, text_for_prompt, w1_prompt, w2_prompt, w3_prompt, about1_prompt, about2_prompt, about3_prompt, contact_prompt  = gptThreads([f'''Опиши в один абзац 90-120 символов услугу под названием "{works[0]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                                                                                                            f'''Опиши в один абзац 90-120 символов услугу под названием "{works[1]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                                                                                                            f'''Опиши в один абзац 90-120 символов услугу под названием "{works[2]}" для сайта, который занимается следующим видом деятельности: «{theme} в городе {city}»''',
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото для сайта компании, занимающейся следующей деятельностью: '{theme}'. обязательно укажи в промпте деятельность компании. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно изображать следующую услугу компании: '{works[0]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно изображать следующую услугу компании: '{works[1]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно изображать следующую услугу компании: '{works[2]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно отображать следующую характеристику компании: '{about[0]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно отображать следующую характеристику компании: '{about[1]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото должно отображать следующую характеристику компании: '{about[2]}', компания занимается следующей деятельностью: '{theme}. обязательно укажи в промпте деятельность компании. если в промпте упомянаются люди, укажи. что они должны быть с европейцами. промпт пришли на английском языке",
                                                                                                                            f"напиши промпт 20-25 символов для нейросити, генерирующей изображения. обязательно укажи, что необходимо получить «фотографию», «реалистичное изображение» или «фотореалистичный стиль» без текста на самой фотографии, используй термины «снимок» или «кадр». фото для раздела 'контакты' сайта компании, занимающейся следующей деятельностью: '{theme}'. обязательно укажи в промпте деятельность компании. промпт пришли на английском языке"])


        # text_for_prompt, w1_prompt, w2_prompt, w3_prompt, about1_prompt, about2_prompt, about3_prompt = f"photo of {fc.translate(theme)}", f"photo of {fc.translate(works[0])}", f"photo of {fc.translate(works[1])}", f"photo of {fc.translate(works[2])}", f"photo of {fc.translate(about[0])}", f"photo of {fc.translate(about[1])}", f"photo of {fc.translate(about[2])}"

        print(time.time() - start)
        # yield "Генерирую изображения"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            yield from yield_function()
            future1 = executor.submit(main_write, name, theme, city, path, img_lib, opt)
            future2 = executor.submit(about_write, name, theme, city, path, img_lib, opt, about)
            # future3 = executor.submit(works_write, name, theme, city, path, img_lib, opt, works, work_text1, work_text2, work_text3)
            future4 = executor.submit(advantages_write, name, theme, city, path, img_lib, opt, about)
            future5 = executor.submit(process_write, name, theme, city, path, img_lib, opt)
            future6 = executor.submit(react_write, name, theme, city, path, img_lib, opt)
            future7 = executor.submit(examples_write, name, theme, city, path, img_lib, opt, works)

            future8 = executor.submit(generateImage, w1_prompt, img_lib, f'service1', 'GPT')
            future9 = executor.submit(generateImage, w2_prompt, img_lib, f'service2', 'GPT')
            future10 = executor.submit(generateImage, w3_prompt, img_lib, f'service3', 'GPT')
            future11 = executor.submit(generateImage, text_for_prompt, img_lib, f'main', 'GPT')
            future12 = executor.submit(generateImage, text_for_prompt, img_lib, f'about', 'GPT')
            future13 = executor.submit(generateImage, text_for_prompt, img_lib, f'about_page', 'GPT')
            future14 = executor.submit(generateImage, text_for_prompt, img_lib, f'advantages', 'GPT')
            future15 = executor.submit(generateImage, text_for_prompt, img_lib, f'process', 'GPT')
            future16 = executor.submit(generateImage, about1_prompt, img_lib, f'about1', 'GPT')
            future17 = executor.submit(generateImage, about2_prompt, img_lib, f'about2', 'GPT')
            future18 = executor.submit(generateImage, about3_prompt, img_lib, f'about3', 'GPT')
            future19 = executor.submit(generateImage, w1_prompt, img_lib, f'example1', 'GPT')
            future20 = executor.submit(generateImage, w2_prompt, img_lib, f'example2', 'GPT')
            future21 = executor.submit(generateImage, w3_prompt, img_lib, f'example3', 'GPT')
            future22 = executor.submit(generateImage, contact_prompt, img_lib, 'contact', 'GPT') #f"photo for contact page of website about {fc.translate(theme)}", img_lib, f'contact'
            # future23 = executor.submit(generateImage, f"photo of workers of {fc.translate(theme)} service", img_lib, f'join', 'GPT')
            # future8 = executor.submit(quest_write, name, theme, city, path, img_pr, questions)

            future24 = executor.submit(work_page, 1, path, works[0], work_text1, name, theme, city)
            future25 = executor.submit(work_page, 2, path, works[1], work_text2, name, theme, city)
            future26 = executor.submit(work_page, 3, path, works[2], work_text3, name, theme, city)
            future27 = executor.submit(contact_page, path, name, theme, '+790000000000', 'gaspom@mail.ru', 'Пенза')
            future28 = executor.submit(policy_page, path, 'http://site.com', 'Петров Иван', 'gaspom@mail.ru')
            future29 = executor.submit(about_page, path, name, theme, city)
            # future30 = yield_function()


            h_main, h_text = future1.result()
            head_about, about1, about2, about3 = future2.result()
            # work_text1, work_text2, work_text3 = future3.result()
            head_advant, advantage1, advantage2, advantage3 = future4.result()
            step1, step2, step3, step1_text, step2_text, step3_text = future5.result()
            react_text1, react_text2, react_text3 = future6.result()
            example1, example2, example3 = future7.result()
            future8.result()
            future9.result()
            future10.result()
            future11.result()
            future12.result()
            future13.result()
            future14.result()
            future15.result()
            future16.result()
            future17.result()
            future18.result()
            future19.result()
            future20.result()
            future21.result()
            future22.result()
            # future23.result()
            future24.result()
            future25.result()
            future26.result()
            future27.result()
            future28.result()
            future29.result()
            # yield future30.result()
            # ans1, ans2, ans3 = future8.result()

        print(time.time() - start)

        yield "Заполняю последнюю страницу"

        threads_tags(path, name, theme, city, works, about, 
                        h_main, h_text, head_about, about1, about2, about3, 
                        work_text1, work_text2, work_text3, head_advant, 
                        advantage1, advantage2, advantage3, step1, step2, step3, step1_text, step2_text, step3_text,
                        react_text1, react_text2, react_text3,
                        example1, example2, example3)
        
        print(time.time() - start)

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     # future1 = executor.submit(contact_page, path, name, theme, '+790000000000', 'gaspom@mail.ru', 'Пенза')
        #     # future2 = executor.submit(policy_page, path, 'Пенза', 'Петров Иван', 'gaspom@mail.ru')
        #     # # future3 = executor.submit(work_page, 1, path, works[0], work_text1, name, theme, city)
        #     # # future4 = executor.submit(work_page, 2, path, works[1], work_text2, name, theme, city)
        #     # # future5 = executor.submit(work_page, 3, path, works[2], work_text3, name, theme, city)
        #     # future6 = executor.submit(about_page, path, name, theme, city) 

        #     future7 = executor.submit(threads_tags, path, name, theme, city, works, about, 
        #                                             h_main, h_text, head_about, about1, about2, about3, 
        #                                             work_text1, work_text2, work_text3, head_advant, 
        #                                             advantage1, advantage2, advantage3, step1, step2, step3, step1_text, step2_text, step3_text,
        #                                             react_text1, react_text2, react_text3,
        #                                             example1, example2, example3)
        #     # future8 = executor.submit(headers, works, path, name) 
        
        #     # future1.result()
        #     # future2.result()
        #     # future3.result()
        #     # future4.result()
        #     # future5.result()
        #     # future6.result()
        #     future7.result()
        #     # future8.result()
            
        headers(works, path, name)

        print(time.time() - start)

        # yield "Генерирую изображения"
        # with concurrent.futures.ThreadPoolExecutor() as executor:            
        #     future1 = executor.submit(generateImage, w1_prompt, img_lib, f'service1', 'GPT')
        #     future2 = executor.submit(generateImage, w2_prompt, img_lib, f'service2', 'GPT')
        #     future3 = executor.submit(generateImage, w3_prompt, img_lib, f'service3', 'GPT')
        #     future4 = executor.submit(generateImage, text_for_prompt, img_lib, f'main', 'GPT')
        #     future5 = executor.submit(generateImage, text_for_prompt, img_lib, f'about', 'GPT')
        #     future5 = executor.submit(generateImage, text_for_prompt, img_lib, f'about_page', 'GPT')
        #     future6 = executor.submit(generateImage, text_for_prompt, img_lib, f'advantages', 'GPT')
        #     future7 = executor.submit(generateImage, text_for_prompt, img_lib, f'process', 'GPT')
        #     future8 = executor.submit(generateImage, about1_prompt, img_lib, f'about1', 'GPT')
        #     future9 = executor.submit(generateImage, about2_prompt, img_lib, f'about2', 'GPT')
        #     future10 = executor.submit(generateImage, about3_prompt, img_lib, f'about3', 'GPT')
        #     future11 = executor.submit(generateImage, w1_prompt, img_lib, f'example1', 'GPT')
        #     future12 = executor.submit(generateImage, w2_prompt, img_lib, f'example2', 'GPT')
        #     future13 = executor.submit(generateImage, w3_prompt, img_lib, f'example3', 'GPT')
        #     future14 = executor.submit(generateImage, f"photo for contact page of website about {fc.translate(theme)}", img_lib, f'contact', 'GPT')
        #     future15 = executor.submit(generateImage, f"photo of workers of {fc.translate(theme)} service", img_lib, f'join', 'GPT')

        #     future1.result()
        #     future2.result()
        #     future3.result()
        #     future4.result()
        #     future5.result()
        #     future6.result()
        #     future7.result()
        #     future8.result()
        #     future9.result()
        #     future10.result()
        #     future11.result()
        #     future12.result()
        #     future13.result()
        #     future14.result()
        #     future15.result()

        # print(time.time() - start)

        yield "Сохраняю ваш архив"
        archive_folder(path, path_name)

        yield "Выгружаю на сервер"
        os.chmod(f'/root/monocreator/results/{path_name}.zip', 0o777)


        load_dotenv()
        if host_opt == "dev":
            host = os.getenv("host_dev")
            log = os.getenv("log_dev")
            password = os.getenv("password_dev")  
            host_path = os.getenv("dev_path") 
        else:
            host = os.getenv("host_prod")
            log = os.getenv("log_prod")
            password = os.getenv("password_prod") 
            host_path = os.getenv("prod_path")

        fc.send_host(host, log, password, f'/root/monocreator/results/{path_name}.zip', f'/sites/{path_name}.zip', path_name)
        fc.unzip_on_hosting(host, log, password, f'/{host_path}/{path_name}.zip', f'/{host_path}/{path_name}')
        os.remove(f'/root/monocreator/results/{path_name}.zip')


        end = time.time() - start
        price = finisher(path, base_names, end, dollar)
        print(end, price, sep="\n")
        print(f"Время: {end}; Стоимость: {price} RUB")
        html_string = (
            f"Город: {city}<br>"
            f"Название: {name}<br>"
            f"Направление работы: {theme}<br>"
            f"Длительность генерации: {int(end)} секунд<br>"
            f"Стоимость генерации: {int(price)} рублей<br>"
            f"<div style='margin-top: 30px;'><button class=\"button-zip\" onclick=\"location.href='/sites/{path_name}.zip'\" type=\"button\">Скачать архив с сайтом</button></div>"
            f"<div style='margin-top: 30px;'><button class=\"button-zip\" onclick=\"window.open('/sites/{path_name}/index.html', '_blank')\" type=\"button\">Открыть сайт в новой вкладке</button></div>"
            f"<button type='button' id='create-new-site-button' style='margin-top:45px;' onclick='createNewSite()'>Создать новый сайт</button>"
        )

        yield html_string

    except Exception as e:
        # bot_token = os.getenv("bot_token")
        # chat_id = os.getenv("chat_id")
        # send_telegram_message(bot_token, chat_id, f"Ошибка на сервере prod: {e}")

        traceback.print_exc()
        print("Error:", e)
        print("Ошибка в main")
        yield("Server Error")
    # #     os.remove(path)
    # #     return "An error occurred, directory removed"

    yield "done"  # Отправляем сообщение о завершении
