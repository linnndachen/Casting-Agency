## Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

### Models:

Movies with attributes title and release date
Actors with attributes name, age and gender

## Endpoints:
GET /actors and /movies
DELETE /actors/ and /movies/
POST /actors and /movies and
PATCH /actors/ and /movies/

## Roles:
#### Casting Assistant
Can view actors and movies

#### Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies


#### Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database


## Tests:
One test for success behavior of each endpoint
One test for error behavior of each endpoint
At least two tests of RBAC for each role

curl --request POST \
--url 'https://casting-project.us.auth0.com/oauth/token' \
--header 'content-type: application/x-www-form-urlencoded' \
--data grant_type=client_credentials \
--data client_id=QzkduPCZUn9Bjj3QV8BGyfYH8W3qU90r \
--data client_secret=1E7I9jqpQ1JIrXiavNZLwnb3Wwc6nFWNCy-TeNFowP4qs8SToR_GIWlUIMDPP-hy
--data audience=casting

audience=casting&
scope=SCOPE&
response_type=token&
client_id=QzkduPCZUn9Bjj3QV8BGyfYH8W3qU90r&
redirect_uri=http://127.0.0.1:8080/users&
state=STATE