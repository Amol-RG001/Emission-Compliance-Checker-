from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf_report(filename: str, fuel_type: str, emissions: dict, compliance: dict):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("Emission Compliance Report", styles["Title"]))
    content.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles["Normal"]))
    content.append(Paragraph(f"Fuel Type: {fuel_type}", styles["Normal"]))
    content.append(Spacer(1, 12))

    table_data = [["Pollutant", "Emission (g/kWh)", "Compliant?"]]
    for pollutant in emissions:
        status = "PASS ✅" if compliance[pollutant] else "FAIL ❌"
        table_data.append([pollutant, str(emissions[pollutant]), status])

    table = Table(table_data, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    content.append(table)

    doc.build(content)
