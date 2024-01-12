from Schedule import Schedule
from xset import NoHashUnorderedSet

class Rater:
    def __init__(self, data, pairs=True):
        self.data = data

    def info(self):
        print("teachers:", len(self.data["teachers"]))
        print("classes:", len(self.data["classes"]))

    def rate_pairs(self, schedule: Schedule, class_: str):
        pair_score = 0
        for day in schedule.schedule[class_]:
            prev_prev_lesson = ""
            prev_lesson = ""
            for lesson in day:
                # if pair +1 score
                if lesson["subject"] == prev_lesson:
                    pair_score += 1

                # if triple +0.5 score
                if lesson["subject"] == prev_prev_lesson:
                    pair_score -= 0.5

                prev_prev_lesson = prev_lesson
                prev_lesson = lesson["subject"]

        # normalizing pair_score
        pair_score /= sum(map(lambda x: len(x) // 2, schedule.schedule[class_]))

        return pair_score

    def rate_distribution(self, schedule: Schedule, class_: str):
        distributed_score = 0

        subjects = []
        for i in schedule.schedule[class_]:
            for j in i:
                subjects.append(j)

        for subject in NoHashUnorderedSet(subjects):
            indexes = []
            for day in schedule.schedule[class_]:
                for lesson in range(len(day)):
                    if day[lesson] == subject:
                        indexes.append(lesson)
                        break

            distances = []
            for i in range(len(indexes) - 1):
                distances.append(abs(indexes[i + 1] - indexes[i]))

            distances.append(abs(indexes[-1] - indexes[0]))

            distributed_score = 1
            for _ in distances:
                distributed_score *= _


            distributed_score **= 0.5
            distributed_score /= 2 * (3 ** 0.5)

        distributed_score /= len(NoHashUnorderedSet(subjects))
        return distributed_score

    def rate_curriculum(self, schedule: Schedule, class_: str):
        curriculum_score = 0
        day_len_score = 0
        study_plan = 0

        class_data = {}
        for class_d in schedule.data["classes"]:
            if class_d["name"] == class_:
                class_data = class_d
                break


        lessons = []
        for day in schedule.schedule[class_]:
            lessons += day
            if class_data["minimum_lessons"] <= len(day) <= class_data["maximum_lessons"]:
                day_len_score += 1

        day_len_score /= schedule.days

        for l in NoHashUnorderedSet(lessons):
            if l["hours_per_week"] == lessons.count(l):
                study_plan += 1

        study_plan /= len(NoHashUnorderedSet(lessons))

        curriculum_score = study_plan + day_len_score
        curriculum_score /= 2

        return curriculum_score

    def t_rate_curriculum(self, schedule: dict, teacher: dict):
        week_days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5}
        days_week = dict(zip(week_days.values(), week_days.keys()))
        hours_of_work = 0
        days_of_work = []
        score = 0
        for class_ in schedule.values():
            day_num = 0
            for day in class_:
                flag = False
                for lesson in day:
                    if lesson["teacher"] == teacher["full_name"]:
                        hours_of_work += 1
                        flag = True
                if flag:
                    days_of_work.append(day_num)

                day_num += 1

        if hours_of_work <= teacher["maximum_hours"]:
            score += 1

        if len(days_of_work) <= teacher["maximum_days"]:
            score += 1

        flag = True
        for day in days_of_work:
            if not teacher["available_days"][days_week[day]]:
                flag = False

        if flag:
            score += 1

        return score

    def rate_schedule(self, schedule: Schedule):
        """
        rate:
        1) that subjects are in pairs, for every pair +1 score divided by maximum sum of pairs
        2) that subjects are distributed: square root of the multiplication of distances divided by 2 square root of 3;
        3) that curriculum is works, +3 score for this
        4) teachers' curriculum is works, +3 score for this
        """

        classes_score = {"pair_scores": [], "distributed_scores": [], "curriculum_scores": []}

        for class_ in schedule.schedule.keys():
            pair_score = 0
            distributed_score = 0
            curriculum_score = 0

            # 1) pairs
            pair_score = self.rate_pairs(schedule, class_)

            # 2) distribution
            distributed_score = self.rate_distribution(schedule, class_)

            # 3) curriculum
            curriculum_score = self.rate_curriculum(schedule, class_)

            # add everything to statistics
            classes_score["pair_scores"].append(pair_score)
            classes_score["distributed_scores"].append(distributed_score)
            classes_score["curriculum_scores"].append(curriculum_score)

        pair_score = sum(classes_score["pair_scores"]) / len(classes_score["pair_scores"])
        distributed_score = sum(classes_score["distributed_scores"]) / len(classes_score["distributed_scores"])
        curriculum_score = sum(classes_score["curriculum_scores"]) / len(classes_score["curriculum_scores"])

        # rating teachers' curriculums
        t_score = 0
        for teacher in schedule.teachers:
            t_score += self.t_rate_curriculum(schedule.schedule, teacher)

        t_score /= len(schedule.teachers)

        score = pair_score + distributed_score + curriculum_score + t_score
        return score
