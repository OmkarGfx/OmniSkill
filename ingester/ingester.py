import os
import shutil
import subprocess
import yaml
import json
import requests
import argparse
import re
from pathlib import Path

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.returncode == 0

def on_rm_error(func, path, exc_info):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def discover_remote_skills(query, limit=10):
    print(f"Searching for '{query}'...")
    # Using a high-performance discovery API
    url = f"https://skills.sh/api/search?q={query}&limit={limit}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        skills = data.get("skills", [])
        print(f"Found {len(skills)} skills")
        return skills
    except Exception as e:
        print(f"Failed to discover skills: {e}")
        return []

def parse_skill_md(md_content):
    """Simple regex parser for YAML frontmatter in SKILL.md."""
    frontmatter = {}
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', md_content, re.DOTALL)
    if match:
        yaml_content = match.group(1)
        try:
            frontmatter = yaml.safe_load(yaml_content)
        except Exception as e:
            print(f"Failed to parse SKILL.md YAML: {e}")
    return frontmatter

def find_skill_path(repo_path, skill_id, skill_name):
    """Try to find the directory containing the skill."""
    if (repo_path / skill_id).exists(): return repo_path / skill_id
    if (repo_path / skill_name).exists(): return repo_path / skill_name
    
    skills_dir = repo_path / "skills"
    if skills_dir.exists():
        if (skills_dir / skill_id).exists(): return skills_dir / skill_id
        if (skills_dir / skill_name).exists(): return skills_dir / skill_name
        for d in skills_dir.iterdir():
            if d.is_dir() and (skill_id in d.name or skill_name in d.name):
                return d
                
    for p in repo_path.rglob("SKILL.md"):
        if skill_id in p.parent.name or skill_name in p.parent.name:
            return p.parent
            
    return None

def ingest(force_query=None):
    config_path = Path("ingester/sources.yaml")
    if not config_path.exists():
        print("Config file not found!")
        return

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    temp_dir = Path("ingester/temp")
    if temp_dir.exists():
        shutil.rmtree(temp_dir, onerror=on_rm_error)
    temp_dir.mkdir(parents=True, exist_ok=True)

    skills_root = Path("skills")
    skills_root.mkdir(exist_ok=True)

    sources = config.get("sources", [])
    if force_query:
        sources = [{
            "name": f"Dynamic Search: {force_query}",
            "type": "skills_sh",
            "query": force_query,
            "limit": 10
        }]

    ingested_hashes = set()

    for source in sources:
        name = source["name"]
        stype = source.get("type", "general")
        
        print(f"\n--- Processing source: {name} ({stype}) ---")
        
        source_skills = []
        if stype == "discovery":
            skills_data = discover_remote_skills(source.get("query", "agent"), source.get("limit", 10))
            for s in skills_data:
                source_name = s.get("source")
                if not source_name: continue
                source_skills.append({
                    "name": s["name"],
                    "skillId": s.get("skillId"),
                    "url": f"https://github.com/{source_name}",
                    "tags": s.get("tags", [])
                })
        else:
            for sub in source.get("sub_paths", ["."]):
                source_skills.append({
                    "name": Path(sub).name if sub != "." else source["name"],
                    "url": source["url"],
                    "sub_path": sub
                })

        for s_info in source_skills:
            url = s_info["url"]
            repo_name = url.split("/")[-1].replace(".git", "")
            repo_path = temp_dir / repo_name
            
            # Use URL + skill name as a unique identifier for deduplication
            skill_id_full = f"{url}/{s_info.get('skillId', s_info['name'])}"
            if skill_id_full in ingested_hashes:
                print(f"Skipping duplicate: {s_info['name']}")
                continue
            ingested_hashes.add(skill_id_full)

            if not repo_path.exists():
                if not run_cmd(f"git clone --depth 1 {url} {repo_name}", cwd=temp_dir):
                    continue

            src_path = None
            if "sub_path" in s_info:
                src_path = repo_path / s_info["sub_path"]
            else:
                src_path = find_skill_path(repo_path, s_info["skillId"], s_info["name"])

            if not src_path or not src_path.exists():
                print(f"Could not find path for skill {s_info['name']} in {repo_name}")
                continue
            
            skill_name = s_info["name"]
            category = source.get("category", "community")
            dest_path = skills_root / category / skill_name
            
            print(f"Copying {skill_name} from {src_path} to {dest_path}...")
            if dest_path.exists():
                shutil.rmtree(dest_path, onerror=on_rm_error)
            
            shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            
            # Strip .git to avoid nested repo issues
            git_path = dest_path / ".git"
            if git_path.exists():
                shutil.rmtree(git_path, onerror=on_rm_error)
            
            # Metadata Enhancement
            metadata = {
                "name": skill_name,
                "category": category,
                "source_url": url,
                "supported_models": ["All"],
                "capabilities": [],
                "install_runtime": "npx"
            }

            skill_md_path = dest_path / "SKILL.md"
            if skill_md_path.exists():
                with open(skill_md_path, "r", encoding="utf-8") as f:
                    frontmatter = parse_skill_md(f.read())
                    if frontmatter:
                        metadata.update({
                            "description": frontmatter.get("description", ""),
                            "capabilities": frontmatter.get("allowed-tools", "").split(",") if isinstance(frontmatter.get("allowed-tools"), str) else []
                        })
            
            with open(dest_path / "skill.json", "w") as mf:
                json.dump(metadata, mf, indent=4)
                
            print(f"Successfully folderized {skill_name}")

    print("\nIngestion complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Universal Agent Skills Hub Ingester")
    parser.add_argument("--query", type=str, help="Force a search query to discovery new skills")
    args = parser.parse_args()
    
    ingest(force_query=args.query)
