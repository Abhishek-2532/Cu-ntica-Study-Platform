import os
import json

def main():
    # Relative paths for ease of use in workspace
    json_path = os.path.join("database", "courses.json")
    modules_dir = os.path.join("templates", "Modules")
    
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return
        
    if not os.path.exists(modules_dir):
        print(f"Error: {modules_dir} not found.")
        return
        
    with open(json_path, 'r', encoding='utf-8') as f:
        courses = json.load(f)
        
    slug_to_module = {
        "introduction-to-artificial-intelligence": "Module_1.html",
        "why-machine-learning": "Module_2.html",
        "classical-machine-learning": "Module_3.html",
        "why-quantum-computing": "Module_4.html",
        "quantum-computing-foundations": "Module_5.html",
        "intersection-machine-learning-and-quantum-computing": "Module_6.html",
        "why-quantum-machine-learning": "Module_7.html",
        "quantum-data-encoding": "Module_8.html",
        "quantum-machine-learning-algorithms": "Module_9.html",
        "quantum-machine-learning-capstone-projects": "Module_10.html"
    }
    
    injected_count = 0
    for course in courses:
        slug = course.get("slug")
        if slug in slug_to_module:
            filename = slug_to_module[slug]
            filepath = os.path.join(modules_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f_html:
                    html_content = f_html.read()
                html_content = html_content.strip()
                course["html_content"] = html_content
                injected_count += 1
                print(f"Loaded HTML for {slug} from {filename} ({len(html_content)} bytes)")
            else:
                print(f"Warning: File {filepath} not found for slug {slug}")
                
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2, ensure_ascii=False)
        
    print(f"\nSUCCESS: Injected HTML content for {injected_count} courses in courses.json.")

if __name__ == "__main__":
    main()
