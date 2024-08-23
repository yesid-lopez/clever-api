# Clever

backend deployed: https://clever.yesidlopez.de/docs
trulens monitoring dashboard: https://trulens-clever.yesidlopez.de/

# Dependencies

- Minio

## How to run 

Once you have a cluster up and running execute 

```bash
helm install clever --namespace tidb-hackathon --create-namespace chart/
```


## Local execution

Considering Minio is a dependency you can run the docker-compose file with:

```bash
docker compose up
```

Do not forget to create a  `.env` file based on the `.env.example` file
