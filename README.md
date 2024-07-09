A lightweight sample dbt project to test executing it from a Kestra dbt plugin

### Using the starter project

Try running the following commands:
- dbt run
- dbt test

### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


```bash
docker-compose up -d
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@git_sync.yaml
curl -X POST http://localhost:8080/api/v1/flows/import -F fileUpload=@generate_dbt_flow.yaml
curl -X POST http://localhost:8080/api/v1/executions/company.myteam/git_sync?wait=true
curl -X POST http://localhost:8080/api/v1/executions/company.myteam/generate_dbt_flow?wait=true
```

