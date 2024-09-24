from src.browser import SimBrowser
from src.llm import GeminiModel



def main():
    browser = SimBrowser()
    browser.search_job_indeed_with_query('ai engineer', 'TP Hồ Chí Minh')
    browser.get_job_indeed(maxPage=5)
    # browser.get_free_proxies()
    browser.driver.quit()


if __name__ == '__main__':
    main()

