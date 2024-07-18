import argparse
import getpass
import os
import random
import sys

import requests
from bs4 import BeautifulSoup

from handle_credentials import credentials

DIR = (
    os.getcwd()
)  # Set the `DIR` variable to the desired directory path where the contest folder will be created.


class Extractor:
    def __init__(self):
        self.problems = []
        self.folder_name = ""
        self.dir = DIR
        self.snippet = "snippet.txt"
        self.link = None
        self.user = None
        self.password = None
        self.soup = None
        self.link = None
        self.credentials = credentials()
        self.login_url = "https://codeforces.com/enter"

    def parse_args(self):
        parser = argparse.ArgumentParser(
            description="Easier_Contest: A Python script to enhance Codeforces contest preparation by auto-organizing problem files."
        )

        parser.add_argument("--link", "-l", help="link for contest")
        parser.add_argument("--config", "-c", help="Configure credentials")
        parser.add_argument("--extension", "-ex", help="The problem files extension")

        args = parser.parse_args()

        self.extension = (
            ".cpp" if str(args.extension) == "None" else str(args.extension)
        )

        self.link = args.link

        if args.config:
            user = input("Enter your user Name: ")
            password = getpass.getpass("Enter your password: ")

            self.credentials.user = user
            self.credentials.password = password
            self.credentials.save()
            exit()

        self.user, self.password = self.credentials.load()

    def login(self):
        session = requests.session()
        if self.link != None:
            self.soup = BeautifulSoup(session.get(self.link).text, "html.parser")
        else:
            print("Please provide a link using -l")
            exit()

        csrf = self.soup.find("input", {"name": "csrf_token"})["value"]
        ftaa = "".join([chr(random.randint(97, 122)) for _ in range(1, 18)])

        payload = {
            "csrf_token": csrf,
            "action": "enter",
            "ftaa": ftaa,
            "bfaa": "f1b3f18c715565b589b7823cda7448ce",
            "handleOrEmail": self.user,  # Python uses snake_case convention
            "password": self.password,
            "_tta": "176",
            "remember": "on",
        }
        session.post(self.login_url, data=payload)
        resp = session.get(self.link)
        self.soup = BeautifulSoup(resp.text, "html.parser")

    def get_problems(self):
        problems_table = self.soup.select_one(".problems")
        links = problems_table.select("a")
        flag = True
        for link in links:
            if (str(link["href"]).find("problem")) < 0 or link.text == "":
                continue
            if flag:
                temp = " ".join(link.text.split()) + "."
                flag = not flag
            else:
                temp = temp + " ".join(link.text.split()) + self.extension
                self.problems.append(temp)
                flag = not flag
        return self.problems

    def get_contest_name(self):
        title = self.soup.select_one(".rtable")
        self.folder_name = title.select_one("a").text
        return self.folder_name

    def foldernfiles(self, problems, folder_name):
        folder_path = os.path.join(self.dir, folder_name)

        try:
            os.mkdir(folder_path)
        except OSError as error:
            if input(
                f"The folder '{folder_path}' already exists. Do you want to continue anyway? (y/n):"
            ).lower() in ["yes", "y"]:
                folder_path = folder_path + "(1)"
                os.mkdir(folder_path)
            else:
                print("Terminating process...")
                exit()

        for name in problems:
            with open(os.path.join(folder_path, name), "w") as f:
                if self.snippet != None:
                    with open(self.snippet, "r") as r:
                        f.write(r.read())


def main():
    Names_grabber = Extractor()
    Names_grabber.parse_args()
    Names_grabber.login()
    problems = Names_grabber.get_problems()
    folder_name = Names_grabber.get_contest_name()

    Names_grabber.foldernfiles(problems, folder_name)


if __name__ == "__main__":
    main()
