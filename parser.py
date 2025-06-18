import re
import fitz 
import unicodedata
from datetime import datetime

def clean_text(text):
    """Cleans weird characters like Iâ€™m, â€“ etc."""
    cleaned = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    cleaned = cleaned.replace("Iâm", "I'm").replace("Iâ€™m", "I'm")
    cleaned = cleaned.replace("â€™", "'").replace("â€œ", '"').replace("â€", '"')
    cleaned = cleaned.replace("â€“", "-").replace("â€¦", "...")
    return cleaned

def extract_text_from_pdf(pdf_path):
    """Extract raw text from a PDF."""
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_name(text):
    lines = text.strip().split('\n')[:15]
    for line in lines:
        match = re.search(r"I['’`]?m\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", line)
        if match:
            return match.group(1)
        words = line.strip().split()
        if 1 < len(words) <= 4 and all(w[0].isupper() for w in words if w[0].isalpha()):
            return ' '.join(words)
    return "Not found"

def extract_contacts(text, pdf_path):
    contacts = {}

    email = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    contacts['Email'] = email[0] if email else "Not found"

    phone = re.findall(r"(?:\+91[\s\-]?)?\d{10}", text)
    contacts['Phone'] = phone[0] if phone else "Not found"

    text_cleaned = text.replace('\n', '')
    linkedin = re.search(r"https:\/\/(www\.)?linkedin\.com\/[^\s)]+", text_cleaned)
    github = re.search(r"https:\/\/(www\.)?github\.com\/[^\s)]+", text_cleaned)

    linkedin_url = linkedin.group(0) if linkedin else "Not found"
    github_url = github.group(0) if github else "Not found"

    doc = fitz.open(pdf_path)
    for page in doc:
        links = page.get_links()
        for link in links:
            uri = link.get("uri", "")
            if "linkedin.com" in uri:
                linkedin_url = uri
            elif "github.com" in uri:
                github_url = uri

    contacts['LinkedIn'] = linkedin_url
    contacts['GitHub'] = github_url

    return contacts

def extract_sections(text):
    sections = {
        "Skills": "Not found",
        "Experience": "Not found",
        "Education": "Not found",
        "Projects": "Not found"
    }

    section_aliases = {
        "Skills": ["Skills","Key skills"],
        "Experience": ["Experience","Working Experience","Work Experience","Internships","INTERNSHIPS"],
        "Education": ["Education", "Qualification"],
        "Projects": ["Projects", "Project"]
    }

    lines = text.splitlines()

    for i, line in enumerate(lines):
        for section in sections:
            if any(alias.lower() in line.lower() for alias in section_aliases[section]):
                collected = []
                for next_line in lines[i + 1:]:
                    clean_line = next_line.strip()
                    if any(clean_line.lower().startswith(s.lower()) for s in sections if s != section):
                        break
                    if clean_line and clean_line not in [".", "-"]:
                        collected.append(clean_line)
                content = " ".join(collected).strip()
                if content:
                    sections[section] = content
                break  
    return sections

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    text = clean_text(text) 

    now = datetime.now()
    uid = now.strftime('%Y/%m/%d/%H/%M/%S/') + f"{now.microsecond}"

    result = {
        "UID": uid,
        "Name": extract_name(text)
    }
    result.update(extract_contacts(text, pdf_path))
    result.update(extract_sections(text))
    return result
