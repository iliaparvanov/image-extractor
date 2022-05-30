# image-extractor
 
## Installation

Docker Desktop is needed for the installation.

    docker-compose up --build

Then the API can be accessed from `localhost:8000/api/v1/`.

A browsable version of the API is available when accessing `localhost:8000/api/v1/images/` from a browser.

SwaggerUI documentation of the API is available at `http://localhost:8000/api/v1/schema/swagger-ui/`.

## Notes

The main functionality of image analysis is implemented in the [Extractor module](./images/extractor.py). The module has been documented with docstrings in the code.

[APScheduler](https://apscheduler.readthedocs.io/en/3.x/) has been used to schedule image analysis due to its easy and quick setup. For a real, production system with high traffic something like Celery would be preferred due to its scalability and flexibility.

[drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/) has been used for API schema generation and visualisation.

## Improvement ideas

* Unit tests for the Extractor class and testing, in general.

* Persistence should be added to the APScheduler. Currently, all jobs are kept in memory and therefore, lost if they are not finished on server restart.

* The url validation logic can be moved from the [ListImage view](./images/views.py) to the ImageCreationSerializer(./images/serializers.py) to make the view thinner.

* Security wasn't paid attention to during development. For example, the Django security key should be kept secret (and not committed to the repo as it currently is), database access should be secured, etc.
