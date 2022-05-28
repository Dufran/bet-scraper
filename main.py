import time

import requests
from decouple import config
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Bet365Crawler:
    def __init__(self):
        # Get api of fingerprint
        # resp = requests.get(
        #     config("ADS_POWER_API"),
        #     {"user_id": config("ADS_POWER_USER_ID")},
        # )
        # if resp.status_code != 200:
        #     raise Exception("Ads power api not working")
        # # print(resp.json())
        # chrome_options = Options()
        # chrome_options.add_experimental_option(
        #     "debuggerAddress", resp.json()["data"]["ws"]["selenium"]
        # )
        # self.driver = webdriver.Chrome(
        #     service=Service(executable_path=resp.json()["data"]["webdriver"]),
        #     options=chrome_options,
        # )\driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        options = Options()
        # ua = UserAgent()
        # # userAgent = ua.safari
        # print(userAgent)
        # options.add_argument(f"user-agent={userAgent}")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
            },
        )
        self.start_time = time.time()
        # driver = webdriver.Chrome(chrome_options=options, executable_path=r'C:\WebDrivers\ChromeDriver\chromedriver_win32\chromedriver.exe')
        # driver.get("https://www.google.co.in")
        # driver.quit()

    def main(self):
        self.driver.get("https://www.bet365.com/#/HO/")
        self.wait = WebDriverWait(self.driver, 30)
        # time.sleep(20)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.ccm-CookieConsentPopup_Accept")
            )
        )
        cookie = self.driver.find_element(
            By.CSS_SELECTOR, value="div.ccm-CookieConsentPopup_Accept"
        )
        self.driver.execute_script("arguments[0].click();", cookie)

        sport_list = self.driver.find_elements(
            by=By.CSS_SELECTOR,
            value="div.wn-ClassificationIcon",
        )
        for sport in sport_list:
            sport_text = sport.find_element(
                By.XPATH, value="./following-sibling::span"
            ).text
            print(f"Entered {sport_text} in {(time.time() - self.start_time)} ")

            self.driver.execute_script("arguments[0].click();", sport)
            match sport_text:
                case "Футбол":
                    self.wait.until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, "div.sm-SplashModule")
                        )
                    )
                    next_categories = self.driver.find_elements(
                        By.CSS_SELECTOR,
                        "div.sm-UpComingFixturesMultipleParticipants_Region",
                    )
                    for category in next_categories:
                        self.driver.execute_script("arguments[0].click();", category)
                        print(
                            f"Entered {sport_text}-group in {(time.time() - self.start_time)} "
                        )
                        self.wait.until(
                            EC.visibility_of_element_located(
                                (By.CSS_SELECTOR, "div.sph-Breadcrumb")
                            )
                        )
                        # region expand all collapsed matches
                        collapsed_list = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            "div.suf-CompetitionMarketGroup.suf-CompetitionMarketGroup-collapsed",
                        )
                        [
                            self.driver.execute_script("arguments[0].click();", item)
                            for item in collapsed_list
                        ]
                        # endregion

                        match_list = self.driver.find_elements(
                            By.CSS_SELECTOR,
                            "div.rcl-ParticipantFixtureDetails_TeamAndScoresContainer",
                        )
                        for match in match_list:
                            print(match)
                            self.driver.execute_script("arguments[0].click();", match)
                            print(
                                f"Entered {sport_text}-group-match in {(time.time() - self.start_time)} "
                            )
                            self.wait.until(
                                EC.visibility_of_element_located(
                                    (By.CSS_SELECTOR, "div.cm-CouponModule")
                                )
                            )
                            time.sleep(20)
                            back = self.driver.find_element(
                                By.CSS_SELECTOR, "div.sph-Breadcrumb"
                            )
                            ActionChains(self.driver).move_to_element(back).perform()
                            self.driver.execute_script("arguments[0].click();", back)
                            time.sleep(10)

                case _:
                    pass


if __name__ == "__main__":
    Bet365Crawler().main()
