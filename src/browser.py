from src.utils import chromeBrowserOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
import time
import re

class SimBrowser:   
    def __init__(self) -> None:
        self.init_browser()

    def init_browser(self) -> webdriver.Chrome:
        try:
            options = chromeBrowserOptions()
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            self.driver = driver
            # self.proxies = self.get_free_proxies()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize browser: {str(e)}")
    
    def set_job_indeed(self, url: str, job_title: str, location: str):
        self.driver.get(url)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="text-input-what"]').send_keys(job_title)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="text-input-where"]').send_keys(location)
        time.sleep(3)
        self.driver.find_element_by_xpath('/html/body/div').click()
        time.sleep(3)
        try:
            self.driver.find_element_by_xpath('//*[@id="jobsearch"]/button').click()
        except:
            self.driver.find_element_by_xpath('//*[@id="whatWhereFormId"]/div[3]/button').click()
        current_url = self.driver.current_url

        return current_url 
    
    def clear_text_element(self, element):
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)

    def search_job_indeed_with_button(self, job_title: str, location: str):
        base_url = "https://vn.indeed.com/"
        self.driver.get(base_url)
        input_what = self.driver.find_element("xpath", '//*[@id="text-input-what"]')
        input_where = self.driver.find_element("xpath", '//*[@id="text-input-where"]')
        submit_button = self.driver.find_element("xpath", '//*[@class="yosegi-InlineWhatWhere-primaryButton"]')
        
        self.clear_text_element(input_what)
        self.clear_text_element(input_where)

        input_what.send_keys(job_title)
        input_where.send_keys(location)
        time.sleep(3)

        submit_button.click()
        print(self.driver.current_url)
        return

    def search_job_indeed_with_query(self, job_title: str, location: str, page: int = None):
        query_url = f"https://vn.indeed.com/jobs?q={job_title}&l={location}"
        if page:
            query_url = f'{query_url}&start={(page-1)*10}'
        self.driver.get(query_url)
        return
    
    def get_job_indeed(self, maxPage:int = 1):
        print("Current URL:", self.driver.current_url)
        counter = 0
        maxPage = max(self.get_current_NumPage(), maxPage)
        listId = []
        while self.get_current_NumPage() <= maxPage:
            miniCounter = 0
            print("Current Page:", self.get_current_NumPage())
            self.driver.delete_all_cookies()
            list_job = self.driver.find_elements("xpath", '//*[@class="css-5lfssm eu4oa1w0"]')
            if not list_job:
                print("Not found jobs.")
                print(self.driver.get_cookies())
                break
            for job in list_job:
                try:
                    job.click()
                    time.sleep(3)
                    id = self.get_job_id()
                    if id in listId:
                        print("Id existed", id, listId)
                        continue
                    listId.append(id)
                    miniCounter += 1
                except Exception as e: 
                    print("Exception:", e)
                    print(self.driver.current_url)
                    pass
            print("Jobs in Page:", miniCounter)
            counter += miniCounter
            time.sleep(3)
            self.next_page_indeed(maxPage = maxPage+1)
            print("============================= New Page =================================")
        print("Jobs:", counter)
        print("ListId:", len(listId), listId)
        return

    def get_current_NumPage(self):
        current_url = self.driver.current_url
        if not re.search(r"\b&start=\d+", current_url):
            return 1
        return int(re.findall(r"\b&start=\d+", current_url)[-1][7:])//10

    def next_page_indeed(self, maxPage:int = 3):
        url = self.driver.current_url
        new_url = None
        if not re.search(r"&start=\d+&?", url):
            new_url = url + f'&start=10'
        else:
            nPage = int(re.findall(r"\b&start=\d+", url)[-1][7:])
            if nPage//10 == maxPage:
                return url
            new_url = re.sub(r"&start=\d+", f"&start={nPage + 10}", url)
        self.driver.get(new_url) 
        return new_url
    
    def previous_page_indeed(self, minPage:int = 1):
        url = self.driver.current_url
        new_url = None
        if not re.search(r"&start=\d+&?", url):
            new_url = url + f'&start=0'
        else:
            nPage = int(re.findall(r"\b&start=\d+", url)[-1][7:])
            if nPage//10 == minPage:
                return url
            new_url = re.sub(r"&start=\d+", f"&start={nPage - 10}", url)
        self.driver.get(new_url) 
        return new_url

    def get_job_id(self):
        pattern = "vjk=[a-zA-Z0-9]*"
        return re.search(pattern=pattern, string=self.driver.current_url).group()[4:]

    # Get free proxies for rotating
    def get_free_proxies(self):
        self.driver.get('https://sslproxies.org')

        table = self.driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        headers = []
        for th in thead:
            headers.append(th.text.strip())

        proxies = []
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            # for i in range(len(headers)):
            #     proxy_data[headers[i]] = tds[i].text.strip()
            proxy_data[headers[0]] = tds[0].text.strip()
            proxies.append((proxy_data['IP Address'], proxy_data['Port']))
        return proxies
