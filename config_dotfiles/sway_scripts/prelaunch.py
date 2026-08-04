#!/usr/bin/env python3

import json
import os
import subprocess
import sys

def get_target(arg):
    path = arg.split()[0]
    return os.path.basename(path).lower()


def get_tree():
    tree = subprocess.run(["swaymsg", "-t", "get_tree"], capture_output=True, text=True)
    return json.loads(tree.stdout)


def count_instances(node, target):
    count = 0

    app_id = node.get("app_id") or ""
    app_class = node.get("window_properties", {}).get("class") or ""
    window_title = node.get("name") or ""

    if (
        target in app_id.lower()
        or target in app_class.lower()
        or target in window_title.lower()
    ):
        count += 1

    for sub in node.get("nodes", []) + node.get("floating_nodes", []):
        count += count_instances(sub, target)

    return count

def main():
    if len(sys.argv) < 3:
        sys.exit(1)
    app_cmd = sys.argv[1]
    workspace = sys.argv[2]

    app = get_target(app_cmd)
    tree = get_tree()

    instances = count_instances(tree, app)

    if instances == 0:
        subprocess.run(["swaymsg", f"workspace {workspace}"])
        subprocess.Popen(f"{app_cmd}", shell=True)
    else:
        subprocess.Popen(f"{app_cmd}", shell=True)


if __name__ == "__main__":
    main()