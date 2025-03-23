import json
import os

# Paths to your JSON files
app_json_file = "dependencies.json"
libs_json_file = "config/libs.json"


# Function to load dependencies from JSON
def load_dependencies(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as f:
            data = json.load(f)
        return data
    return []


# Load application dependencies
app_dependencies = load_dependencies(app_json_file)

# Load optional library dependencies, only if the file exists
optional_dependencies = load_dependencies(libs_json_file)

# Combine both dependencies (application first, then optional)
combined_dependencies = app_dependencies + optional_dependencies

# Write to requirements.txt
with open("requirements.txt", "w") as req_file:
    for dependency in combined_dependencies:
        req_file.write(f"{dependency['package']}=={dependency['version']}\n")

print("requirements.txt has been successfully generated!")
