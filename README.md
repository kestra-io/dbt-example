## Orchestrate dbt with kestra
A lightweight sample dbt project building dbt models in the same Postgres database used as Kestra backend.

## Getting started

To spin up Kestra in Docker (including Postgres database), use the following commands:

```bash
docker-compose up -d
sleep 60 # wait a minute for the containers to start
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@kestra/git_sync.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@kestra/generate_dbt_flow.yaml
curl -X POST http://localhost:8080/api/v1/executions/company.myteam/git_sync?wait=true
curl -X POST http://localhost:8080/api/v1/executions/company.myteam/generate_dbt_flow?wait=true
curl -X POST http://localhost:8080/api/v1/executions/company.myteam/dbt_flow?wait=true
```

The `curl` commands will deploy and run flows that:
- sync dbt code from this GitHub repository to Kestra 
- dynamically generate Kestra tasks based on dbt models and tests

![kestra](kestra/flow_topology.png)

## Note

Note that DuckDB adapter is currently not supported as Kestra runs each dbt task in a stateless manner so sharing the same DuckDB database across dbt tasks is not supported using this approach. For DuckDB, try [this blueprint](https://kestra.io/blueprints/git/50-git-workflow-for-dbt-with-duckdb) instead.