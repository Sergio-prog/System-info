from system_info import get_system_info
import json

info = get_system_info()
with open(f"{info['info']['system_info']['system']['comp_name']}_info.log", "w", encoding="utf-8") as f:
    json.dump(info, f, ensure_ascii=False, indent=4)
