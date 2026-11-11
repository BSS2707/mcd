"""PDF Inspection Report generator using ReportLab."""
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from config.settings import REPORTS_DIR

def generate_pdf_report(inspection_data, original_img_path=None, annotated_img_path=None):
    """
    inspection_data: dict containing:
      - inspection_id
      - timestamp
      - image_name
      - defect_count
      - defect_names
      - detections (list of dicts)
      - status
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_filename = f"report_{inspection_data.get('inspection_id', 'unknown')}.pdf"
    pdf_path = os.path.join(REPORTS_DIR, report_filename)
    
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#253C6D'),
        spaceAfter=15
    )
    story.append(Paragraph("Motherboard Quality Inspection Report", title_style))
    story.append(Paragraph("Automated Visual Inspection System (YOLOv8)", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Metadata Table
    meta_data = [
        ["Inspection ID:", inspection_data.get('inspection_id', 'N/A')],
        ["Date / Time:", inspection_data.get('timestamp', 'N/A')],
        ["Image Filename:", inspection_data.get('image_name', 'N/A')],
        ["Overall Status:", inspection_data.get('status', 'N/A')],
        ["Total Defects Detected:", str(inspection_data.get('defect_count', 0))]
    ]
    meta_table = Table(meta_data, colWidths=[150, 350])
    meta_table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F2F5F9')),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#333333')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))
    
    # Defects Detail Table
    detections = inspection_data.get('detections', [])
    if detections:
        story.append(Paragraph("Detected Defects Breakdown", styles['Heading2']))
        det_data = [["#", "Defect Class", "Confidence", "Bounding Box [x1, y1, x2, y2]"]]
        for i, det in enumerate(detections, 1):
            box_str = f"[{', '.join(str(int(x)) for x in det.get('box', []))}]"
            det_data.append([str(i), det.get('name', 'N/A'), f"{det.get('confidence', 0):.2%}", box_str])
            
        det_table = Table(det_data, colWidths=[30, 150, 100, 220])
        det_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#253C6D')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ]))
        story.append(det_table)
    else:
        story.append(Paragraph("No defects detected. Motherboard passed inspection.", styles['Normal']))
        
    story.append(Spacer(1, 20))
    
    # Annotated Image if available
    if annotated_img_path and os.path.exists(annotated_img_path):
        story.append(Paragraph("Visual Evidence (Annotated)", styles['Heading2']))
        story.append(Spacer(1, 10))
        img = Image(annotated_img_path, width=400, height=300)
        story.append(img)
        
    doc.build(story)
    return pdf_path

