from functions.GPT import gptGenerate, gptThreads
import functions.functions as fc


def generate_and_insert_content(soup, works, name):

    logo_tag = soup.find(id="header").find(id="logo1")
    logo_tag.string = name
    logo_tag = soup.find(id="header").find(id="logo2")
    logo_tag.string = name
    logof_tag = soup.find(id="footer").find(id="logo")
    logof_tag.string = name
    # title_tag = soup.find(id="title")
    # title_tag.string = name

    for i in range(1, 4):
        work_tag = soup.find(id=f"header").find(id=f"header{i}")
        mobile_tag = soup.find(id=f"mobile-menu").find(id=f"header{i}")
        work_tag.string, mobile_tag.string = works[i - 1], works[i - 1]


def headers(works, path, name):
    for file in ["about.html", "index.html", "service1.html", "service2.html", "service3.html", "policy.html", "contact.html"]:
        print(file)
        soup = fc.load_html_template(f"{path}/{file}")
        generate_and_insert_content(soup, works, name)
        fc.save_html_template(soup, f"{path}/{file}")
