import json

def strip_keys(obj):
    """Recursively strip whitespace from dictionary keys."""
    if isinstance(obj, dict):
        return {k.strip(): strip_keys(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strip_keys(item) for item in obj]
    return obj

if __name__ == "__main__":
    with open("data/full_proto_dravidian.json", "r") as f:
        data = json.load(f)
    
    cleaned = strip_keys(data)
    
    with open("data/full_proto_dravidian.json", "w") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
    
    print("Done. Keys stripped.")

