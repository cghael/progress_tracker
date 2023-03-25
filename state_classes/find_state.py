from .state import State


class FindState(State):

    def handle_request(self):
        user_input = input().strip()
        if user_input == "back":
            return self.back_handle()
        return self.find_student(user_input)

    # ---------- Back command handle ----------

    @staticmethod
    def back_handle():
        return "menu"

    # ---------- Add points command handle ----------

    def find_student(self, student_id):
        student = self._context.students.get(student_id)
        if student is None:
            print(f"No student is found for id={student_id}.")
        else:
            points = student["points"]
            print(f"{student_id} points: Python={points[0]}; "
                  f"DSA={points[1]}; Databases={points[2]}; Flask={points[3]}")
        return "stay"
