from argparse import ArgumentParser
from time import sleep

from selenium import webdriver


parser = ArgumentParser(description="Script for gettting III Chapter of polish mortgage register")
parser.add_argument("-cc", "--city-code",
                    help="City code for given mortgage division. E.g. 'KR1P' for Kraków")
parser.add_argument("-r", "--register-number",
                    help="Number of given register, e.g. '00220543'")
parser.add_argument("-s", "--control-sum",
                    help="Control sum for given register number, e.g. '3'")


def insert_text(xpath: str, string: str, driver: webdriver) -> None:
    """Insert text to form element specified by its xpath."""
    input_elem = driver.find_element_by_xpath(xpath)
    input_elem.send_keys(string)


def click(xpath: str, driver: webdriver) -> None:
    """Emulates clicking on element specified by its xpath"""
    elem = driver.find_element_by_xpath(xpath)
    elem.click()


def get_register_html(driver: webdriver, city_code: str, register_no: str,
                      control_no: str) -> str:
    """
    Function emulates user interaction with mortgage register website,
    resulting in getting source code for chapter III of given mortgage register.
    """
    # TODO: error handling
    API_URL = "https://przegladarka-ekw.ms.gov.pl"

    driver.get(API_URL)
    sleep(1)

    insert_text('//*[@id="kodWydzialuInput"]', city_code, driver)
    insert_text('//*[@id="numerKsiegiWieczystej"]', register_no, driver)
    insert_text('//*[@id="cyfraKontrolna"]', control_no, driver)

    click('//*[@id="wyszukaj"]', driver)
    click('//*[@id="przyciskWydrukZwykly"]', driver)
    click('/html/body/table[1]/tbody/tr/td[4]/form/input[7]', driver)
    return driver.page_source


if __name__ == "__main__":
    args = parser.parse_args()
    driver = webdriver.Firefox()
    chapter3sc = get_register_html(driver, args.city_code, args.register_number,
                                   args.control_sum)
