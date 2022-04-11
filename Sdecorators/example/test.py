import Preptile as reptile


class TestReptile(reptile.BaseReptile):
    pass

if __name__ == '__main__':
    link = "https://www.englishday.cc/"
    with TestReptile(link) as Connector:
        Connector.goto()
