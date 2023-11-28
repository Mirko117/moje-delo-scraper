
import os
import requests as req
from bs4 import BeautifulSoup

def moje_delo():
    targeted_elements = ['div', 'a']

    if "moje_delo.html" in os.listdir("html"):
        os.remove("html/moje_delo.html")

    html = open("html/moje_delo.html", "w", encoding="utf-8")

    head = open("html/head.html", "r")
    lines = head.readlines()
    for line in lines:
        html.write(line)

    url = "https://www.mojedelo.com/prosta-delovna-mesta/vsa-podrocja/gorenjska?p=1&rid=7"
    page = req.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8-sig'), 'html.parser')
    last_page = soup.find("li", class_="PagedList-skipToLast")
    last_page = last_page.find("a")
    last_page = int(last_page.text)

    for i in range(1, last_page+1):
        print(i)
        if i != 1:
            url = f"https://www.mojedelo.com/prosta-delovna-mesta/vsa-podrocja/gorenjska?p={i}&rid=7"
            page = req.get(url)
            soup = BeautifulSoup(page.content.decode('utf-8-sig'), 'html.parser')
        jobs = soup.find_all(lambda tag: tag.name in targeted_elements and 'job-ad' in tag.get('class', []))

        for job in jobs:
            details = job.find_all("div", class_="detail")
            for detail in details:
                if detail.text == "Kranj":
                    name = job.find("h2", class_="title")
                    description = job.find("p", class_="premiumDescription")
                    links = job.find_all("a")
                    date = details[0].text
                    for link in links:
                        link = link["href"]
                        if link != "#":
                            try:
                                description = description.text
                                html.write(f"\t<p class='jobs'><a class='jobs' href='https://www.mojedelo.com{link}'>{name.text}</a></p>\n")
                                html.write(f"\t<p class='jobs'>{date}</p>\n")
                                html.write(f"\t<p class='jobs'>{description}</p><hr>\n\n")
                            except Exception as e:
                                print(e)
                                html.write(f"\t<p class='jobs'><a class='jobs' href='https://www.mojedelo.com{link}'>{name.text}</a></p>\n")
                                html.write(f"\t<p class='jobs'>{date}</p><hr>\n\n")
    html.write("</body>")
    html.close()
    print("Moje Delo is completed!")


if __name__ == "__main__":
    moje_delo()