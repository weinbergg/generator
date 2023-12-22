import functions.functions as fc
import shutil


def policy(path, soup, adress, fio, mail):
    shutil.copy2('/root/monocreator/MonoCreatorNew/html/templates/main_template/policy.css', path)
    with open('blocks/policy.txt', 'r') as file:
        policy = file.read()

    replacements = {'https://ADRESS': adress, 'https://PRIVACY': f'{adress}/privacy', 'FIO': fio, 'MAIL': mail}
    for replacement, word in replacements.items():
        policy.replace(replacement, word)
    
    insert_soup = fc.load_html_template('blocks/policy.txt')
    tag = soup.find(id="policy_text")
    tag.append(insert_soup)
    # tag.insert(len(tag.contents), policy)

    # tag.append(policy)

def policy_page(path, adress, fio, mail):
    soup = fc.load_html_template(f"html/templates/main_template/policy.html")
    policy(path, soup, adress, fio, mail)
    fc.save_html_template(soup, f"{path}/policy.html")
