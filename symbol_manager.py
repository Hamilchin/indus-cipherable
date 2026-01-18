import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


"""
indus_symbols = {
    "1": {
        "type": "basic",
        "interpretations": ["fish", "water", "aquatic"],
        "confidence": 0.9,
        "possible_proto_dravidian": ["*mīn", "*nīr"]
    },
    "2": {
        "type": "composite"
        "components": ["1", "2"]z
    }
}
"""


def load_symbol_data(path="data/symbols.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_symbol_data(data, path="data/symbols.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# def init_from_freq_csv(path="data/IM77_symbol_freq.csv"):
#     indus_symbols = {}
#     with open(path, "r", encoding="utf-8") as f:
#         reader = csv.reader(f)
#         next(reader)
#         for row in reader:
#             id = row[0]
#             frequencies = {
#                 "SOL": row[1],
#                 "INI": row[2],
#                 "MED": row[3],
#                 "FIN": row[4],
#                 "TOT": row[5]
#             }
#             indus_symbols[id] = {"frequencies": frequencies}

#     return indus_symbols

def show_symbols(sids):
    images, labels = [], []
    for sid in sids:
        path = Path(f"data/symbol_images/{sid}.gif")
        if not path.exists():
            print(f"Warning: {path} not found")
            continue
        images.append(mpimg.imread(path))
        labels.append(sid)
    if not images:
        return
    ratios = [img.shape[1] / img.shape[0] for img in images]
    fig, axes = plt.subplots(1, len(images), figsize=(sum(ratios) * 1.2, 1.2),
                             gridspec_kw={"width_ratios": ratios, "wspace": 0.05})
    if len(images) == 1:
        axes = [axes]
    for ax, img, label in zip(axes, images, labels):
        ax.imshow(img, cmap="gray")
        ax.set_xlabel(label, fontsize=8)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
    plt.show()

def repl():
    def print_symbol(sid):
        if sid not in data:
            print(f"Symbol {sid} not found.")
            return
        print(f"\n=== Symbol {sid} ===")
        for k, v in data[sid].items():
            if v: 
                print(f"  {k}: {v}")
        print()

    def parse_list_arg(arg):
        to_add, to_remove = [], []
        for item in arg.split(","):
            item = item.strip()
            if not item:
                continue
            if item.startswith("-"):
                to_remove.append(item[1:].strip())
            else:
                to_add.append(item)
        return to_add, to_remove

    try:
        data = load_symbol_data()
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    while True:
        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not cmd:
            continue
        if cmd in ("q", "quit", "exit"):
            break

        if cmd == "help":
            print("""
Commands:
  <id>                       — View symbol properties
  show <id> [id2] ...        — Display symbols in a window
  <id> interpretations a,b,-c — Add/remove interpretations (- prefix removes)
  <id> confidence <0-1>      — Set confidence level
  <id> type <type>           — Set symbol type
  <id> components a,b,-c     — Add/remove components (- prefix removes)
  list                       — List all symbols
  help                       — Show this help
  q / quit / exit            — Exit
""")
            continue

        if cmd == "list":
            for sid in data:
                print_symbol(sid)
            continue

        if cmd.startswith("show "):
            show_symbols(cmd.split()[1:])
            continue

        parts = cmd.split(maxsplit=2)
        sid = parts[0]

        if len(parts) == 1:
            print_symbol(sid)
            continue

        action, arg = parts[1], parts[2] if len(parts) > 2 else ""
        if sid not in data:
            data[sid] = {}
        sym = data[sid]

        if action == "interpretations":
            current = sym.get("interpretations", [])
            to_add, to_remove = parse_list_arg(arg)
            current = [x for x in current if x not in to_remove]
            current.extend(x for x in to_add if x not in current)
            sym["interpretations"] = current

        elif action == "confidence":
            sym["confidence"] = float(arg)

        elif action == "type":
            sym["type"] = arg

        elif action == "components":
            current = sym.get("components", [])
            to_add, to_remove = parse_list_arg(arg)
            current = [x for x in current if x not in to_remove]
            current.extend(x for x in to_add if x not in current)
            sym["components"] = current

        else:
            print(f"Unknown action: {action}")
            continue

        save_symbol_data(data)
        print_symbol(sid)


if __name__ == "__main__":
    repl()