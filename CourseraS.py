# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


from bs4 import BeautifulSoup
import urllib.request
import re

class CScraper():
    def __init__(self, course, week):
        self.course = course
        self.week = week
        self.url = f"https://www.coursera.org/learn/{course}/discussions/weeks/{week}/?page=2"
        #self.url = f"https://www.coursera.org/learn/python-data-analysis/discussions/weeks/1/?page=2"
        self.driver = webdriver.Firefox()
        self.delay = 20
        self.postlist = []

    def load_c_url(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "emailInput_7-input")))
            print("Page is ready")
        except TimeoutException:
            print("Loading took too much time")

    def log_in(self, email, password):
        email_field = self.driver.find_element_by_name("email")
        password_field = self.driver.find_element_by_name("password")
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.submit()
        try:
            wait = WebDriverWait(self.driver, self.delay)
            username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "c-ph-username")))
            run = True
            return run
        except TimeoutException:
            print("wait for a longtime to log in")

    def extract_post_information(self, run):
        if run == True:
            try:
                # self.driver.find_elements_by_class_name("forReader")
                # rc-ThreadsListEntry blurred
                wait = WebDriverWait(self.driver, self.delay)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "forReader")))
                all_posts = self.driver.find_elements_by_class_name("rc-ThreadsListEntry")
                print(type(all_posts))
                print(len(all_posts))
                print(all_posts[0])
            except:
                print("cannot fine the posts")

            postList = []
            for post in all_posts:
                info = post.text
                info = info.split('\n')
                title = info[0]
                line2 = info[1]
                views = info[2]
                replies = info[4]
                #pattern = re.compile(r"\d+")
                #match = re.match(pattern, line2)
                #num = match.group()
                #time = line2[line.find(num):]
                #print(time)
                postMap = {"title": title, "line2": line2, "views": views, "replies": replies}
                postList.append(postMap)
            self.postlist = postList

    def flip_page(self):
        while True:
            try:
                WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(By.XPATH,"//div[contains(@class,'arrow')]"))
                button = browser.find_element_by_class_name("btn-search")
                button.click()

                #By.xpath("//div[ contains (translate(@id, '1234567890',''),'--')]")
                #"//div[contains(@class,'arrow')][contains(@aria-label,'Next')]")).click()
                #By.Xpath("//div[contains(@id, 'type-')][contains(@id, '-model')][@class='vehicle']")data-track-component="pagination_right_arrow"]').click())
                #By.Xpath("//div[contains(@class, 'arrow')][contains(@aria-label, 'Next')]")
                print("fliping page success")
                #(By.XPATH, "//div[@class ='label-text box arrow' and aria-label='Next_x0020_Page']")).c
            except TimeoutException:
                break

    def write_csv(self):
        with open("post_title.csv", "a+", encoding="utf8") as titleCSV:
            titleCSV.write("title, line2, views, replies\n")
            for i in self.postlist:
                titleCSV.write("{},{},{},{}\n".format(i["title"], i["line2"], i["views"], i["replies"]))


email = ""
password = ""
course = "python-data-analysis"
week = "1"
f = CScraper(course, week)
f.load_c_url()
# f.log_in(email, password)
#run = f.log_in(email, password)
f.log_in(email, password)
#f.extract_post_information(run)
f.flip_page()
#f.write_csv()
# print("All are run")
# f.close()
