from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def export_chat_pdf(
        messages,
        filename="chat_history.pdf"
):

    doc = SimpleDocTemplate(
        filename
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    for msg in messages:

        p = Paragraph(
            f"<b>{msg['role']}:</b> "
            f"{msg['content']}",
            styles["BodyText"]
        )

        elements.append(p)

        elements.append(
            Spacer(
                1,
                12
            )
        )

    doc.build(
        elements
    )

    return filename