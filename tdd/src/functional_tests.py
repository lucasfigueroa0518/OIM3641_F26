from selenium import webdriver

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_list
        # can open website
        self.browser.get('http://localhost:8000')

        # sees title & header with To-Do list
        self.assertIn('Cart', self.browser.title)
        # sees textbox to enter to do

        # enter to do

        # hit enter & page update

        # enter another one

        # go home
        self.fail("Finish the test")

        if __name__ == '__main__':
            unittest.main()

browser.get('http://localhost:8000')
assert 'Congratulations!' in browser.title
print("OK")

