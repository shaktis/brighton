# Brighton Tech Challenge

## Setup instructions
1. Pre-requisites -- [git](https://git-scm.com/downloads), [docker](https://www.docker.com/products/docker-desktop/)
2. Clone repo
    ```shell
       git clone git@github.com:shaktis/brighton.git
       cd brighton
    ```
3. Create a `.env` file with feed URL.  
    ```shell
       cp .env.example .env
    ```
4. Build and launch the app and tail logs 
    ```shell
       docker compose build --no-cache && docker compose up -d && docker logs -f --tail 10 brighton-app-1 
    ```
5. The application logs will display store counts by state as well as create a static HTML file as required by the tech challenge. See screenshots below.
   <img src="docs/images/app_logs_1.png" style="width:600px;"/>
   <img src="docs/images/app_logs_1.png" style="width:600px;"/>
6. Navigate to http://127.0.0.1:5000 in your browser to view the home page as shown in the image below. The first link goes to the static HTML file created at server start and the second link will re-download and recreate the static HTML file
   <img src="docs/images/homepage.png" style="width:600px;"/>
   

## Application structure 
### 1-Backend 
A `python`/`flask` backend with an entry point located in [manage.py](manage.py) `Line 3`.

`Lines 29-32` in [app.py](brighton/app.py) display the store counts by state and create the static HTML file.

`StoreService` in [services.py](brighton/services.py) is a service façade for the backend operations required to complete the task. 

### 2-Front-end
[brighton/templates/stores.html](brighton/templates/stores.html) contains the required HTML and CSS for the front-end. It is defined as a Jinja2 template, the templating system used by the `flask` framework.

### 3-Database
The recommended database definition for storing data returned by the feed is provided in [sql/ddl.sql](sql/ddl.sql) 

### 4-DevOps
Docker related files are [docker-compose.yml](docker-compose.yml) and [DockerFile](DockerFile) and Kubernetes related config is provided in [k8s/deployment.yml](k8s/deployment.yml)