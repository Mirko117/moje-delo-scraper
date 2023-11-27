import os
import requests as req
from bs4 import BeautifulSoup


def deloglasnik():
    if "deloglasnik.html" in os.listdir("html"):
        os.remove("html/deloglasnik.html")
    
    html = open("html/deloglsnik.html", "w", encoding="utf-8")

    head = open("html/head.html", "r")
    lines = head.readlines()
    for line in lines:
        html.write(line)

    url = "https://www.deloglasnik.si/Iskanje-zaposlitve/?searchWord=&keyword=&job_title=&job_title_id=&area=10&category=&page=1"
    page = req.get(url)
    soup = BeautifulSoup(page.content.decode('utf-8-sig'), 'html.parser')

    page_count = soup.find("ul", class_="page-count")
    numbers = page_count.find_all("li", class_=None)

    last_page = 1
    for number in numbers:
        page = int(number.text)
        if page > last_page:
            last_page = page
    
    for i in range(1, last_page+1):
        print(i)
        if i != 1:
            url = f"https://www.deloglasnik.si/Iskanje-zaposlitve/?searchWord=&keyword=&job_title=&job_title_id=&area=10&category=&page={i}"
            page = req.get(url)
            soup = BeautifulSoup(page.content.decode('utf-8-sig'), 'html.parser')
        jobs = soup.find_all("div", class_="job")

        for job in jobs:
            location = job.find("p", class_="job-location")
            if location.text == "Kranj":
                name = job.find("p", class_="job-title")
                link = name.find("a", class_=None)
                link = link["href"]
                date = job.find("p", class_="deadline")
                description = job.find("p", class_="intro-txt")
                try:
                    description = description.text
                    html.write(f"\t<p class='jobs'><a class='jobs' href='{link}'>{(name.text).strip()}</a></p>\n\t<p class='jobs'>{date.text}</p>\n\t<p class='jobs'>{description}</p><hr>\n\n")
                except Exception as e:
                    print(e)
                    html.write(f"\t<p class='jobs'><a class='jobs' href='{link}'>{(name.text).strip()}</a></p>\n\t<p class='jobs'>{date.text}</p><hr>\n\n")
    html.write("</body>")
    html.close()
    print("Deloglasnik is completed!")


if __name__ == "__main__":
    deloglasnik()