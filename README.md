# ATCF-HTTP-Server
A RESTful Flask server that returns JSON data of ATCF storm data.  

## How to use
### Server installation and startup
[Python 3.9](https://www.python.org/downloads/) is required for installation, as well as an up-to-date pip package installer. 

Clone the repository via a zip download, or from a local git installation.  Once cloned, the server can be run by running
`run.bat` (Windows) or `run.sh` (Linux/MacOS).  This will first check if a virtual environment exists in the directory, and will 
install all packages in `requirements.txt` to the virtual environment or - if no virtual environment is detected - the system environment.
This will run the server on localhost (127.0.0.1) and port 5000 by default.


To change the IP address and/or port used, you can create an .env file containing the following values:
* For development: `DEV_FLASK_IP` and `DEV_FLASK_PORT`
* For production: `PROD_FLASK_IP` and `PROD_FLASK_PORT`

To use the development environment variables, the `DevelopmentConfig` must be loaded from `config.py`.  The production variables
can be loaded using the `StagingConfig` and `ProductionConfig`. By default, `DevelopmentConfig` is loaded in `src/__init__.py`

Client will need to send a HTTP GET request in order to get data.  

To see examples as well with parameters, check out the [client README](src/README.md) or the [index file](127.0.0.1:5000) (only accessible if server is running on localhost)

![Index file of api.  Instructions are presented for clients, and can be found at ](images/home_page_example.png)