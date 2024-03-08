# GET /_cat/allocation?format=json

import json

# Load JSON data from a file
with open("./allocation.json", "r") as file:
    data = json.load(file)

# Initialize variables to accumulate totals
total_disk_avail = 0
total_disk_used = 0
total_disk = 0


# Function to convert human-readable sizes to bytes
def convert_to_bytes(size):
    # Mapping for size units including single-letter abbreviations
    size_units = {
        "b": 1,
        "k": 1024,
        "kb": 1024,
        "m": 1024**2,
        "mb": 1024**2,
        "g": 1024**3,
        "gb": 1024**3,
        "t": 1024**4,
        "tb": 1024**4,
    }
    numeric_part, unit = "", ""
    for char in size:
        if char.isdigit() or char == ".":  # Allow for numeric part including decimal
            numeric_part += char
        else:
            unit += char  # Build unit from letters

    # Adjust single-letter unit to their full equivalent (e.g., 't' to 'tb')
    if len(unit) == 1 and unit in {"k", "m", "g", "t"}:
        unit += "b"

    unit = unit.lower()  # Ensure unit is in lowercase
    if unit in size_units:
        # Convert numeric part to float, multiply by unit multiplier, and cast to int
        return int(float(numeric_part) * size_units[unit])
    else:
        # Raise an error if the unit is not recognized
        raise ValueError(f"Unknown size unit in '{size}'")


# Process each node's data
for node in data:
    total_disk_avail += convert_to_bytes(node["disk.avail"])
    total_disk_used += convert_to_bytes(node["disk.used"])
    total_disk += convert_to_bytes(node["disk.total"])

# Calculate total free disk space
total_disk_free = total_disk_avail

# Assuming total_disk and total_disk_used are in bytes for high precision
disk_utilization_percent = (total_disk_used / total_disk) * 100 if total_disk > 0 else 0


# Print results with guidelines for disk utilization
print(f"Total Disk Available: {total_disk_avail / (1024**4):.2f} TB")
print(f"Total Disk Used: {total_disk_used / (1024**3):.2f} GB")
print(f"Total Free Space: {total_disk_free / (1024**4):.2f} TB")
print(f"Disk Utilization: {disk_utilization_percent:.6f}%")

# Adding guideline statements
print("\nGuidelines:")
print(
    "A common practice is to aim for 60-80% disk utilization. This helps ensure there's enough room for unexpected data growth while making efficient use of the storage capacity. It's crucial to avoid reaching 100% utilization, as this can lead to performance degradation and operational issues."
)
print(
    "If the disk utilization consistently remains below 40%, consider downgrading the storage or optimizing node configurations with lower EBS (Elastic Block Store) volumes to reduce costs without compromising on performance or data integrity."
)
print(
    "Regular monitoring and proactive planning based on utilization trends are essential for maintaining optimal performance and cost efficiency."
)
