from services.export_service import make_english_pdf
import fitz


def test_downloadable_pdf_summary():
    data=make_english_pdf("Illustrative Labs","## Summary\nA sample summary for educational purposes.")
    assert data.startswith(b"%PDF-")
    with fitz.open(stream=data,filetype="pdf") as doc:
        assert "Healthcare Info Assistant" in doc[0].get_text()
