"""
Title: ATCF HTTP Server
Description: A Flask-based HTTP server that returns data from the ATCF in JSON format.
"""
from threading import Thread
from src import ATCFServer, DevelopmentConfig, app

config = DevelopmentConfig

if __name__ == "__main__":
    Thread(target=ATCFServer).start()  # Read class description
    # Server will try to use ip and port defined in .env.  If not found, it will use default values
    Thread(app.run(host=config.FLASK_IP,
                   port=config.FLASK_PORT,
                   debug=config.DEBUG,
                   use_reloader=config.RELOADER)).start()  # Flask server
