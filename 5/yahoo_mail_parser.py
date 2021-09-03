from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class YahooMail:
    def __init__(self, login, password):
        chrome_options = Options()
        chrome_options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
        self.driver.get('https://login.yahoo.com')

        btn_login = self.driver.find_element_by_id('login-username')
        btn_login.send_keys(login)
        btn_login.send_keys(Keys.ENTER)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'login-passwd')))

        btn_psw = self.driver.find_element_by_id('login-passwd')
        btn_psw.send_keys(password)
        btn_psw.send_keys(Keys.ENTER)
        self.driver.get('https://mail.yahoo.com')

    def get_emails(self):
        emails = []
        emails_xpath = "//a[contains(@role, 'article')]"
        emails_info = self.driver.find_elements_by_xpath(emails_xpath)
        if len(emails_info):
            for n in range(len(emails_info)):
                WebDriverWait(self.driver, 10)\
                    .until(EC.presence_of_element_located((By.XPATH, "//ul[contains(@role, 'list')]")))
                emails_info = self.driver.find_elements_by_xpath(emails_xpath)
                email_info = emails_info[n]
                email_info.click()

                messages_xpath = "//li/div[contains(@data-test-id, 'message-view')]"
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, messages_xpath)))
                messages = self.driver.find_elements_by_xpath(messages_xpath)
                subject = self.driver.find_element_by_xpath("//span[contains(@data-test-id, "
                                                            "'message-group-subject-text')]").text
                print(len(messages))
                for message in messages:
                    email = self.__get_email_info(message, subject)
                    emails.append(email)
                self.driver.back()
            return emails
        else:
            return emails

    def __get_email_info(self, email, subject):
        return {
            'from': email.find_element_by_xpath("//span[contains(@data-test-id, 'message-from')]").text,
            'to': email.find_element_by_xpath("//span[contains(@data-test-id, 'message-to')]").text,
            'subject': subject,
            'body': email.find_element_by_xpath("//div[contains(@data-test-id, 'message-view-body')]").text
        }
