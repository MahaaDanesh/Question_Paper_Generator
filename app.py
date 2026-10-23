from flask import Flask, render_template, request, redirect, flash
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = "anna_university_project"

DATABASE = "database/anna_qp.db"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================
# Home Page
# ==========================================
@app.route("/")
def home():
    return render_template("index.html")


# ==========================================
# Add Subject Page
# ==========================================
@app.route("/add-subject")
def add_subject():
    return render_template("add_subject.html")


# ==========================================
# Save Subject
# ==========================================
@app.route("/save-subject", methods=["POST"])
def save_subject():

    regulation = request.form["regulation"]
    department = request.form["department"]
    subject_code = request.form["subject_code"].upper().strip()
    subject_name = request.form["subject_name"].strip()

    syllabus = request.files["syllabus"]
    previous_papers = request.files.getlist("previous_papers")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # ---------------------------------------------------
    # Check if subject already exists
    # ---------------------------------------------------
    cursor.execute("""
        SELECT id
        FROM subjects
        WHERE regulation=?
        AND department_code=?
        AND subject_code=?
    """, (
        regulation,
        department,
        subject_code
    ))

    existing_subject = cursor.fetchone()

    if existing_subject:

        conn.close()

        flash("❌ Subject already exists!")

        return redirect("/add-subject")

    # ---------------------------------------------------
    # Create Folder Structure
    # ---------------------------------------------------
    subject_folder = os.path.join(
        "data",
        f"R{regulation}",
        department,
        subject_code
    )

    previous_folder = os.path.join(
        subject_folder,
        "previous"
    )

    os.makedirs(previous_folder, exist_ok=True)

    # ---------------------------------------------------
    # Save syllabus
    # ---------------------------------------------------
    syllabus_path = ""

    if syllabus and syllabus.filename != "":

        syllabus_filename = "syllabus.pdf"

        syllabus_path = os.path.join(
            subject_folder,
            syllabus_filename
        )

        syllabus.save(syllabus_path)

    # ---------------------------------------------------
    # Insert Subject
    # ---------------------------------------------------
    cursor.execute("""
INSERT INTO subjects
(
regulation,
department_code,
subject_code,
subject_name,
folder_path,
syllabus_pdf
)

VALUES (?,?,?,?,?,?)
""",
(
regulation,
department,
subject_code,
subject_name,
subject_folder,
syllabus_path
))

    # ---------------------------------------------------
    # Save Previous Papers
    # ---------------------------------------------------
    for pdf in previous_papers:

        if pdf.filename == "":
            continue

        filename = secure_filename(pdf.filename)

        pdf_path = os.path.join(
            previous_folder,
            filename
        )

        pdf.save(pdf_path)

        cursor.execute("""
            INSERT INTO previous_papers
            (
                subject_code,
                exam_year,
                exam_month,
                pdf_path
            )
            VALUES (?,?,?,?)
        """, (
            subject_code,
            None,
            None,
            pdf_path
        ))

    conn.commit()

    conn.close()

    flash("✅ Subject Added Successfully!")

    return redirect("/add-subject")


# ==========================================
# View Subjects
# ==========================================
@app.route("/view-subjects")
def view_subjects():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            regulation,
            department_code,
            subject_code,
            subject_name
        FROM subjects
        ORDER BY regulation, department_code
    """)

    subjects = cursor.fetchall()

    conn.close()

    return render_template(
        "view_subjects.html",
        subjects=subjects
    )

# ==========================================
# Generate Question Paper Page
# ==========================================
# ==========================================
# Generate Question Paper
# ==========================================
@app.route("/generate", methods=["GET", "POST"])
def generate():

    if request.method == "POST":

        regulation = request.form["regulation"]

        department = request.form["department"]

        subject_code = request.form["subject_code"].upper().strip()


        conn = sqlite3.connect(DATABASE)

        cursor = conn.cursor()


        cursor.execute("""
            SELECT
                regulation,
                department_code,
                subject_code,
                subject_name,
                folder_path,
                syllabus_pdf
            FROM subjects
            WHERE regulation=?
            AND department_code=?
            AND subject_code=?
        """,
        (
            regulation,
            department,
            subject_code
        ))


        subject = cursor.fetchone()

        conn.close()


        if subject:

            return render_template(
                "result.html",
                message="✅ Subject Found",
                subject=subject
            )


        else:

            return render_template(
                "result.html",
                message="❌ Subject Not Found",
                subject=None
            )


    return render_template("generate.html")

if __name__ == "__main__":
    app.run(debug=True)