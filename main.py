import requests
from bs4 import BeautifulSoup
import os

DIR = r"D:\projects\cpp"

class Extractor:
    def __init__(self):
        self.problems = []
        self.folder_name = "" 
        self.dir = DIR
        self.snippet = "snippet.txt"

        with open('link.txt', 'r') as f:
                self.link = f.read()

        self.soup = BeautifulSoup(requests.get(self.link).text, "html.parser")


    def get_problems(self):
        problems_table = self.soup.select_one('.problems')
        links = problems_table.select("a")
        flag = True
        for link in links:
            if any(char == 'x' for char in link.text) or link.text == "":
                continue
            if flag:
                temp = ' '.join(link.text.split()) + "."
                flag = not flag
            else:
                temp = temp + ' '.join(link.text.split()) + ".cpp"
                self.problems.append(temp)
                flag = not flag
        return self.problems
    
    def get_contest_name(self):
        title = self.soup.select_one('.rtable')
        self.folder_name = title.select_one("a").text
        return self.folder_name
    
    def foldernfiles(self, problems, folder_name):
        folder_path = os.path.join(self.dir,folder_name)
        os.mkdir(folder_path) 
        for name in problems:
            with open(os.path.join(folder_path,name),'w') as f:
                if self.snippet != None:
                    with open(self.snippet,'r') as r:
                        f.write( r.read() )
                        

    
def main():

    Names_grabber = Extractor()

    problems = Names_grabber.get_problems()
    folder_name = Names_grabber.get_contest_name()

    Names_grabber.foldernfiles(problems,folder_name)

if __name__ == "__main__":
    main()     
