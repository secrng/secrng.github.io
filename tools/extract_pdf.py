from pdfminer.high_level import extract_text
import re
import json

def parse_linkedin_pdf(pdf_path):
    text = extract_text(pdf_path)
    
    # Very basic parsing logic customized for LinkedIn PDFs
    data = {
        "name": "Cyrus Chua", # Fallback, though we know it
        "contact": {},
        "about": "",
        "experience": [],
        "education": [],
        "skills": []
    }

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        data["contact"]["email"] = email_match.group(0)

    # Simple heuristic to find sections (LinkedIn PDFs usually have headers)
    # This is a best-effort parser
    lines = text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if "Experience" in line and len(line) < 15:
            current_section = "experience"
            continue
        elif "Education" in line and len(line) < 15:
            current_section = "education"
            continue
        elif "Summary" in line or "About" in line:
            current_section = "about"
            continue
        elif "Skills" in line:
            current_section = "skills"
            continue

        if current_section == "about":
            data["about"] += line + " "
        elif current_section == "experience":
            # Just collecting raw lines for now to avoid losing data
            data["experience"].append(line)
        elif current_section == "education":
            data["education"].append(line)
        elif current_section == "skills":
            # LinkedIn skills are often dot separated or newline separated
            if "•" in line or len(line) < 30:
                 data["skills"].append(line.replace("•", "").strip())

    return data

if __name__ == "__main__":
    try:
        data = parse_linkedin_pdf("Cyrus C. _ LinkedIn.pdf")
        with open("parsed_profile.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
