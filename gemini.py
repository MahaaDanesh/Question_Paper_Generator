import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_question_paper(
    regulation,
    department,
    subject_code,
    subject_name,
    syllabus_text,
    previous_papers_text
):

    prompt = f"""
You are an expert Anna University Question Paper Setter.

Generate ONE Anna University End Semester Examination Question Paper.

===========================
DETAILS
===========================

Regulation : {regulation}

Department : {department}

Subject Code : {subject_code}

Subject Name : {subject_name}

===========================
SYLLABUS
===========================

{syllabus_text}

===========================
PREVIOUS YEAR QUESTION PAPERS
===========================

{previous_papers_text}

===========================
IMPORTANT RULES
===========================

1. Follow Anna University Question Paper Pattern.

2. Generate

PART A
10 Questions × 2 Marks

PART B
Question 11 to 15
Each question has (a) OR (b)

PART C
Question 16
(a) OR (b)

3. Cover every unit.

4. Do NOT copy previous year questions.

5. Maintain Anna University difficulty level.

6. Return ONLY valid JSON.

7. Do NOT use markdown.

8. Do NOT use ```json.

Return exactly in this format.

{{
    "header": {{
        "university":"ANNA UNIVERSITY, CHENNAI",
        "exam":"B.E./B.Tech Degree Examination",
        "semester":"",
        "regulation":"{regulation}",
        "department":"{department}",
        "subject_code":"{subject_code}",
        "subject_name":"{subject_name}",
        "time":"Three Hours",
        "maximum_marks":"100"
    }},

    "part_a":[
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "part_b":[
        {{
            "number":11,
            "a":"...",
            "b":"..."
        }},
        {{
            "number":12,
            "a":"...",
            "b":"..."
        }},
        {{
            "number":13,
            "a":"...",
            "b":"..."
        }},
        {{
            "number":14,
            "a":"...",
            "b":"..."
        }},
        {{
            "number":15,
            "a":"...",
            "b":"..."
        }}
    ],

    "part_c":[
        {{
            "number":16,
            "a":"...",
            "b":"..."
        }}
    ]
}}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini accidentally adds it
    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    return json.loads(text)