import json
import re

JSON_FILES = ["url_markdown_tree_for_home_page.json", "url_markdown_tree_for_documentation.json"]

def remove_links(text):
    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
    # Remove bare URLs
    text = re.sub(r'https?://[^\s\)]+', '', text)
    # Remove image references ![alt](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    return text

for json_file in JSON_FILES:
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        false_entries = [item for item in data if item.get("is_prose") == False]
        
        if false_entries:
            print(f"\n=== {json_file} ===\n")
            
            for entry in false_entries:
                markdown = entry.get("markdown", "")
                clean_text = remove_links(markdown)
                print(clean_text)
                print("\n---\n")
                
    except FileNotFoundError:
        print(f"File not found: {json_file}")
    except Exception as e:
        print(f"Error processing {json_file}: {e}")