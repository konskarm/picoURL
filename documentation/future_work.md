# Taking the application into production

Currently, the following are true for our application:
* We are using SQLite which has to be changed to a more robust technology, not just in the 
local environment, but in production too. 
* The database and the application are in the same container.
* The server is running using the default Django server (runserver).
* The secret key is version controlled. 

# Improvement points
* Use PostgreSQL or, since we do not have a strict database schema, we can move to a NoSQL database.
* Separate the database and the application in different containers.
* Use load balancers. 
* Use Kubernetes to orchestrate the deployment of the application and keep the secrets there.
* Possibly create custom HTTP error codes. For example, instead of returning 500 error
if we ever encounter the maximum number of hash collisions, we can have an error
HTTP_555_MAX_HASHING_RETRIES_ENCOUNTERED.
* Have different settings.py for production and development.
* Use the [Django checklist for production](https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/).
* Use Docker volumes to map the current database to the host machine, in order to keep it persistent 
(if we consider SQLite for production).


# Deploy the application on the cloud
With the assumption that the cloud server has docker installed, we can deploy the application 
using the current setup, since it is containarized.
