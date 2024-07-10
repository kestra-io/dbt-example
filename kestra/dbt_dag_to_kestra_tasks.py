import json
import subprocess
import os
from ruamel.yaml import YAML

# Step 1: Compile the dbt project
subprocess.run(["dbt", "compile"], check=True)

# Step 2: Load the generated manifest.json file
manifest_path = "target/manifest.json"
with open(manifest_path) as f:
    manifest = json.load(f)

# Step 3: Extract models and their dependencies from the manifest
nodes = manifest["nodes"]
models = {k: v for k, v in nodes.items() if v["resource_type"] == "model"}
tests = {k: v for k, v in nodes.items() if v["resource_type"] == "test"}

# Step 4: Generate Kestra tasks
kestra_tasks = []

def create_kestra_task(node_id, node, command_type):
    dbt_command = f"dbt {command_type} --models {node['name']}"
    task = {
        "id": node["name"],
        "type": "io.kestra.plugin.dbt.cli.DbtCLI",
        "commands": [dbt_command]
    }
    return task

# Add model tasks
for node_id, node in models.items():
    task = create_kestra_task(node_id, node, "run")
    task_entry = {"task": task}
    depends_on = [dep.split(".")[-1] for dep in node["depends_on"]["nodes"] if dep in models]
    if depends_on:
        task_entry["dependsOn"] = depends_on
    kestra_tasks.append(task_entry)

# Add test tasks
for node_id, node in tests.items():
    task = create_kestra_task(node_id, node, "test")
    task_entry = {"task": task}
    depends_on = [dep.split(".")[-1] for dep in node["depends_on"]["nodes"] if dep in models]
    if depends_on:
        task_entry["dependsOn"] = depends_on
    kestra_tasks.append(task_entry)

# Step 5: Generate the Kestra flow YAML with the correct order and indentation
kestra_flow = {
    "id": os.getenv('DBT_FLOW_ID', "dbt_flow"),
    "namespace": os.getenv('DBT_FLOW_NAMESPACE', "company.myteam"),
    "tasks": [
        {
            "id": "seed_deps",
            "type": "io.kestra.plugin.dbt.cli.DbtCLI",
            "commands": [
                "dbt seed",
                "dbt deps"
            ]
        },
        {
            "id": "dag",
            "type": "io.kestra.plugin.core.flow.Dag",
            "tasks": kestra_tasks
        }
    ]
}

# Add pluginDefaults with a preceding newline
adapter = os.getenv('DBT_ADAPTER', "dbt-postgres")
plugin_defaults = {
    "pluginDefaults": [
        {
            "type": "io.kestra.plugin.dbt.cli.DbtCLI",
            "forced": True,
            "values": {
                "warningOnStdErr": False,
                "parseRunResults": False,
                "beforeCommands": [
                    f"pip install -q {adapter}"
                ],
                "namespaceFiles": {
                    "enabled": True
                },
                "taskRunner": {
                    "type": "io.kestra.plugin.core.runner.Process"
                }
            }
        }
    ]
}

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

output_path = "kestra_flow.yaml"
with open(output_path, "w") as f:
    yaml.dump(kestra_flow, f)
    f.write("\n")
    yaml.dump(plugin_defaults, f)

print(f"Kestra flow YAML has been generated and saved to {output_path}")
