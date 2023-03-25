from .state import State


class MenuState(State):

    def handle_request(self):
        user_input = input().strip()
        request = user_input.lower()

        if not request:
            print("No input")
            return "stay"

        switcher = {
            "exit": self.exit_handle,
            "back": self.back_handle,
            "add students": self.add_student_handle,
            "list": self.list_handle,
            "add points": self.add_points_handle,
            "find": self.find_handle,
            "statistics": self.statistics_handle,
            "notify": self.notify_handle
        }
        return switcher.get(request, self.unknown_cmd)()

    # ---------- Exit command handle ----------

    @staticmethod
    def exit_handle():
        return "exit"

    # ---------- Back command handle ----------

    @staticmethod
    def back_handle():
        print("Enter 'exit' to exit the program.")
        return "stay"

    # ---------- Add student command handle ----------

    @staticmethod
    def add_student_handle():
        print("Enter student credentials or 'back' to return")
        return "add students"

    # ---------- Students list command handle ----------

    def list_handle(self):
        print("Students:")
        if not self._context.students:
            print("No students found")
        else:
            for i in list(self._context.students.keys()):
                print(i)
        return "stay"

    # ---------- Add points command handle ----------

    @staticmethod
    def add_points_handle():
        print("Enter an id and points or 'back' to return")
        return "add points"

    # ---------- Find command handle ----------

    @staticmethod
    def find_handle():
        print("Enter an id or 'back' to return")
        return "find"

    # ---------- Statistics command handle ----------

    def statistics_handle(self):
        print("Type the name of a course to see details or 'back' to quit")
        self.display_information()
        return "statistics"

    @staticmethod
    def get_results(students_values, indicator):
        results = {}
        for i, k in enumerate(["Python", "DSA", "Databases", "Flask"]):
            results[k] = [
                x[indicator][i] for x in students_values if x[indicator][i] > 0
            ]
        return results

    def build_statistic(self):
        """
            Args:
                None.

            Returns:
                A dictionary object containing the statistic information for the students,
                including the following keys:
                - "MP": most productive discipline(s) (Python, DSA, Databases, Flask)
                        by count of completed tasks.
                - "LP" (optional): least productive discipline(s) (Python, DSA, Databases, Flask)
                                    by count of completed tasks, returned only when at least one
                                    discipline has the lowest count of completed tasks.
                - "HA": most hard-working student(s) by sum of completed tasks.
                - "LA" (optional): least hard-working student(s) by sum of completed tasks,
                                   returned only when at least one student has the lowest
                                   sum of completed tasks.
                - "EC": most efficient student(s) by average points per task in each discipline.
                - "HC" (optional): least efficient student(s) by average points per task
                                   in each discipline, returned only when at least one student
                                   has the lowest average points per task.

            Raises:
                None.

            Side effects:
                None.
        """
        statistic = self._context.statistic.copy()
        if not self._context.students:
            return statistic

        students_values = self._context.students.values()
        points = self.get_results(students_values, "points")
        tasks = self.get_results(students_values, "tasks")

        counts = {k: len(v) for k, v in points.items()}
        statistic["MP"] = ", ".join(
            k for k, v in counts.items() if v == max(counts.values())
        )
        if max(counts.values()) != min(counts.values()):
            statistic["LP"] = ", ".join(
                k for k, v in counts.items() if v == min(counts.values())
            )

        sums = {k: sum(v) for k, v in tasks.items()}
        statistic["HA"] = ", ".join(
            k for k, v in sums.items() if v == max(sums.values())
        )
        if max(sums.values()) != min(sums.values()):
            statistic["LA"] = ", ".join(
                k for k, v in sums.items() if v == min(sums.values())
            )

        means = {k: sum(v)/len(v) if len(v) > 0 else 0 for k, v in points.items()}
        statistic["EC"] = ", ".join(
            k for k, v in means.items() if v == max(means.values())
        )
        if max(means.values()) != min(means.values()):
            statistic["HC"] = ", ".join(
                k for k, v in means.items() if v == min(means.values())
            )

        return statistic

    def display_information(self):
        statistic = self.build_statistic()
        print(f"Most popular: {statistic['MP']}\n"
              f"Least popular: {statistic['LP']}\n"
              f"Highest activity: {statistic['HA']}\n"
              f"Lowest activity: {statistic['LA']}\n"
              f"Easiest course: {statistic['EC']}\n"
              f"Hardest course: {statistic['HC']}")

    # ---------- Notify command handle ----------

    def notify_handle(self):
        notified = 0
        for stud_id, course_list in self._context.to_notify.items():
            for course in course_list:
                student = self._context.students[stud_id]
                print(f"To: {student['email']}\n"
                      f"Re: Your Learning Progress\n"
                      f"Hello, {student['name']}! You have accomplished our {course} course!")
            notified += 1
        print(f"Total {notified} students have been notified.")
        self._context.to_notify = {}
        return "stay"

    # ---------- Unknown command handle ----------

    @staticmethod
    def unknown_cmd():
        print("Error: unknown command!")
        return "stay"
