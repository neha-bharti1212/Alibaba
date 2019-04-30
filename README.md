## Alibaba

This project is developed to give a more detailed insight into the search’s data that is generated by a company from the Export API. This application named Alibaba gives a more visualized form of the data fetched from the Export API. The company for which this application has been developed is a China based multinational company that specializes in e-commerce, retail, Internet and technology called Alibaba. All the searches that are generated for this company in the Export API is usually fetched from the Chinese sources which are in native Chinese language. The application provides a platform where these search results can be translated and graphically represented to give a better understanding of the data produced. Also the application analyses these translated search results and classifies them in relatable categories which in turn act as parameters for graphically representing the data. 


#### Getting Started

### Prerequisites

There are three main files to run to deploy the project. The software and hardware requirement for running the three files are:
* Front-End : The front-end is designed in Angular 6. The basic requirement to run this file are:
        * Npm - Node package manager.
        * Angular 6- Angular command line interface that is the angular cli helps in easy interfacing with angular.
            To check if both npm and angular-cli are installed and running in the system, check “ng -v” and “node -v” to check angular-             cli and node version. Open the front-end named “LoginPage”  and run “npm install” to download all dependencies and run the               project. 

* Middleware : The middle-platform is built in NodeJS using Express. To run the program we need to open terminal and run “npm install”. 

* Back-End: The back-end is developed in python. There are some changes you need to do to run the code on your local system:
The Google Translate API requires your credentials to authenticate and use the Google service. 
The database used is PostgreSQL which will require user credentials to access and manipulate data.
An AWS account as S3 buckets are used to store the graphs and data that is used to generate the report.

### Credentials:

* in [api.py](https://github.com/neha-bharti1212/Alibaba/tree/master/api) replace it with the path of google key from google IAM (key.json file) *
```
["GOOGLE_APPLICATION_JSON_FILE"] = <Path to your key.json file downloaded from google IAM >
```
* in [api.py](https://github.com/neha-bharti1212/Alibaba/tree/master/api) replace it with the UserKey from yout Export API  *
```
user_key='<Your User key from Export API develoepr portal>'
```
* in [main.py](https://github.com/neha-bharti1212/Alibaba/blob/master/api/main.py) replace it with the UserKey from yout Export API  *
```
user_key='<Your User key from Export API develoepr portal>'
```




## How to Run 
Once the prerequisites are installed. The program is ready to run. 
Run the command “npm start” on both the Express and Angular  terminal. Run the python script api.py and the application will be ready to run.
The application is hosted on https://localhost:4200/ in the browser  in the local machine that it is hosted on.
* Some missing dependencies that can be encountered are:
 * Amazon’s authentication problem. Make sure to set the environment variables correct in order for the program to crawl and set the amazon credentials required to store the .csv’s and clustered data graphs. *


## Testing
*A file named [main.py](https://github.com/neha-bharti1212/Alibaba/blob/master/api/main.py) is coded for testing purpose. it is a command line interface of the project where you can test the functionality of the entire project. by running this script alone will lets you collect data from export api and make reports.*


## And coding style tests
The code has been coded in a way that it handles most of the exceptions that were encountered during the building phase of this application. 


## Deployment
To run the project on any system : 
* Clone the git repository. 
* Download all the required dependencies.
* Replace the GOOGLE_KEY 
* Replace your User key from export API.
* Create database (Postgres SQL) connection in the [psql.py](https://github.com/neha-bharti1212/Alibaba/blob/master/api/psql.py).
* Run both angular and express files using “npm start” and run the main python script named “api.py”.


## Built With
* Node js - The tool used to code the backend partially.
* Python - The tool used to code the backend majorly.
* Angular - The frontend designing tool.
* Express.js - The routing framework used for the application development.


## Contributing
Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.


## Versioning
We use specific versioning of some packages and tools in the project. To know the specific versions of the python packages to be installed are mentioned in the “req.txt” file in the api folder . For the versions available for tools, npm manages batch package management.


## Authors
* Bibin Benny - developer - Areas of expertise : Python and Export API
* Neha Bharti - developer - Areas of expertise : Angular and Node


