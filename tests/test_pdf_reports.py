import pymupdf
import pytest
from services.report_service import analyze_labs, extract_pdf, ReportError, clean_filename

SAMPLE='''LDL Cholesterol 165 mg/dL 0 - 100
Vitamin D 15 ng/mL 30 - 100
Hemoglobin 14.2 g/dL 13 - 17
Total Cholesterol 230 mg/dL < 200
TSH 4.5 mIU/L 0.4 - 4.0
Fasting Glucose 115 mg/dL 70 - 99
Creatinine 1.0 mg/dL
'''


def test_range_flags_only_when_range_is_supplied():
    results={x["name"]:x for x in analyze_labs(SAMPLE)}
    assert results["LDL Cholesterol"]["status"]=="High"
    assert results["Vitamin D"]["status"]=="Low"
    assert results["Hemoglobin"]["status"]=="Within stated range"
    assert results["Total Cholesterol"]["status"]=="High"
    assert results["TSH"]["status"]=="High"
    assert results["Fasting Glucose"]["status"]=="High"
    assert results["Creatinine"]["status"]=="Not evaluated"


def test_real_pdf_extraction():
    doc=pymupdf.open()
    page=doc.new_page()
    page.insert_text((75,100),"Illustrative Laboratory Report",fontsize=15)
    page.insert_text((75,135),"LDL Cholesterol 165 mg/dL 0 - 100",fontsize=10)
    page.insert_text((75,153),"Vitamin D 15 ng/mL 30 - 100",fontsize=10)
    data=doc.tobytes()
    doc.close()
    raw,pages=extract_pdf(data)
    assert pages==1
    assert "LDL Cholesterol" in raw
    parsed=analyze_labs(raw)
    assert any(x["name"]=="LDL Cholesterol" and x["status"]=="High" for x in parsed)


def test_reject_bad_or_empty_pdf():
    with pytest.raises(ReportError,match="valid PDF"):
        extract_pdf(b"%NOT_A_PDF")
    with pytest.raises(ReportError,match="10 MB"):
        extract_pdf(b"")
    assert clean_filename("C:\\Users\\example\\patient.pdf")=="patient.pdf"


def test_reference_not_invented():
    data=analyze_labs("Vitamin B12 170 pg/mL\nHDL 50 mg/dL")
    assert len(data)==2
    assert all(x["status"]=="Not evaluated" and not x["reference"] for x in data)
