import functions.functions as fc
from functions.GPT import gptGenerate
import shutil

def contact_page(path, name, theme, phone, mail, adress):
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/contact.css', path)
    soup = fc.load_html_template(f"html/templates/main_template/contact.html")

    tag = soup.find(id="text")
    text = gptGenerate(f"создай текст 200 символов для страницы 'Контакты' сайта компании под названием {name}, которая занимается следующей деятельностью: '{theme}'")
    tag.string = text

    # generateImage(fc.translate(theme), img_lib, "about_page", opt)
    # image_tag = soup.find('div', {'id': 'about_image'})
    # if image_tag:
    #     image_tag['src'] = f'images/about_page.jpeg'
    # else:
    #     print('IMAGE FAILED')
    
    fc.save_html_template(soup, f"{path}/contact.html")