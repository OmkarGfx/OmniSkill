import os
import shutil
import subprocess
import yaml
import json
import requests
import argparse
import re
import datetime
import threading
import time
import random
from pathlib import Path

PROGRESS = {"total": 0, "current_skill": "", "last_update": ""}
TOTAL_COUNT = 0
TARGET = 10000
INGESTED_HASHES = set()

def update_status(total, current):
    PROGRESS["total"] = total
    PROGRESS["current_skill"] = current
    PROGRESS["last_update"] = datetime.datetime.now().isoformat()
    with open("status.json", "w") as f:
        json.dump(PROGRESS, f, indent=4)

def on_rm_error(func, path, exc_info):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def discover_remote_skills(query, limit=100, offset=0):
    url = f"https://skills.sh/api/search?q={query}&limit={limit}&offset={offset}"
    try:
        time.sleep(3) # Heavy search delay
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json().get("skills", [])
    except Exception:
        pass
    return []

def download_skill_direct(skill_id):
    url = f"https://skills.sh/api/download/{skill_id}"
    try:
        time.sleep(5) # Fixed survivor delay (Ensures we never hit 429)
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"!!! Still limited on {skill_id}. Retrying after 2-minute cool-down...")
            time.sleep(120)
            return download_skill_direct(skill_id)
    except Exception:
        pass
    return None

def process_skill(s, category, skills_root):
    global TOTAL_COUNT
    try:
        skill_name = s["name"]
        sid = s.get("id")
        if not sid or sid in INGESTED_HASHES: return
        
        INGESTED_HASHES.add(sid)
        print(f"[{TOTAL_COUNT}/{TARGET}] Person Mode: Harvesting {sid}...")
        
        data = download_skill_direct(sid)
        if data and "files" in data:
            dest_path = skills_root / category / skill_name
            if dest_path.exists():
                shutil.rmtree(dest_path, onerror=on_rm_error)
            dest_path.mkdir(parents=True, exist_ok=True)
            
            for f_info in data["files"]:
                fpath = dest_path / f_info["path"]
                fpath.parent.mkdir(parents=True, exist_ok=True)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(f_info["contents"])
            
            # Simple metadata
            meta = {"name": skill_name, "category": category, "source_url": sid}
            with open(dest_path / "skill.json", "w") as mf:
                json.dump(meta, mf, indent=4)
            
            TOTAL_COUNT += 1
            update_status(TOTAL_COUNT, skill_name)
    except Exception as e:
        print(f"Error: {e}")

def survivor_harvest():
    global TOTAL_COUNT
    skills_root = Path("skills")
    comm_root = skills_root / "community"
    
    if comm_root.exists():
        TOTAL_COUNT = len([d for d in comm_root.iterdir() if d.is_dir()])
    
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
    combinations = [a+b for a in alphabet for b in alphabet]
    random.shuffle(combinations) # Keep results interesting
    
    print(f"Starting Survivor Mode (Single-Threaded). Target: {TARGET}. Current: {TOTAL_COUNT}")

    for q in combinations:
        if TOTAL_COUNT >= TARGET: break
        
        print(f"--- Sweeping query: '{q}' ---")
        for offset in [0, 100, 200]:
            if TOTAL_COUNT >= TARGET: break
            skills = discover_remote_skills(q, limit=100, offset=offset)
            if not skills: break
                
            for s in skills:
                process_skill(s, "community", skills_root)
                if TOTAL_COUNT >= TARGET: break
    
    print(f"Harvest complete. Final count: {TOTAL_COUNT}")

if __name__ == "__main__":
    survivor_harvest()
