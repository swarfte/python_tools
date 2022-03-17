import Preptile as reptile


class EveryDayEnglishReptile(reptile.BaseReptile):
    def run(self):
        self.goto()
        print(self.get_element_text("#english_word_box"))
        print(self.get_element_text("#main_content_box h1 a"))


if __name__ == '__main__':
    link = "https://www.englishday.cc/" # 每日英文連結
    with EveryDayEnglishReptile(link) as Connector:
        Connector.run()