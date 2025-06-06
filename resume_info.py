import fitz  # PyMuPDF
import re
from typing import Dict, List
import json
import csv
import os

def parse_resume_content(pdf_path: str) -> Dict[str, str]:
    try:
        # Load PDF content
        document = fitz.open(pdf_path)
        full_text = "".join(page.get_text() for page in document)

        # Extract lines
        text_lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        candidate_name = text_lines[0] if text_lines else "Unknown"

        # Extract email
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_match = re.search(email_pattern, full_text)
        candidate_email = email_match.group(0) if email_match else "Unknown"

        # Extract phone
        phone_pattern = r'\+?\d[\d\s\-]{8,15}'
        phone_match = re.search(phone_pattern, full_text)
        candidate_phone = phone_match.group(0) if phone_match else "Unknown"

        # Extract sections
        skills_content = fetch_section_content(full_text, [
            'Skills', 'Technical Skills', 'Programming Languages', 'Technologies', 'Relevant Coursework', 'Core Competencies', 'Tools', 'Platforms'
        ])
        experience_content = fetch_section_content(full_text, [
            'Experience', 'Work Experience', 'Professional Experience', 'Internship', 'Employment History'
        ])

        return {
            "name": candidate_name,
            "email": candidate_email,
            "phone": candidate_phone,
            "skills": skills_content,
            "experience": experience_content
        }

    except Exception as error:
        return {
            "name": "Error",
            "email": f"Error: {str(error)}",
            "phone": "Error",
            "skills": "Error",
            "experience": "Error"
        }

def fetch_section_content(text: str, headers: List[str]) -> str:
    try:
        # Combine headers into a regex pattern
        header_pattern = r'(?i)(' + '|'.join(headers) + r')\s*[:\n]*\s*(.*?)(?=\n[A-Z][^\n]{1,100}\n|\Z)'
        matches = re.findall(header_pattern, text, re.DOTALL)

        if not matches:
            return "Unknown"

        content = " ".join(match[1].strip() for match in matches)

        # Clean up extracted text
        content = re.sub(r'\s*[-•*]\s*', ' ', content)  # Remove bullet points
        content = re.sub(r'\s+', ' ', content)  # Normalize spacing
        content = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', content)  # Remove emails
        content = re.sub(r'\+?\d[\d\s\-]{8,15}', '', content)  # Remove phone numbers
        content = re.sub(r'\d{4}\s*[-–]\s*(?:\d{4}|present|current)', '', content, flags=re.IGNORECASE)  # Remove years

        return content.strip() or "Unknown"

    except Exception as error:
        print(f"Section extraction error: {str(error)}")
        return "Unknown"

def save_to_json(data: Dict[str, str], filename: str = "/app/resumes_data.json"):
    try:
        existing_data = []

        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []

        existing_data.append(data)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2)

    except Exception as e:
        print(f"Error saving to JSON: {str(e)}")

def save_to_csv(data: Dict[str, str], filename: str = "/app/results/resumes_data.csv"):
    try:
        file_exists = os.path.exists(filename)
        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["name", "email", "phone", "skills", "experience"])
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
