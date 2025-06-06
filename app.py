from flask import Flask, render_template, request
import os
import json
from werkzeug.utils import secure_filename
from resume_info import parse_resume_content, save_to_json, save_to_csv

# Instantiate the Flask application
application = Flask(__name__)

# Directory paths for file handling
RESUME_STORAGE = '/app/resumes'
OUTPUT_STORAGE = '/app/results'

# Ensure necessary folders are available
for folder in [RESUME_STORAGE, OUTPUT_STORAGE]:
    os.makedirs(folder, exist_ok=True)

# Set the upload destination in the app config
application.config['UPLOAD_FOLDER'] = RESUME_STORAGE

@application.route('/', methods=['GET', 'POST'])
def home():
    extracted_data = None

    # When a file is submitted via form
    if request.method == 'POST':
        uploaded_file = request.files.get('resume')

        if uploaded_file and uploaded_file.filename.lower().endswith('.pdf'):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(application.config['UPLOAD_FOLDER'], filename)
            uploaded_file.save(filepath)

            # Analyze the uploaded resume
            extracted_data = parse_resume_content(filepath)

            # Store individual resume output
            individual_output_path = os.path.join(OUTPUT_STORAGE, f"{filename}.json")
            with open(individual_output_path, 'w') as f:
                json.dump(extracted_data, f, indent=2)

            # Update cumulative storage files
            save_to_json(extracted_data)
            save_to_csv(extracted_data)

            return render_template('index.html', data=extracted_data, uploaded=True)

    return render_template('index.html', data=extracted_data)

@application.route('/results', methods=['GET'])
def view_results():
    resumes = []
    keyword = request.args.get('keyword', '').lower().strip()

    try:
        if not os.path.exists(OUTPUT_STORAGE):
            return render_template('results.html', results=[], keyword=keyword)

        for file in os.listdir(OUTPUT_STORAGE):
            if file.endswith('.json') and not file.startswith('resumes_data'):
                with open(os.path.join(OUTPUT_STORAGE, file), 'r') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        resumes.append(data)

        # Apply filtering logic if a search keyword is provided
        if keyword:
            resumes = [
                r for r in resumes
                if keyword in r.get('skills', '').lower() or
                   keyword in r.get('experience', '').lower()
            ]

    except Exception as e:
        return render_template('results.html', results=[], keyword=keyword, error=str(e))

    return render_template('results.html', results=resumes, keyword=keyword)

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)
