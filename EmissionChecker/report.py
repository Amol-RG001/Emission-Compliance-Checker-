
# ###

# Date: 2025-09-01 10:56:00
# Fuel Type: Petrol
# Power Output: 525 kW
# Operating Hours: 1 hr
#
# 📊 Final Report (for 525 kW , 1 hr)
#
# Pollutant    Measured (g/kWh)    BS6 Limit (g/kWh)    Total Emission (g)    Status
# CO           1.208               1.5                  634.2                 ✅ PASS
# NOx          0.21                0.25                 110.25                ✅ PASS
# PM           0.011               0.01                 5.78                  ❌ FAIL
# HC           0.052               0.07                 27.3                  ✅ PASS
#
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime

def generate_pdf_report(filename: str, fuel_type: str, power_kw: float, hours: float, emissions: dict, limits: dict):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    # Date & Header Info
    content.append(Paragraph("Emission Compliance Report", styles["Title"]))
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content.append(Paragraph(f"<b>Date:</b> {date_str}", styles["Normal"]))
    content.append(Paragraph(f"<b>Fuel Type:</b> {fuel_type}", styles["Normal"]))
    content.append(Paragraph(f"<b>Power Output:</b> {power_kw} kW", styles["Normal"]))
    content.append(Paragraph(f"<b>Operating Hours:</b> {hours} hr", styles["Normal"]))
    content.append(Spacer(1, 12))

    # Final Report Title

    content.append(Paragraph(f" <b>\u26A0 Final Report</b> (for {power_kw} kW , {hours} hr)", styles["Heading2"]))
    content.append(Spacer(1, 12))

    # Table Header
    data = [["Pollutant", "Measured (g/kWh)", "BS6 Limit (g/kWh)", "Total Emission (g)", "Status"]]

    # Fill Table Rows
    for pollutant, measured in emissions.items():
        limit = limits.get(pollutant, "-")

        total_emission = measured * power_kw * hours
        status = "\u2714 PASS" if measured <= limit else "\u2718 FAIL"
        data.append([pollutant, f"{measured:.2f}", f"{limit:.3f}", f"{total_emission:.2f}", status])

    # Table Styling
    table = Table(data, colWidths=[80, 120, 120, 120, 80])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.8, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    content.append(table)

    # Build PDF
    doc.build(content)
    print(f"✅ Report generated: {filename}")


#generate_pdf_report("final_report.pdf", fuel_type, power_kw, hours, emissions, limits)
