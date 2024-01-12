import random

class Schedule:
    def __init__(self, data, days=5):
        """self.template = {
            "subject": None,
            "teacher": None
        }"""
        self.days = days
        self.schedule = {}
        self.data = data
        classes = data["classes"]
        """schedule = {
            "8A": [[lesson1, leesson2, lesson3, lesson4], [lesson1, lesson2, lesson3, lesson4]]
        }
        """
        for c in classes:
            self.schedule[c["name"]] = []

        self.teachers = data["teachers"]

    def randomly_generate(self):
        data = self.data

        # function to get class by its name
        def get_class(name):
            for c in data["classes"]:
                if c["name"].strip().lower() == name.strip().lower():
                    return c

        for c in self.schedule.keys():
            # filling class with random amount of lessons
            cl = get_class(c)
            self.schedule[c] = [[] for i in range(self.days)]
            for day in range(self.days):
                lessons_num = random.randint(cl["minimum_lessons"], cl["maximum_lessons"])

                # filling every day with random lessons
                for lesson in range(lessons_num):
                    subject = random.choice(cl["curriculum"])
                    self.schedule[c][day].append(subject)



