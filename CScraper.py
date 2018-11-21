# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import urllib.request
import re

# This class provides several methods to help with getting post title from a Coursera class forum
class CScraper():
    def __init__(self, course, week):
        self.course = course
        self.week = week
        self.baseurl = f"https://www.coursera.org/learn/{course}/discussions/weeks/{week}/"
        self.driver = webdriver.Firefox()
        self.delay = 20
        self.postBlueMap = {}

# return the base URL of the forum
    def baseurl(self):
        return self.baseurl

# return a dictionary that contains the post titles of the papges
    def bigMap(self):
        return self.postBlueMap

#  shut down the web driver instance or destroy the web driver instance(Close all the windows).
    def quit(self):
        self.driver.quit()

# given a url and load the page
# input: page, the url of a page, a string
# function: load the page with the input url
# return: a boolean True,if the page is load successfully
    def load_one_url(self, page):
        loaded = False
        try:
            self.driver.get(page)
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "rendered-content")))
            print(page[:6] + "Page is ready")
            loaded = True
        except TimeoutException:
            print("Loading took too much time")
        return loaded
# given the base url and the page range generate a list of url string
# input: minPage, int, the minimum page number; maxPage, int, the minimum page number
# return: a list of url strings
    def url_generator(self, minPage=1, maxPage=15):
        urlList = []
        for i in range(minPage, maxPage + 1):
            iurl = self.baseurl + "?page=" + str(i)
            urlList.append(iurl)
        return urlList

# given email and password, log in to a given page
# input: email, string, the email user name; password, string, the password for log in
# return: a boolean, true if the login the successful
    def login(self, email, password):
        logined = False
        wait = WebDriverWait(self.driver, self.delay)
        wait.until(EC.presence_of_element_located((By.ID, "emailInput_7-input")))
        email_field = self.driver.find_element_by_name("email")
        password_field = self.driver.find_element_by_name("password")
        email_field.send_keys(email)
        password_field.send_keys(password)
        password_field.submit()
        try:
            wait = WebDriverWait(self.driver, self.delay)
            username = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "c-ph-username")))
            logined = True
        except TimeoutException:
            print("wait for a longtime to log in")
        return logined

# given a loaded page, extract the titles of the posts.
    # save all information in a dictionary, please all bigMap() to return the information in the map
# input: pageReady, boolean, true if a page is loaded and ready for extracting information
    # url: string, the url of the page that is extracted information from
# return: void
    def extract_post_information(self, pageReady,url):
        if pageReady == True:
            try:
                # self.driver.find_elements_by_class_name("forReader")
                # rc-ThreadsListEntry blurred
                wait = WebDriverWait(self.driver, self.delay)
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "forReader")))
                all_posts = self.driver.find_elements_by_class_name("rc-ThreadsListEntry")
                print(type(all_posts))
                print(len(all_posts))
                print(all_posts[0])
                if len(all_posts) != 0:
                    infoExtracted = True
                postList = []
                for post in all_posts:
                    info = post.text
                    info = info.split('\n')
                    title = info[0]
                    line2 = info[1]
                    views = info[2]
                    replies = info[4]
                    postMap = {"title": title, "line2": line2, "views": views, "replies": replies}
                    print(postMap["title"], postMap["line2"], postMap["views"], postMap["replies"])
                    postList.append(postMap)
                    print(len(postList))
                self.postBlueMap[url] = postList
            except:
                print("cannot fine the posts")

# write all the post information from the big dictionary in to a CSV file named "post_title.csv"
# input: none
# return: void
    def write_csv(self):
        try:
            with open("post_title.csv", "a+", encoding="utf8") as titleCSV:
                titleCSV.write("title, line2, views, replies\n")
                map = self.postBlueMap
                for i in map.keys():
                    try:
                        titleCSV.write(i + "\n")
                    except:
                        continue
                    for j in map[i]:
                        try:
                            titleCSV.write("{},{},{},{}\n".format(j["title"], j["line2"], j["views"], j["replies"]))
                        except:
                            continue
        except:
            print("CSV write in fail")


if __name__ == '__main__':
    email = ""
    password = ""
    course = "python-data-analysis"
    week = "1"
    f = CScraper(course, week)
    baseUrlLoaded = f.load_one_url(f.baseurl)
    loginSucess = f.login(email, password)
    print(loginSucess)
    if loginSucess:
        urlList = f.url_generator()
        for eachUrl in urlList:
            pageLoaded = f.load_one_url(page=eachUrl)
            f.extract_post_information(pageLoaded, eachUrl)
    bigMap = f.bigMap()
    for item in bigMap.keys():
        print(bigMap[item])
    f.write_csv()
    f.quit()








