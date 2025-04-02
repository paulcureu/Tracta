import json
import os

# Schimbă cu calea către folderul tău cu fișiere JSON
json_folder = "./json_files"
output_file = "data-base.json"

combined_data = []

# Parcurge toate fișierele din folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(json_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    combined_data.extend(data)
                else:
                    combined_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Eroare la citirea fișierului {filename}: {e}")

# Scrie rezultatul într-un nou fișier
with open(output_file, "w", encoding="utf-8") as out_file:
    json.dump(combined_data, out_file, ensure_ascii=False, indent=2)

print(f"Fișierele au fost combinate cu succes în {output_file}.")
