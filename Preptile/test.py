import Preptile as reptile


class TestReptile(reptile.BaseReptile):
    def run(self):
        self.goto()
        print(self.querySelectorEval("li a", self.property["text"]))
        print(self.querySelectorEval("li a", self.property["href"]))


if __name__ == '__main__':
    with TestReptile("http://www.jornalvakio.com/NewsCategory/view/id/12") as Connector:
        Connector.run()
