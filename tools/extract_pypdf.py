from pypdf import PdfReader
import json
import re

def parse_pdf_pypdf_v2(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    # Save raw text for debug if needed
    with open("raw_text_debug.txt", "w") as f:
        f.write(text)

    data = {
        "name": "Cyrus Chua", 
        "tagline": "Security Engineer", # Default/fallback
        "about": "",
        "experience": [],
        "education": [],
        "skills": [],
        "contact": {}
    }

    # 1. Extract Tagline / Current Role
    # Look for the line under Name or near top
    # In the raw output we saw "He/Him\nSecurity Engineering @ Gusto"
    # We can try to grab that.
    tagline_match = re.search(r'He/Him\s+(.*?)\s+San Francisco', text, re.DOTALL)
    if tagline_match:
         data["tagline"] = tagline_match.group(1).replace('\n', ' ').strip()

    # 2. Extract About
    # We saw "About\n- Seasoned infosec professional..."
    # Ends usually at "Experience" or "Activity"
    about_match = re.search(r'About\s*\n(.*?)(?=\nExperience|\nActivity|\nEducation)', text, re.DOTALL)
    if about_match:
        data["about"] = about_match.group(1).replace('\n', ' ').strip()

    # 3. Extract Experience
    # This is the hardest part. Usually layout is:
    # Company Name\nTitle\nDates
    # We will do a loose search for blocks that look like jobs
    # "Security Engineering @ Gusto" suggests Gusto is a company.
    
    # Let's try to capture sections between "Experience" and "Education"
    exp_section_match = re.search(r'Experience\s*\n(.*?)(?=\nEducation|\nSkills)', text, re.DOTALL)
    if exp_section_match:
        exp_text = exp_section_match.group(1)
        # Split by known companies or just structure
        # Heuristic: Lines that look like dates "Jan 2020 - Present"
        date_pattern = r'([A-Z][a-z]{2}\s\d{4}\s-\s(?:Present|[A-Z][a-z]{2}\s\d{4}))'
        
        # Split text by date patterns to isolate jobs
        jobs = re.split(date_pattern, exp_text)
        
        # This split results in [Title/Company parts, DATE, Desc parts, DATE, Desc parts...]
        # It's messy but we can reconstruct loosely
        
        current_job = {}
        for i in range(1, len(jobs), 2):
            period = jobs[i].strip()
            # The part BEFORE the date usually contains Title and Company
            pre_date = jobs[i-1].strip().split('\n')
            title = pre_date[-2] if len(pre_date) > 1 else pre_date[-1] if pre_date else "Security Role"
            company = pre_date[-3] if len(pre_date) > 2 else "Unknown Company"
            
            # The part AFTER the date is the description (until next job)
            desc = jobs[i+1].strip()
            # Clean up desc - remove location lines usually
            desc_lines = [l for l in desc.split('\n') if "yrs" not in l and "mos" not in l and "Francisco" not in l]
            clean_desc = " ".join(desc_lines)[:300] + "..."
            
            data["experience"].append({
                "title": title,
                "company": company,
                "period": period,
                "description": clean_desc
            })

    # 4. Extract Skills
    # In LinkedIn PDF, skills are often at the bottom or separate section
    # "Top Skills" or just "Skills"
    skills_match = re.search(r'Skills\s*\n(.*?)(?=\nLanguages|\nInterests|$)', text, re.DOTALL)
    if skills_match:
        raw_skills = skills_match.group(1)
        # LinkedIn often lists them one per line or dot separated
        extracted_skills = [s.strip() for s in re.split(r'[\n•]', raw_skills) if len(s.strip()) > 2]
        # Remove garbage
        data["skills"] = [s for s in extracted_skills if "Page" not in s and "LinkedIn" not in s][:20]

    return data

if __name__ == "__main__":
    try:
        data = parse_pdf_pypdf_v2("Cyrus C. _ LinkedIn.pdf")
        with open("parsed_profile.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
