from .state import State


class AddPointsState(State):

    def handle_request(self):
        user_input = input().strip()
        if user_input == "back":
            return self.back_handle()
        return self.add_points(user_input)

    # ---------- Back command handle ----------

    @staticmethod
    def back_handle():
        return "menu"

    # ---------- Add points command handle ----------

    def add_points(self, points):
        """
            Adds points to a student's record.

            Args:
                points (str): A string of four space-separated integers representing the
                student ID and the points to add to each of the four tasks.

            Returns:
                str: A string representing the state to transition to after the method is executed.

            Raises:
                ValueError: If the input points string is empty or improperly formatted.
                IndexError: If the student with the specified ID is not found in the student records.

            Side effects:
                Updates the points and tasks lists of the specified student in the student records.

        """

        student_id = ""
        try:
            student_id, student_add_points = self.try_transform_points(points)
            student_stats = self._context.students.get(student_id)
            if student_stats is None:
                raise IndexError
        except ValueError:
            print("Incorrect points format")
        except IndexError:
            print(f"No student is found for id={student_id}")
        else:
            student_points = student_stats["points"]
            student_tasks = student_stats["tasks"]
            final_points = list(self._context.scores.values())

            for i, point in enumerate(student_add_points):
                student_points[i] += point

                if student_points[i] >= final_points[i]["score"]:
                    self.add_to_notify(student_id, final_points[i]["txt"])

                if point > 0:
                    student_tasks[i] += 1

            student_stats["points"] = student_points
            student_stats["tasks"] = student_tasks
            self._context.students[student_id] = student_stats
            print("Points updated")
        return "stay"

    def add_to_notify(self, student_id, course):
        if student_id in self._context.to_notify:
            self._context.to_notify[student_id].append(course)
        else:
            self._context.to_notify[student_id] = [course]

    @staticmethod
    def try_transform_points(points_str):
        if not points_str:
            raise ValueError

        points_str_list = points_str.split()
        student_id = points_str_list[0]
        point_list = []

        for i in points_str_list[1:]:
            i = int(i)
            if i < 0:
                raise ValueError
            point_list.append(i)

        if len(point_list) != 4:
            raise ValueError
        return student_id, point_list
