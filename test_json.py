from gemini import generate_question_paper

paper = generate_question_paper(
    regulation="2021",
    department="CSE",
    subject_code="CS3491",
    subject_name="Artificial Intelligence",
    syllabus_text="Artificial Intelligence, Search, Knowledge Representation, Planning, Machine Learning",
    previous_papers_text="Previous papers related to AI."
)

print(type(paper))
print()

print(paper["header"])
print()

print("PART A")
for i, q in enumerate(paper["part_a"], start=1):
    print(i, q)

print()

print("PART B")
for q in paper["part_b"]:
    print(q)

print()

print("PART C")
for q in paper["part_c"]:
    print(q)