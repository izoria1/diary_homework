import sys
import json
from diarybook import Diary, DiaryBook
from util import read_from_json_into_application
from account_manager import load_accounts, register_user, login_user

class Menu:

    def __init__(self):
        self.diarybook = DiaryBook()
        self.accounts = load_accounts()
        self.authenticate_user()
        self.choices = {
            "1": self.show_diaries,
            "2": self.add_diary,
            "3": self.search_diaries,
            "4": self.populate_database,
            '5': self.quit
        }

    def authenticate_user(self):
        while True:
            print("1: Register")
            print("2: Login")
            choice = input("Choose an option: ")
            if choice == "1":
                if register_user(self.accounts):
                    self.accounts = load_accounts()  # Reload accounts after registration
            elif choice == "2":
                username = input("Enter username: ")
                password = input("Enter password: ")
                if login_user(self.accounts, username, password):
                    self.current_user = username  # Correctly set the current user
                    print("Login successful.")
                    self.load_user_diaries()
                    break
                else:
                    print("Invalid username or password.")
            else:
                print("Invalid choice.")


    def load_user_diaries(self):
        try:
            with open(f'{self.current_user}_diaries.json', 'r') as file:
                diaries_data = json.load(file)
                self.diarybook.diaries = [Diary(d['memo'], d['tags']) for d in diaries_data]
        except FileNotFoundError:
            self.diarybook.diaries = []  # Initialize an empty list if the file doesn't exist


    def save_user_diaries(self):
        diaries_data = [{'memo': d.memo, 'tags': d.tags} for d in self.diarybook.diaries]
        with open(f'{self.current_user}_diaries.json', 'w') as file:
            json.dump(diaries_data, file)

    def display_menu(self):
        print(""" 
                 Notebook Menu  
                1. Show diaries
                2. Add diary
                3. Search diaries
                4. Populate database
                5. Quit program
                """)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def show_diaries(self, diaries=None):
        if not diaries:
            diaries = self.diarybook.diaries

        print("Sort options: ")
        print("1: Sort by ID")
        print("2: Sort by Memo content")
        sort_choice = input("Choose your sort option (or press enter to skip): ")

        if sort_choice == "1":
            diaries = sorted(diaries, key=lambda diary: diary.id)
        elif sort_choice == "2":
            diaries = sorted(diaries, key=lambda diary: diary.memo)

        for diary in diaries:
            print(f"ID: {diary.id}, Memo: {diary.memo}, Tags: {diary.tags}")


    def add_diary(self):
        memo = input("Enter a memo: ")
        tags = input("Add tags: ")
        self.diarybook.new_diary(memo, tags)
        self.save_user_diaries()
        print("Your note has been added")

    def search_diaries(self):

        filter_text = input("Search for:  ")
        diaries = self.diarybook.search_diary(filter_text)
        for diary in diaries:
            print(f"{diary.id}-{diary.memo}")

    def quit(self):
        self.save_user_diaries()
        print("Thank you for using diarybook today")
        sys.exit(0)

    def populate_database(self):
        diaries1 = read_from_json_into_application('data.json')
        for diary in diaries1:
            self.diarybook.diaries.append(diary)


if __name__ == "__main__":
    Menu().run()
