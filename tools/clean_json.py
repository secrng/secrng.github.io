import json
import re

def clean_profile():
    with open('parsed_profile.json', 'r') as f:
        data = json.load(f)

    # Clean Experience
    new_experience = []
    for job in data.get('experience', []):
        title = job.get('title', '')
        company = job.get('company', '')
        desc = job.get('description', '')
        
        # heuristic: if title is super long, it's probably a description
        if len(title) > 100:
            desc = title + " " + desc
            title = "Security Professional" # Fallback
            
        # Clean company if it is "Unknown" but title has "Gusto" or "Yahoo"
        if "Unknown" in company:
            if "Gusto" in title: company = "Gusto"
            elif "Yahoo" in title or "Oath" in title: company = "Yahoo / Verizon Media"
            elif "GovTech" in desc: company = "GovTech Singapore"
            
        # Clean Title (remove junk like "Full-time")
        title = title.split("·")[0].strip()
        
        new_experience.append({
            "title": title,
            "company": company,
            "period": job.get('period', ''),
            "description": desc[:500] # Truncate massive descriptions
        })
        
    data['experience'] = new_experience
    
    # Clean Skills (remove garbage)
    clean_skills = []
    for s in data.get('skills', []):
        if len(s) < 30 and "Show all" not in s and "http" not in s:
            clean_skills.append(s)
    data['skills'] = list(set(clean_skills))[:20]

    with open('parsed_profile.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    clean_profile()
