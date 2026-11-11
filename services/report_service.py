"""Safe local PDF extraction and conservative extraction of lab values/ranges."""
import io
import re
from pathlib import Path
import pymupdf
from config.settings import MAX_REPORT_BYTES, MAX_REPORT_PAGES, MAX_REPORT_CHARS, ENABLE_OCR, TESSERACT_CMD


class ReportError(ValueError):
    pass


# Ordering matters: specific names before broader labels to avoid overlapping matches.
TEST_NAMES = [
    ("eGFR", ["egfr", "estimated glomerular filtration rate"]),
    ("Uric Acid", ["uric acid", "serum urate"]),
    ("Albumin", ["serum albumin", "albumin"]),
    ("Alkaline Phosphatase", ["alkaline phosphatase", "alp"]),
    ("CRP", ["c-reactive protein", "crp"]),
    ("ESR", ["erythrocyte sedimentation rate", "esr"]),
    ("MCHC", ["mean corpuscular hemoglobin concentration", "mchc"]),
    ("MCH", ["mean corpuscular hemoglobin", "mch"]),
    ("MCV", ["mean corpuscular volume", "mcv"]),
    ("HbA1c", ["hba1c", "hemoglobin a1c", "glycated hemoglobin", "glycosylated hemoglobin"]),
    ("LDL Cholesterol", ["ldl cholesterol", "ldl-c", "ldl"]),
    ("HDL Cholesterol", ["hdl cholesterol", "hdl-c", "hdl"]),
    ("Total Cholesterol", ["total cholesterol", "cholesterol total", "serum cholesterol"]),
    ("Triglycerides", ["triglycerides", "triglyceride"]),
    ("Vitamin D", ["vitamin d 25-oh", "25 hydroxy vitamin d", "vitamin d", "25-oh vitamin d"]),
    ("Vitamin B12", ["vitamin b12", "b12", "cobalamin"]),
    ("Fasting Glucose", ["fasting blood glucose", "fasting glucose", "fbs", "fasting blood sugar"]),
    ("Blood Glucose", ["blood glucose", "plasma glucose", "blood sugar", "glucose"]),
    ("Hemoglobin", ["haemoglobin", "hemoglobin", "hb"]),
    ("Ferritin", ["ferritin"]),
    ("Serum Iron", ["serum iron", "iron"]),
    ("TSH", ["thyroid stimulating hormone", "tsh"]),
    ("Free T4", ["free t4", "ft4"]),
    ("Free T3", ["free t3", "ft3"]),
    ("Creatinine", ["creatinine"]),
    ("Urea", ["blood urea", "urea"]),
    ("Calcium", ["calcium"]),
    ("Sodium", ["sodium"]),
    ("Potassium", ["potassium"]),
    ("Platelets", ["platelet count", "platelets"]),
    ("WBC", ["white blood cell", "wbc"]),
    ("RBC", ["red blood cell", "rbc"]),
    ("ALT", ["alanine aminotransferase", "sgpt", "alt"]),
    ("AST", ["aspartate aminotransferase", "sgot", "ast"]),
    ("Bilirubin", ["total bilirubin", "bilirubin"]),
    ("Folate", ["folate", "folic acid"]),
    ("Magnesium", ["magnesium"]),
]
UNIT = r"(?:mg/L|g/L|ng/L|µg/dL|ug/dL|mg/dL|ng/mL|g/dL|mmol/L|µmol/L|umol/L|pg/mL|mL/min/1\.73m2|mIU/L|µIU/mL|uIU/mL|U/L|IU/L|mEq/L|fL|pg|%|10\^3/µL|10\^6/µL|x10\^3/uL|x10\^6/uL)"
NUMBER = r"-?\d{1,5}(?:[.,]\d{1,4})?"
# Reference must appear AFTER the measured value: e.g. 165 mg/dL 0-100; 4.5 mIU/L 0.4 - 4.0
RANGE_RE = re.compile(rf"(?<!\w)({NUMBER})\s*(?:-|–|—|to)\s*({NUMBER})(?!\w)", re.I)
LESS_RE = re.compile(rf"(?:<|≤|<=|up to)\s*({NUMBER})", re.I)
MORE_RE = re.compile(rf"(?:>|≥|>=)\s*({NUMBER})", re.I)
VALUE_RE = re.compile(rf"(?<![\w])({NUMBER})\s*({UNIT})?", re.I)


def clean_filename(name: str) -> str:
    return (Path(name.replace("\\", "/")).name or "report.pdf")[:180]


def _optional_ocr(page) -> str:
    try:
        import pytesseract
        from PIL import Image
        if TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.7, 1.7), alpha=False)
        pic = Image.open(io.BytesIO(pix.tobytes("png")))
        return pytesseract.image_to_string(pic, lang="eng")
    except Exception:
        return ""


def extract_image(data: bytes) -> tuple[str, int]:
    """Use local Tesseract on an image. No cloud OCR and no saved raw upload."""
    if not ENABLE_OCR:
        raise ReportError('Image OCR is optional: set ENABLE_OCR=true, install Tesseract and requirements-ocr.txt.')
    if not data or len(data)>MAX_REPORT_BYTES:
        raise ReportError('Image is empty or larger than 10 MB.')
    try:
        from PIL import Image, UnidentifiedImageError
        import pytesseract
        img=Image.open(io.BytesIO(data))
        if img.format not in {'PNG','JPEG'}:
            raise ReportError('Supported report images: PNG and JPEG only.')
        if img.width*img.height>18_000_000:
            raise ReportError('Image is too large for safe OCR.')
        if TESSERACT_CMD:
            pytesseract.pytesseract.tesseract_cmd=TESSERACT_CMD
        text=pytesseract.image_to_string(img.convert('RGB'),lang='eng')
    except ReportError:
        raise
    except Exception as exc:
        raise ReportError('Local image OCR unavailable or image unreadable. Install Tesseract OCR.') from exc
    if len(text.strip())<20:
        raise ReportError('OCR found too little readable text. Try a clearer image.')
    return text[:MAX_REPORT_CHARS],1


def extract_pdf(data: bytes) -> tuple[str, int]:
    if not data or len(data) > MAX_REPORT_BYTES:
        raise ReportError("PDF must be between 1 byte and 10 MB.")
    if not data.startswith(b"%PDF-"):
        raise ReportError("Only valid PDF files are accepted.")
    try:
        with pymupdf.open(stream=data, filetype="pdf") as doc:
            if doc.needs_pass:
                raise ReportError("Password-protected PDFs are not supported. Export an unlocked copy.")
            if len(doc) > MAX_REPORT_PAGES:
                raise ReportError(f"Maximum {MAX_REPORT_PAGES} pages per report. Please split the PDF.")
            parts = []
            for page in doc:
                raw = page.get_text("text", sort=True) or ""
                if len(raw.strip()) < 20 and ENABLE_OCR:
                    raw = _optional_ocr(page)
                parts.append(raw)
            text = "\n".join(parts)
    except ReportError:
        raise
    except (ValueError, RuntimeError, pymupdf.FileDataError) as exc:
        raise ReportError("PDF is damaged or could not be opened.") from exc
    if len(text.strip()) < 20:
        raise ReportError("No readable text found. This is likely a scanned PDF. Optional OCR needs Tesseract installed and ENABLE_OCR=true.")
    return text[:MAX_REPORT_CHARS], len(parts)


def _find_test(line: str):
    for label, aliases in TEST_NAMES:
        for alias in aliases:
            pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"
            found = re.search(pattern, line, re.I)
            if found:
                return label, line[found.end():].strip()
    return None, None


def _reference(rest_after_value: str):
    r = RANGE_RE.search(rest_after_value)
    if r:
        low, high = float(r.group(1).replace(",", ".")), float(r.group(2).replace(",", "."))
        if low < high:
            return low, high, None, f"{r.group(1)}–{r.group(2)}"
    less = LESS_RE.search(rest_after_value)
    if less:
        upper = float(less.group(1).replace(",", "."))
        return None, upper, "lt", f"<{less.group(1)}"
    more = MORE_RE.search(rest_after_value)
    if more:
        lower = float(more.group(1).replace(",", "."))
        return lower, None, "gt", f">{more.group(1)}"
    return None, None, None, ""


def analyze_labs(text: str) -> list[dict]:
    """Compare only where reference range is explicitly stated on the SAME line.

    This is a demo-oriented parser: it intentionally leaves ambiguous results unevaluated.
    All flagged lab values require confirmation against the original PDF.
    """
    parsed = []
    seen = set()
    for original in text.splitlines():
        line = " ".join(original.strip().split())
        if not (5 <= len(line) <= 230):
            continue
        test, suffix = _find_test(line)
        if not test:
            continue
        # Remove parenthetical common test labels before the value, but never substitute one.
        suffix = re.sub(r"^\s*\((?:25[- ]?OH|serum|plasma|fasting|SGOT|SGPT|ALT|AST)\)\s*", " ", suffix, flags=re.I)
        # Reject dangling reference-style fragments that precede a true value.
        if re.match(r"^\s*(?:range|reference|normal)\b", suffix, re.I):
            continue
        suffix = suffix.lstrip(" :\t|–-")
        match = VALUE_RE.search(suffix)
        if not match:
            continue
        try:
            value = float(match.group(1).replace(",", "."))
        except ValueError:
            continue
        # Reject impossible generic numeric noise, dates and inline pre-measurement range.
        if value < 0 or value > 100000:
            continue
        unit = (match.group(2) or "").strip()
        following = suffix[match.end():]
        lo, hi, operator, reference = _reference(following)
        status = "Not evaluated"
        if lo is not None and value < lo:
            status = "Low"
        elif hi is not None and value > hi:
            status = "High"
        elif reference:
            status = "Within stated range"
        # For exclusive bounds, equality does not satisfy the condition.
        if operator == "lt" and hi is not None:
            status = "Within stated range" if value < hi else "High"
        if operator == "gt" and lo is not None:
            status = "Within stated range" if value > lo else "Low"
        # If units are missing from immediately after value, look just before reference.
        if not unit:
            unit_found = re.search(UNIT, following, flags=re.I)
            if unit_found:
                unit = unit_found.group(0)
        key = (test, value, unit, reference)
        if key in seen:
            continue
        seen.add(key)
        parsed.append({"name": test, "value": value, "unit": unit or "unit not found",
                       "reference": reference, "status": status,
                       "warning": "Automated extraction; verify against the original lab report."})
    return parsed[:70]
