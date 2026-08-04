#!/usr/bin/env python3

import json
import subprocess
import sys

def get_focused(node):
    if node.get("focused"):
        return node
    for sub in node.get("nodes", []) + node.get("floating_nodes", []):
        focused = get_focused(sub)
        if focused:
            return focused
    return None

def get_id(node):
    if not node:
        return None
    return node.get("app_id") or node.get("window_properties", {}).get("class")

def count_instances(node, target):
    count = 0

    current = get_id(node)

    if current and current.lower() == target.lower():
        count += 1
    for sub in node.get("nodes", []) + node.get("floating_nodes", []):
        count += count_instances(sub, target)

    return count

def main():
    if len(sys.argv) < 2:
        sys.exit(1)
    workspace = sys.argv[1]

    result = subprocess.run(
        ["swaymsg", "-t", "get_tree"], capture_output=True, text=True
    )
    
    tree = json.loads(result.stdout)
    focused = get_focused(tree)

    if focused:
        target = get_id(focused)

        if target:
            instances = count_instances(tree, target)
            
            if instances == 1:
                subprocess.run(["swaymsg", f"move container to workspace {workspace}"])

if __name__ == "__main__":
    main()