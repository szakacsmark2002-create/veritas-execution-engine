from nl import interpret_question

questions = [
    "Ce probleme sunt azi?",
    "De ce order 002799 este blocat?",
    "Ce materiale lipsesc?"
]

for q in questions:
    print(q, "->", interpret_question(q))

