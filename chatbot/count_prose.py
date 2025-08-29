import json

JSON_FILES = ["is_prose_url_markdown_tree_for_documentation.json", "is_prose_url_markdown_tree_for_home_page.json"]

total_true = 0
total_false = 0
file_stats = {}

for json_file in JSON_FILES:
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    true_count = sum(1 for item in data if item.get("is_prose") == True)
    false_count = sum(1 for item in data if item.get("is_prose") == False)
    
    file_stats[json_file] = {
        "true": true_count,
        "false": false_count,
        "total": len(data)
    }
    
    total_true += true_count
    total_false += false_count
    
    print(f"\n{json_file}:")
    print(f"  True:  {true_count}")
    print(f"  False: {false_count}")
    print(f"  Total: {len(data)}")

print("\n" + "="*50)
print("OVERALL SUMMARY:")
print(f"Total True:  {total_true}")
print(f"Total False: {total_false}")
print(f"Grand Total: {total_true + total_false}")
print(f"True %:      {total_true/(total_true + total_false)*100:.1f}%" if (total_true + total_false) > 0 else "N/A")
print("="*50)