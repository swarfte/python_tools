import Preptile as reptile


class TestReptile(reptile.BaseReptile):
    def run(self):
        self.goto()
        self.sleep()
        print(type(self.content()))

if __name__ == '__main__':
    with TestReptile("http://www.vakiodigital.com/login") as Connector:
        Connector.run()
