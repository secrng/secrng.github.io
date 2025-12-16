import json
import re

def parse_strings_output(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    data = {
        "name": "Cyrus Chua",
        "contact": {"email": "contactme@cyruschua.com", "linkedin": "https://www.linkedin.com/in/cyruschua/"},
        "about": "",
        "experience": [],
        "education": [],
        "skills": []
    }

    # Very heuristic parsing of raw strings
    # We look for blocks of text that look like job descriptions
    
    buffer = []
    capture_mode = None
    
    for line in lines:
        line = line.strip()
        if len(line) < 3: continue
        
        # Heuristics
        if "Experience" in line:
            capture_mode = "experience"
            continue
        if "Education" in line:
            capture_mode = "education"
            continue
        if "Skills" in line:
            capture_mode = "skills"
            continue
            
        if capture_mode == "experience":
            # Filter out UI elements from PDF
            if any(x in line for x in ["Page", "LinkedIn", "www.", ".com"]): continue
            # If line is substantial, treat as job/desc
            if len(line) > 20: 
                 data["experience"].append({"description": line, "title": "Experience", "company": "", "period": ""})
        
        elif capture_mode == "skills":
             if len(line) < 40 and "Page" not in line:
                 data["skills"].append(line)

    # Cleanup skills
    data["skills"] = list(set(data["skills"]))[:12] # Limit to 12 unique
    
    return data

if __name__ == "__main__":
    try:
        data = parse_strings_output("raw_pdf_strings.txt")
        with open("parsed_profile.json", "w") as f:
            json.dump(data, f, indent=2)
        print("Success")
    except Exception as e:
        print(f"Error: {e}")
