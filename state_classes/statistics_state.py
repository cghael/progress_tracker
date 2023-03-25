from .state import State


class StatisticsState(State):
    """
        A state that displays statistics for the student grades.
    """

    def handle_request(self):
        user_input = input().strip()
        if user_input == "back":
            return self.back_handle()
        return self.top_students(user_input.lower())

    # ---------- Back command handle ----------

    @staticmethod
    def back_handle():
        return "menu"

    # ---------- Top students command handle ----------

    def top_students(self, course):
        """
            Displays the top students for the given course.
            If the course is not recognized, prints an error message and returns.

            Args:
                course (str): The name of the course.

            Returns:
                str: A string representing the state to transition to
                after the method is executed.
        """

        if course not in self._context.scores:
            print("Unknown course.")
            return "stay"

        index = list(self._context.scores.keys()).index(course)
        students = []
        for student_id, results in self._context.students.items():
            if results["points"][index] > 0:
                students.append([student_id, results["points"][index]])

        desc_students = sorted(students, key=lambda item: item[1], reverse=True)
        max_course_scores = self._context.scores[course]["score"]

        percent_list = []
        for student_id, points in desc_students:
            percents = self.percents(points, max_course_scores)
            percent_list.append([student_id, points, percents])

        self.print_top_students(percent_list, course)
        return "stay"

    @staticmethod
    def percents(points, max_points):
        return round(points * 100 / max_points, 1)

    def print_top_students(self, students, course):
        print(f"{self._context.scores[course]['txt']}\n"
              f"id\t\tpoints\tcompleted")
        for s in students:
            print(f"{s[0]}\t{s[1]}\t\t{s[2]}%")