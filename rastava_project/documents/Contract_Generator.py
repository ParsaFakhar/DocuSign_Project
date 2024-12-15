from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, black
import base64


def generate_contract_pdf(save_path=None):
    """Generate a compact PDF contract with placeholders and save it optionally."""
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(400, 600))  # Reduce page size for a more compact layout
    width, height = 400, 600

    # Contract title
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 50, "Contract Agreement")

    # Contract body text
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 100, "This agreement contract!.")
    c.drawString(50, height - 120, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
    c.drawString(50, height - 140, "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    c.drawString(50, height - 160, "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.")
    c.drawString(50, height - 180, "Nisi ut aliquip ex ea commodo consequat.")
    c.drawString(50, height - 200, "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.")

    # Placeholder for User's signature
    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 260, "Name:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(100, height - 260, "/USRNM/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 280, "Email:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(100, height - 280, "/USREML/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 300, "Signing Place:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(150, height - 300, "/SignHereUser/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 320, "Signature (User): _______________________")

    # Placeholder for Recipient's signature
    c.drawString(50, height - 380, "Name:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(100, height - 380, "/RCPTN/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 400, "Email:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(100, height - 400, "/RCPTEML/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 420, "Signing Place:")
    c.setFillColorRGB(1, 0, 0)  # Red text
    c.drawString(150, height - 420, "/SignRecipient/")

    c.setFillColorRGB(0, 0, 0)  # Black text
    c.drawString(50, height - 440, "Signature (Recipient): __________________")

    # Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, 50, "Generated using Django and ReportLab")

    c.save()

    # Save PDF if save_path is provided
    if save_path:
        with open(save_path, 'wb') as f:
            f.write(buffer.getvalue())

    buffer.seek(0)
    return buffer.read()  # Return PDF data for further use


def convert_pdf_to_base64(file_path):
    """Convert PDF file at file_path to a base64-encoded string."""
    with open(file_path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read()).decode("utf-8")
    return encoded_string
