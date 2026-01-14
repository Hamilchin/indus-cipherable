import json
import csv

"""
indus_symbols = {
    "1": {
        "frequencies": {
            "SOL": 127,
            "INI": 127,
            "MED": 127,
            "FIN": 127,
            "TOT": 127
        },
        "type": "basic",
        "human_interpretations": ["fish", "water", "aquatic"],
        "human_confidence": 0.9,
        "possible_proto_dravidian": ["*mīn", "*nīr"]
    },
    "2": {
        "type": "composite"
        "components": ["1", "2"]
    }
}
"""


def load_symbol_data(path="data/symbols.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_symbol_data(data, path="data/symbols.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def init_from_freq_csv(path="data/IM77_symbol_freq.csv"):
    indus_symbols = {}
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id = row[0]
            frequencies = {
                "SOL": row[1],
                "INI": row[2],
                "MED": row[3],
                "FIN": row[4],
                "TOT": row[5]
            }
            indus_symbols[id] = {"frequencies": frequencies}

    return indus_symbols


def print_symbol(symbol_id, symbol_data):
    """Display a symbol's data clearly."""
    print(f"\n{'='*50}")
    print(f"  SYMBOL: {symbol_id}")
    print(f"{'='*50}")
    
    freq = symbol_data.get("frequencies", {})
    print(f"  Frequencies: TOT={freq.get('TOT', '?')} | SOL={freq.get('SOL', '?')} INI={freq.get('INI', '?')} MED={freq.get('MED', '?')} FIN={freq.get('FIN', '?')}")
    
    conf = symbol_data.get("human_confidence")
    conf_str = f"{conf:.0%}" if conf is not None else "—"
    print(f"  Confidence: {conf_str}")
    
    interps = symbol_data.get("human_interpretations", [])
    if interps:
        print(f"  Interpretations: {', '.join(interps)}")
    else:
        print(f"  Interpretations: (none)")
    print(f"{'='*50}\n")


def repl():
    """Interactive REPL for managing symbol interpretations."""
    data = load_symbol_data()
    print(f"\n🔣 Loaded {len(data)} symbols.\n")
    
    while True:
        cmd = input(">>> ").strip()
        
        if not cmd:
            continue
        
        if cmd in ("q", "quit", "exit"):
            print("Goodbye.")
            break
        
        if cmd in ("h", "help"):
            print("""
Commands:
  <id>                  - View symbol by ID
  <id> i <words...>     - Add/remove interpretations (prefix with - to remove)
                          e.g., "234 i fish, ball, -shoe, -deer"
  <id> c <0-1>          - Set confidence (e.g., "1 c 0.8")
  list                  - List all symbols with interpretations
  q / quit              - Exit
""")
            continue
        
        if cmd == "list":
            has_interps = [(k, v) for k, v in data.items() if v.get("human_interpretations")]
            if not has_interps:
                print("No symbols have interpretations yet.")
            else:
                print(f"\n{'ID':<8} {'INTERPRETATIONS'}")
                print("-" * 40)
                for sid, sdata in sorted(has_interps, key=lambda x: int(x[0]) if x[0].isdigit() else x[0]):
                    interps = ", ".join(sdata.get("human_interpretations", []))
                    print(f"{sid:<8} {interps}")
                print()
            continue
        
        parts = cmd.split(maxsplit=1)
        symbol_id = parts[0]
        
        if symbol_id not in data:
            print(f"Symbol '{symbol_id}' not found.")
            continue
        
        # View only
        if len(parts) == 1:
            print_symbol(symbol_id, data[symbol_id])
            continue
        
        arg = parts[1].strip()
        
        # Set confidence: "<id> c <value>"
        if arg.startswith("c "):
            try:
                conf = float(arg[2:].strip())
                if not 0 <= conf <= 1:
                    print("Confidence must be between 0 and 1.")
                    continue
                data[symbol_id]["human_confidence"] = conf
                save_symbol_data(data)
                print(f"✓ Set confidence to {conf:.0%}")
            except ValueError:
                print("Invalid number. Use: <id> c <0-1>")
                continue
        
        # Add/remove interpretations: "<id> i <words...>"
        elif arg.startswith("i "):
            if "human_interpretations" not in data[symbol_id]:
                data[symbol_id]["human_interpretations"] = []
            interps = data[symbol_id]["human_interpretations"]
            
            words = [word.strip() for word in arg[2:].strip().split(",")]
            added, removed = [], []
            for w in words:
                if w.startswith("-"):
                    target = w[1:]
                    if target in interps:
                        interps.remove(target)
                        removed.append(target)
                else:
                    if w not in interps:
                        interps.append(w)
                        added.append(w)
            
            if added or removed:
                save_symbol_data(data)
                if added:
                    print(f"✓ Added: {', '.join(added)}")
                if removed:
                    print(f"✓ Removed: {', '.join(removed)}")
        
        else:
            print("Unknown command. Use 'h' for help.")
            continue
        
        print_symbol(symbol_id, data[symbol_id])


if __name__ == "__main__":
    repl()
