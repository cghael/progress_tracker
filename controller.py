from state_classes.menu_state import MenuState
from state_classes.add_student_state import AddStudentState
from state_classes.add_points_state import AddPointsState
from state_classes.find_state import FindState
from state_classes.statistics_state import StatisticsState


class Controller:

    _state = None

    def __init__(self) -> None:
        self._orchestrator = {
            "menu": MenuState,
            "add students": AddStudentState,
            "add points": AddPointsState,
            "find": FindState,
            "statistics": StatisticsState,
            "stay": self.get_state,
            "exit": self.bye
        }
        self.students = {}
        self.statistic = {
            "MP": "n/a",
            "LP": "n/a",
            "HA": "n/a",
            "LA": "n/a",
            "EC": "n/a",
            "HC": "n/a"
        }
        self.scores = {
            "python": {"score": 600,
                       "txt": "Python"},
            "dsa": {"score": 400,
                    "txt": "DSA"},
            "databases": {"score": 480,
                          "txt": "Databases"},
            "flask": {"score": 550,
                      "txt": "Flask"},
        }
        self.set_state(MenuState())
        self.to_notify = {}

    def set_state(self, state) -> None:
        self._state = state
        if self._state:
            self._state.set_context(self)

    def get_state(self):
        return self._state

    def handle_request(self):
        return self._state.handle_request()

    def run(self):
        self.greetings()
        while self._state:
            res = self.handle_request()
            self.set_state(self._orchestrator[res]())

    @staticmethod
    def greetings():
        print("Learning progress tracker")

    @staticmethod
    def bye():
        print("Bye!")
        return None


def main():
    tracker = Controller()
    tracker.run()


if __name__ == "__main__":
    main()
