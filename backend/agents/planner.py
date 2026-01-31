import re
from typing import Dict, Any


def run_planner_agent(contract_text: str) -> Dict[str, Any]:


   
    project_name = "Unnamed Road Project"
    total_segments = 10
    milestone_percentage = 50
    milestone_deadline = "2026-06-30"

    text_lower = contract_text.lower()

    
    name_match = re.search(r"project\s*title\s*:\s*(.+)", contract_text, re.IGNORECASE)
    if name_match:
        project_name = name_match.group(1).strip() 
# length->segments, percent->milestone_percentage, deadline->milestone_deadline
    
    length_match = re.search(r"(\d+)\s*km", text_lower)
    if length_match:
        total_segments = int(length_match.group(1))

    
    percent_match = re.search(r"(\d+)\s*%", text_lower)
    if percent_match:
        milestone_percentage = int(percent_match.group(1))

  
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", contract_text)
    if date_match:
        milestone_deadline = date_match.group(0)

    # output structured plan
    return {
        "project_name": project_name,
        "total_segments": total_segments,
        "milestones": [
            {
                "percentage": milestone_percentage,
                "deadline": milestone_deadline
            }
        ]
    }
