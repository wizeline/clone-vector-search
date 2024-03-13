# Clone Vector Search
## Overview

This service provides endpoints for handling and vectorizing S3 objects, and consume and populate an OpenSearch index, inspired by hexagonal architecture principles.

## Table of Contents
* [Project Structure](#project-structure)
* [Tech Stack](#tech-stack)
* [Installation](#installation)
* [Running the service](#running-the-service)
* [Building the Docker image](#building-the-docker-image)
* [Code Contribution](#code-contribution)

## Project structure

* **service**: Contains the third party services access logic.
* **usecase**: Contains business logic layer.
* **controller**: Contains the Flask API endpoint handlers.
[⇧ back to top](#table-of-contents)

## Tech Stack
* Python
* Flask
* boto3
* Llama-Index
[⇧ back to top](#table-of-contents)

## Installation
1. Clone the repository

```Bash
git clone git@github.com:wizeline/clone-vector-search.git
```

2. Create a Python virtual environment (recommended):

```Bash
python3 -m venv env 
source env/bin/activate 
```

3. Install Dependencies:

```Bash
pip install -r requirements.txt
```
[⇧ back to top](#table-of-contents)

## Running the Service
1. Set Environment Variables (if applicable) in [.env](.env) and [.flaskenv](.flaskenv) files:
2. Create the opensearch index. The application will create the needed mapping.
3. In order to run this service locally, you'll need localstack in order to mock some AWS Services. 
   * Once you have localstack installed and running, create a `clone-ingestion-messages` bucket:
   `aws --endpoint-url=http://localhost:4566 s3 mb s3://clone-ingestion-messages`
   * Add the required test files by running:
   `aws --endpoint-url=http://localhost:4566 s3 cp /path/to/your/file/filename.json s3://clone-ingestion-messages/key/to/file.json`
4. Start the Flask Server:

```Bash
flask run
```
[⇧ back to top](#table-of-contents)

## Building the Docker Image
```Bash
docker compose up --build
```
[⇧ back to top](#table-of-contents)

## Code Contribution

Ensure you adhere to the following conventions when working with code in the Clone Vector Search project:

* **Relate every commit to a ticket**: If the commit is not related to a ticket, the branch name contains the related ticket.
* **Work on one feature for each PR**: Do not crowd unrelated features in one PR.
* **Every line of code in your commits must be production-ready**: Do not create incomplete, work-in-progress commits.
* **Ensure the branching strategy is simple**:
  * Create a feature branch and then merge it with the main branch.
  * Do not create extra branches beside the feature or fix branches to merge with the main.
  * Remove any feature or fix branches after you merge the changes.

[⇧ back to top](#table-of-contents)