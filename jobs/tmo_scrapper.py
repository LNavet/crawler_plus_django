#!/usr/bin/python
# Author: Luis Navarrete
# Version: 1.0

import pathlib
import re
from os import path
from time import sleep
from abc import abstractmethod

import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from django.db.utils import IntegrityError
from mangas.models import Chapter
from mangas.models import Manga
from mangas.models import Update


class Driver:
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __init__(self) -> None:
        """Initialize the options for the driver"""
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36"
        )
        self.driver = uc.Chrome(options=chrome_options)

    def __new__(cls):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Driver, cls).__new__(cls)
        return cls.instance


class ContentExtractorInterface:

    @abstractmethod
    def extract_content(self, elements: list[WebElement]):
        return NotImplementedError

    @abstractmethod
    def start_extraction(self):
        return NotImplementedError


class TMOExtractorContent(ContentExtractorInterface, Driver):
    _continued_failed_constraint = 0
    _UPDATE = None
    _FIND_ID = re.compile(r"\/([0-9]+)\/")

    @staticmethod
    def parse_style_attribute(style_string: str) -> str:
        """Get the url for the cover image"""
        if "background-image" in style_string:
            style_string = style_string.split(" url('")[1]
            style_string = style_string.split("');")[0]
            return style_string
        raise AttributeError("attribute 'background-image' not found")

    @staticmethod
    def links_2_tmo() -> list[str]:
        return [
            f"https://lectortmo.com/latest_uploads?page={index}&uploads_mode=thumbnail"
            for index in range(1, 21)
        ]

    def _save_element_2_db(self, *args, **kwargs):
        manga_name, manga_id, cover_link, link_to_book, chapter_number = args
        # Get or Create Manga reference
        manga, _ = Manga.objects.get_or_create(
            name=manga_name, uid=manga_id, cover=cover_link, link_to_manga=link_to_book
        )
        chapter, _ = Chapter.objects.get_or_create(
            manga_id=manga,
            uid=manga_id,
            number=chapter_number,
            cover=cover_link,
            link_to_manga=link_to_book,
        )
        self._UPDATE.chapters.add(chapter)

    def extract_content(self, elements: list[WebElement]) -> None:
        for element in elements:
            try:
                link_to_book = str(
                    element.find_element(By.TAG_NAME, "a").get_attribute("href")
                )
                manga_id = re.search(self._FIND_ID, link_to_book)[1]
                manga_name = element.find_element(
                    By.CSS_SELECTOR, "div.thumbnail-title > h4.text-truncate"
                ).text
                chapter_number = element.find_element(
                    By.CSS_SELECTOR, "div.chapter-number > span.number"
                ).text
                cover_link = self.parse_style_attribute(
                    str(
                        element.find_element(By.TAG_NAME, "style").get_attribute(
                            "innerHTML"
                        )
                    )
                )
            except NoSuchElementException:
                continue
            try:
                self._save_element_2_db(
                    manga_name, manga_id, cover_link, link_to_book, chapter_number
                )
            except IntegrityError:
                print("IntegrityError")
                self._continued_failed_constraint += 1
                continue

    def start_extraction(self):
        update = Update()
        update.save()
        print(update)
        self._UPDATE: Update = update
        for url in self.links_2_tmo():
            # if self.__continued_failed_constraint >= 30:
            # If the counter is over 30, all content in the page is already in db
            #    break
            self.driver.get(url)
            list_of_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "div.upload-file-row"
            )
            sleep(6)
            self.extract_content(list_of_elements)
        return True


class Crawler:

    @staticmethod
    def update_content(extractor: ContentExtractorInterface):
        result = extractor.start_extraction()
        return result


if __name__ == "__main__":
    crawler = Crawler
    tmo = TMOExtractorContent()
    crawler.update_content(tmo)
