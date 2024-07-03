from pathlib import Path

from bs4 import BeautifulSoup

from base_classes.base_test_scraper import TestScraper
from base_classes.test_types import Types


class CorruptionTestScraper(TestScraper):
    def add_answers_from_file(self, source_filename: str | Path):
        html = self.get_html_from_file(source_filename)
        soup = BeautifulSoup(html, "html.parser")

        divs = soup.find_all("div", id=lambda x: x and x.startswith("question-"))
        for div in divs:
            question = div.find("div", class_="qtext").get_text()

            options = []
            corrects = []
            if div.get("class")[1] == "match":
                type = Types.select
                for row in div.find_all("tr"):
                    options.append(row.find("td", class_="text").get_text())
                    corrects.append(row.find("option", selected="selected").get_text())
            else:
                answer_div = div.find("div", class_="answer")
                type = answer_div.find("input").get("type")
                for row in answer_div.find_all(
                    "div", class_=lambda x: x and x.startswith("r")
                ):
                    options.append(row.get_text())
                    corrects.append(row.find("input").get("checked") == "checked")

            solved = div.find("div", class_="grade").get_text() == "Балів 1,00 з 1,00"

            self.add_question(question, type, options, corrects, solved)

        self.dump_answers()
        self.write_answers_to_html()


if __name__ == "__main__":
    folder = Path(
        "/home/vskesha/downloads/Навчання УЗ/Антикорупційна програма липень 2024"
    )
    answers_html = folder / "answers.html"
    answers_json = folder / "answers.json"

    cts = CorruptionTestScraper(answers_html, answers_json)

    attempts = folder / "спроби"
    source_htmls = [
        # "Болюх М.В..html",
        # "Болюх В.М.2.html",
        # "Тимчишин Н.В..html",
        # "Стадарська Л.Г..html",
        # "Долгова М.М..html",
        # "Музика В.М..html",
        # "Крамар І.М..html",
        # "Адамик О.М..html",
        "Ковальчук О.В..html",
    ]

    for source_html in source_htmls:
        cts.add_answers_from_file(attempts / source_html)
