import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


try:
    pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
    FONT = "Arial"
except:
    FONT = "Helvetica"


class PaperGenerator:

    def __init__(self):

        os.makedirs(
            "output/question_papers",
            exist_ok=True
        )


    def generate_pdf(self, paper):

        subject = paper["header"]["subject_code"]

        filename = subject + "_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".pdf"

        filepath = os.path.join(
            "output/question_papers",
            filename
        )

        c = canvas.Canvas(
            filepath,
            pagesize=A4
        )

        width, height = A4

        y = height - 45

        # ------------------------------------------------

        c.setFont(FONT, 15)

        c.drawCentredString(
            width/2,
            y,
            paper["header"]["university"]
        )

        y -= 22

        c.setFont(FONT, 12)

        c.drawCentredString(
            width/2,
            y,
            paper["header"]["exam"]
        )

        y -= 22

        c.drawCentredString(
            width/2,
            y,
            paper["header"]["department"]
        )

        y -= 20

        c.drawCentredString(
            width/2,
            y,
            paper["header"]["subject_code"]
            + " - "
            + paper["header"]["subject_name"]
        )

        y -= 20

        c.drawCentredString(
            width/2,
            y,
            "Regulation " +
            paper["header"]["regulation"]
        )

        y -= 35

        c.drawString(
            40,
            y,
            "Time : Three Hours"
        )

        c.drawRightString(
            width-40,
            y,
            "Maximum Marks : 100"
        )

        y -= 25

        c.drawString(
            40,
            y,
            "Reg. No."
        )

        c.rect(
            110,
            y-5,
            220,
            18
        )

        y -= 25

        c.line(
            40,
            y,
            width-40,
            y
        )

        y -= 25

        c.setFont(FONT, 11)

        c.drawCentredString(
            width/2,
            y,
            "Answer ALL Questions"
        )

        y -= 30

        # ------------------------------------------------
        # PART A
        # ------------------------------------------------

        c.setFont(FONT, 12)

        c.drawString(
            40,
            y,
            "PART A (10 × 2 = 20)"
        )

        y -= 25

        c.setFont(FONT, 10)

        for i, q in enumerate(paper["part_a"], 1):

            if y < 70:

                c.showPage()

                y = height - 50

                c.setFont(FONT, 10)

            c.drawString(
                50,
                y,
                f"{i}. {q}"
            )

            y -= 18

        # ------------------------------------------------

        y -= 15

        c.setFont(FONT, 12)

        c.drawString(
            40,
            y,
            "PART B (5 × 13 = 65)"
        )

        y -= 25

        c.setFont(FONT, 10)

        for q in paper["part_b"]:

            c.drawString(
                40,
                y,
                f'{q["number"]}. (a) {q["a"]}'
            )

            y -= 20

            c.drawCentredString(
                width/2,
                y,
                "OR"
            )

            y -= 20

            c.drawString(
                40,
                y,
                f'(b) {q["b"]}'
            )

            y -= 30

        # ------------------------------------------------

        c.setFont(FONT, 12)

        c.drawString(
            40,
            y,
            "PART C (1 × 15 = 15)"
        )

        y -= 25

        c.setFont(FONT, 10)

        for q in paper["part_c"]:

            c.drawString(
                40,
                y,
                f'{q["number"]}. (a) {q["a"]}'
            )

            y -= 20

            c.drawCentredString(
                width/2,
                y,
                "OR"
            )

            y -= 20

            c.drawString(
                40,
                y,
                f'(b) {q["b"]}'
            )

        c.save()

        return filepath