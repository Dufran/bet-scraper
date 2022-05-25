import time

import requests
from decouple import config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Bet365Crawler:
    def __init__(self):
        # Get api of fingerprint
        resp = requests.get(
            config("ADS_POWER_API"),
            {"user_id": config("ADS_POWER_USER_ID")},
        )
        if resp.status_code != 200:
            raise Exception("Ads power api not working")
        # print(resp.json())
        chrome_options = Options()
        chrome_options.add_experimental_option(
            "debuggerAddress", resp.json()["data"]["ws"]["selenium"]
        )
        self.driver = webdriver.Chrome(
            service=Service(executable_path=resp.json()["data"]["webdriver"]),
            options=chrome_options,
        )

    def main(self):
        self.driver.get("https://www.bet365.com/#/HO/")
        self.wait = WebDriverWait(self.driver, 30)
        sport_list = self.driver.find_elements(
            by=By.CSS_SELECTOR,
            value="div.wn-ClassificationIcon",
        )
        for sport in sport_list:
            sport_text = sport.find_element(
                By.XPATH, value="./following-sibling::span"
            ).text
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
                            self.driver.execute_script("arguments[0].click();", match)
                            time.sleep(100)
                            back = self.driver.find_element(
                                By.CSS_SELECTOR, "div.sph-Breadcrumb"
                            )
                            self.driver.execute_script("arguments[0].click();", back)

                case _:
                    pass


if __name__ == "__main__":
    Bet365Crawler().main()
