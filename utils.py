import json

with open("data/full_proto_dravidian.json", "r", encoding="utf-8") as f:
    data = json.load(f)

leads = [
            "bull",
            "bull horns",
            "pot",
            "container",
            "vessel",
            "storage",
            "crucible"
        ]



def get_roots(leads, dictionary):
    for entry in dictionary:
        root = 
        for lead in leads:
            x = find_instance_in_nested_dict(entry, lead)
            if x:
                print(f"With lead: {lead}, found root")
    return None
    

def find_instance_in_nested_dict(dict, lead):
    for key, value in dict.items():
        if type(value) == str:
            cleaned = ''.join(c if c.isalpha() or c in "-*" else ' ' for c in value)
            words = cleaned.lower().split()

            if lead.lower() in words:
                return value

        elif type(value) == dict:
            x = find_instance_in_nested_dict(value, lead)
            if x:
                return x
    return None
