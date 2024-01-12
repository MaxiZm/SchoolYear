from Schedule import Schedule
import json
from Rater import Rater
from deap import *

with open('data.json') as f:
    data = json.load(f)


sch = Schedule(data)
rater = Rater(data)


rater.info()
sch.randomly_generate()

print(sch.schedule)

for class_name, class_ in zip(sch.schedule.keys(), sch.schedule.values()):
    print(class_name)
    print(*list(map(lambda x: list(map(lambda y: y["subject"], x)), class_)), sep="\n")
    print()

res = rater.rate_schedule(sch)
print(res)

