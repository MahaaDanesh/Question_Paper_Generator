from pdf_reader import read_pdf
from pdf_reader import read_previous_papers


print("Reading Syllabus...\n")

text = read_pdf(
    "data/R2025/CSE/CS3491/syllabus.pdf"
)

print(text)


print("\n\nReading Previous Papers...\n")

papers = read_previous_papers(
    "data/R2025/CSE/CS3491/previous"
)

print(papers)