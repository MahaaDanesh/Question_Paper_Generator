from paper_generator import PaperGenerator
from gemini import generate_question_paper

paper = generate_question_paper(
    regulation="2025",
    department="CSE",
    subject_code="CS3491",
    subject_name="Artificial Intelligence",
    syllabus_text="AI syllabus",
    previous_papers_text="Previous AI papers"
)

generator = PaperGenerator()

pdf = generator.generate_pdf(paper)

print(pdf)