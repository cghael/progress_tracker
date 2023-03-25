import hashlib as h
import re


from .state import State


class AddStudentState(State):

    def handle_request(self):
        user_input = input().strip()
        if user_input == "back":
            return self.back_handle()
        return self.add_student(user_input)

    # ---------- Back command handle ----------

    def back_handle(self):
        print(f"Total {len(self._context.students)} students have been added")
        return "menu"

    # ---------- Add students command handle ----------

    def add_student(self, name_str):
        try:
            student = self.is_correct_name(name_str)
            self.try_add_student(student)
            print("The student has been added.")
            # return "stay"
        except ValueError as err:
            print(err)
        except IndexError as err:
            print(err)
        finally:
            return "stay"

    def try_add_student(self, student):
        student_id = self.get_hashed_id(student[-1])
        if self._context.students.get(student_id) is not None:
            raise IndexError("This email is already taken.")
        self._context.students[student_id] = {"points": [0, 0, 0, 0],
                                              "tasks": [0, 0, 0, 0],
                                              "name": " ".join(student[:-1]),
                                              "email": student[-1]}

    @staticmethod
    def get_hashed_id(h_string):
        m = h.md5()
        m.update(h_string.encode())
        return str(int(m.hexdigest(), 16))[:5]

    @staticmethod
    def create_name_list(name_str):
        name_str = name_str.split()
        first = name_str[0]
        email = name_str[-1]
        second = " ".join(name_str[1:-1])
        return first, second, email

    @staticmethod
    def is_valid_name(name):
        if len(name) < 2:
            return False

        pattern = r"[^a-zA-Z-']|--|''|-'|'-|^[-']\w+|\w+[-']$"
        for word in name.split():
            if re.search(pattern, word):
                return False
        return True

    @staticmethod
    def is_valid_email(email):
        if re.search(r"\w+@\w+", email) is None:
            return False
        domain = email.split("@")[1]
        if re.search(r"\w+\.\w+", domain) is None:
            return False
        return True

    def is_correct_name(self, name_str):
        if not name_str:
            raise ValueError("Incorrect credentials.")

        name_list = self.create_name_list(name_str)

        if "" in name_list:
            raise ValueError("Incorrect credentials.")

        if not self.is_valid_name(name_list[0]):
            raise ValueError("Incorrect first name.")

        if not self.is_valid_name(name_list[1]):
            raise ValueError("Incorrect last name.")

        if not self.is_valid_email(name_list[2]):
            raise ValueError("Incorrect email.")

        return name_list
