## Description

Create a URL shortening service, like TinyURL or bit.ly.

## Requirements

The application must have the following endpoints:
* **POST /**
    * Request: JSON containing the original URL.
    * Response: JSON containing the generated short code.
* **GET /:short_code:**
    * Response: Redirect to the original URL.
* **GET /:short_code:/stats**
    * Response: JSON containing the original URL, the creation date and the amount of times it has been used.
    
