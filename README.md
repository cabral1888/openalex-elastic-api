# OpenAlex API

This is the elasticsearch-backed portion of the [OpenAlex API](https://api.openalex.org/).

Please send all bug reports and feature requests to support@openalex.org.

## How to run the application
### Pre requisites
Please make sure you have the following installed in your local:
- Docker Desktop
- Python 3.9+
- VSCode
- Elastic search 8.18.x (with `xpack.security.enabled` disabled)
- Redis (any version)
- Postgresql (any version)

In order to start those services, you can navigate to ` prerequisites/` folder and run the following command:
```
docker-compose up
```
It will spin up an elasticsearch and postgresql instance. Finally we can set up the redis cache by going to the root of this project and running:
```
make cache-up
```
#### Elasticsearch preparation
We need to set up the index properly according to the desired template (https://github.com/ourresearch/openalex-elasticsearch/tree/main/elasticsearch_templates). Using `works` model as an example, we need to instruct elasticsearch to use the `works` model, by running the following command:
```
curl -X PUT "http://localhost:9200/works-v26-test" -H 'Content-Type: application/json' -d '
{
  "mappings": {
    ...
  }
}'
```
This will create the index structure, required for the application to function properly.

#### Destroying the infra assets
If needed, in order to destroy the containers created in the previous step, you can run:
```
cd prerequisites; docker-compose down --rmi all; cd .. # stop elasticsearch and postgresql
make cache-stop # stop redis
```  

### Virtual Container in VSCode
In order to have a plug and play and reproducible local env, we are leveraging the feature called Dev Container. With this feature,
we will be able to execute the backend server without having to manually configure the details in the host machine.

In order to do it, we just need to click in the blue box in the bottom left corner and then choose `Reopen in Dev Container`. If everything is set up properly, you should be able to see a prompt like the following:
```
root@942815961e34:/workspaces/openalex-elastic-api
```
If it doesn't open, we need to click on the `+` sign (New Terminal) and there we go!

### Running the application
Make sure you have the following env var set within the terminal opened in VSCode from previous step:
```
export CACHE_REDIS_URL=redis://localhost:6379
export REDIS_DO_URL=redis://localhost:6379
export ES_URL_V2=http://localhost:9200
export USERS_DB_URL=postgresql://localhost:5432
ES_URL_PROD=http://192.168.1.9:9200 # depending on how your Docker network setup is configured, you need to speficy your host private IP
```
With those env vars set, you can execute the Flask backend app by running the following command:
```
python app.py
```
If everything is set up properly, you will see the following in the console:
```
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
You can navigate to any model ingested previously, for example `http://127.0.0.1:5000/works` and it will bring up data from ElasticSearch