import json
import subprocess
import os
from ruamel.yaml import YAML

# Step 1: Run dbt deps to install dependencies
subprocess.run(["dbt", "deps"], check=True)

# Step 2: Compile the dbt project
subprocess.run(["dbt", "compile"], check=True)

# Step 3: Load the generated manifest.json file
manifest_path = "target/manifest.json"
with open(manifest_path) as f:
    manifest = json.load(f)

# Step 4: Extract models and their dependencies from the manifest
nodes = manifest["nodes"]
models = {k: v for k, v in nodes.items() if v["resource_type"] == "model"}

# Step 5: Generate Kestra tasks
kestra_tasks = []

def create_kestra_task(node_id, node):
    # Run `dbt deps` before each `dbt run` to ensure dependencies are installed
    dbt_command = f"dbt deps && dbt run --models {node['name']}"
    task = {
        "id": node["name"],
        "type": "io.kestra.plugin.dbt.cli.DbtCLI",
        "commands": [dbt_command]
    }
    return task

# Add model tasks (each task will first run `dbt deps` before `dbt run`)
for node_id, node in models.items():
    task = create_kestra_task(node_id, node)
    task_entry = {"task": task}
    depends_on = [dep.split(".")[-1] for dep in node["depends_on"]["nodes"] if dep in models]
    if depends_on:
        task_entry["dependsOn"] = depends_on
    kestra_tasks.append(task_entry)

# Step 6: Add a single `dbt test` task for the entire project, to be executed after all models are run
dbt_test_task = {
    "id": "dbt_test",
    "type": "io.kestra.plugin.dbt.cli.DbtCLI",
    "commands": ["dbt test"]
}

# Ensure `dbt test` runs after all model runs are completed
kestra_tasks.append({
    "task": dbt_test_task,
    "dependsOn": [task['task']['id'] for task in kestra_tasks]  # Depends on all model tasks
})

# Step 7: Generate the Kestra flow YAML with the correct order and indentation
kestra_flow = {
    "id": os.getenv('DBT_FLOW_ID', "dbt_flow"),
    "namespace": os.getenv('DBT_FLOW_NAMESPACE', "company.myteam"),
    "tasks": [
        {
            "id": "deps_seed",
            "type": "io.kestra.plugin.dbt.cli.DbtCLI",
            "commands": [
                "dbt deps",  # Make sure dbt deps runs before dbt seed
                "dbt seed"
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