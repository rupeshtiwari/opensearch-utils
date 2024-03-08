# GET /_cat/shards?format=json
import json

# Load shard allocation data from a file
with open("./shards.json", "r") as file:
    shards = json.load(file)

# Count primary and replica shards
primary_count = sum(1 for shard in shards if shard["prirep"] == "p")
replica_count = sum(1 for shard in shards if shard["prirep"] == "r")

print(f"Primary Shards: {primary_count}")
print(f"Replica Shards: {replica_count}")
