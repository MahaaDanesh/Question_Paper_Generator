import sqlite3
import os

# ----------------------------
# Create database folder
# ----------------------------
os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/anna_qp.db")
cursor = conn.cursor()

# ============================
# Departments
# ============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    department_code TEXT UNIQUE NOT NULL,

    department_name TEXT NOT NULL

)
""")

# ============================
# Subjects
# ============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS subjects(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    regulation TEXT NOT NULL,

    department_code TEXT NOT NULL,

    subject_code TEXT NOT NULL,

    subject_name TEXT NOT NULL,

    folder_path TEXT NOT NULL,

    syllabus_pdf TEXT NOT NULL,

    UNIQUE(regulation,department_code,subject_code)

)
""")

# ============================
# Previous Papers
# ============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS previous_papers(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    subject_code TEXT NOT NULL,

    pdf_name TEXT,

    exam_year TEXT,

    exam_month TEXT,

    pdf_path TEXT

)
""")

# ============================
# Generated Papers
# ============================

cursor.execute("""
CREATE TABLE IF NOT EXISTS generated_papers(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    subject_code TEXT,

    generated_date TEXT,

    question_paper_pdf TEXT,

    answer_key_pdf TEXT

)
""")

# ============================
# Departments
# ============================

departments=[

("CSE","Computer Science and Engineering"),

("AIML","Artificial Intelligence and Machine Learning")

]

cursor.executemany("""

INSERT OR IGNORE INTO departments

(department_code,department_name)

VALUES (?,?)

""",departments)

conn.commit()

conn.close()

print("Database Created Successfully")