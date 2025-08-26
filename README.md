# Star Wars Delivery Quote Generator
This project is used to generate quotes for delivering Star Wars vehicles using starships.  
<b>NOTE:</b> The data for this project has been grabbed from https://swapi.tech, a community approved mirror of https://swapi.dev

## TABLE OF CONTENT

- [Development System Details](#development-system-details)
- [Requirements](#requirements)
- [Design](#design)
  - [Considerations](#considerations)
  - [Data Flow](#data-flow)
  - [Input Format](#input-format)
  - [Output Structure](#output-structure)
- [Run](#run)
  - [Pre-requisites](#pre-requisites)
  - [Run on Host Directly](#run-on-host-directly)
  - [Run in Docker Container (Preferred)](#run-in-docker-container-preferred)
- [Output File Description](#output-file-description)

## Development System Details
Below are the tools and stack used to develop the code:
- macOS Sonoma
- PyCharm 2025.2.0.1
- Python 3.11.13
- Docker 28.3.2

## Requirements
The aim of the project is to generate sales quote for delivery of vehicles through starships.
The following are the requirements of this task:
1. Application should accept these inputs from the user:
    - list of vehicle names
    - distance to deliver vehicles in MegaLights
2. Application should generate a quote in a machine-readable format (like json) with the following information :
   - The cheapest starship that can be used to transport the specified vehicles 
   - The fastest starship that can be used to transport the specified vehicles 
   - A recommendation for an up-sell. This should be the next fastest starship after the cheapest starship (if one exists). 
   - The Millennium Falcon can never be an up-sell recommended
3. All of the data should be available via the API available at https://swapi.dev
4. The starship will have minimum number of crew for the delivery and each crew will receive 100 credits per day of travel. That will form the cost in credits for the delivery. 
5. The application should consider generating a quote translated to wookie for the wookiee customers.

## Design
### Considerations
Some considerations were made to design the algorithm:
1. Vehicles will fit as long as the max length of all vehicles is lesser than the length of the starship vehicle. Some starships are smaller in length than a vehicle, and since we don't have a reference to their width we can assume that a vehicle will atleast need to fit length-wise. For ease of design, its also considered that multiple vehicles may be arranged side by side rather than just end to end, because starships are also usually bigger in width so sum of vehicle length does not have to be lesser than starship length.
2. An hr is 60 mins, and A “day” is 24 hours as considered on our lovely planet Earth.
3. The quote does not require all the data for the starship or the vehicle just a couple of meaningful columns like name, model, MGLT rating, cost of delivery, minimum crew and number of days to travel. 
4. A starship is not being “bought” so the only cost associated to the delivery is the credits earned by the crew.
5. The quote in question also does not have costs associated with “purchasing” the vehicles because the requirement clearly stated this is a delivery business.
6. If crew is not mentioned then it's considered to carry 1 minimum crew member.
7. MGLT of starships is used to calculate days of travel and if its unknown we don’t include that in our quote.

### Data Flow
1. The application pulls all the starship data from the website once at the start.
   - It grabs the list of starship urls in one go using `https://swapi.tech/starships?page=1&limit=40`
   - Then pulls data for each url using `https://swapi.tech/starships/<uid>`  and stores it in a pandas DataFrame
2. Then user inputs, `list_of_vehicles` and `distance_to_deliver`, are gathered in an interactive way
3. Following that the vehicle data is pulled based on the list of `list_of_vehicles`. Note that swapi.tech has a useful api design which allows us to query data by name with the url `https://swapi.tech/vehicles?name=<name>`
4. Cost of credits to deliver is calculated for each starship using the input `distance_to_deliver` with the minimal columns needed
   - Number of days to travel is calculated using the input and the `MGLT` property of the starship: `((distance_to_deliver/MGLT)*2)/24`
   - Cost associated to the minimum crew is calculated using the number of days to travel: `min_crew*100*number_of_days_travel`
5. The cheapest starship is found in the top row if sorting the above DataFrame by cost of credits to deliver
6. The fastest starship is found in the top row if sorting the above DataFrame by `MGLT` value
7. The recommended upsell or the next fastest starship after the cheapest starship is found in the DataFrame resulted from step 6. It will be in the previous row of the row that houses the cheapest starship found.
   - If that starship happens to be "Millenium Falcon" then its ignored and the application looks for the row previous to that
8. The above information from steps 5-7 is written in a json file in `output` folder which is basically the quote required.
9. The quote is also transformed into wookie and saved in the same `output` folder
10. Application allows the user to generate more quotes by pressing the key `Y` upon the prompt to do so which repeats everything from step 2. 

### Input Format
Input is taken interactively from the user. These 2 inputs should be provided to the application for it to generate the quotes:
1. list of exact vehicle names separated by commas
2. distance to deliver in MegaLights as a numeric

### Output Structure
Output is stored in Json format. The structure is below:
```
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Generated schema for Root",
  "type": "object",
  "properties": {
    "sales_input": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "vehicles_list": {
            "type": "string"
          },
          "distance_to_deliver_mglt": {
            "type": "string"
          }
        },
        "required": [
          "vehicles_list",
          "distance_to_deliver_mglt"
        ]
      }
    },
    "cheapest_starship_quote": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "model": {
            "type": "string"
          },
          "min_crew": {
            "type": "string"
          },
          "MGLT": {
            "type": "string"
          },
          "num_days_to_travel": {
            "type": "string"
          },
          "cost_of_credits_delivery": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "model",
          "min_crew",
          "MGLT",
          "num_days_to_travel",
          "cost_of_credits_delivery"
        ]
      }
    },
    "fastest_starship_quote": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "model": {
            "type": "string"
          },
          "min_crew": {
            "type": "string"
          },
          "MGLT": {
            "type": "string"
          },
          "num_days_to_travel": {
            "type": "string"
          },
          "cost_of_credits_delivery": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "model",
          "min_crew",
          "MGLT",
          "num_days_to_travel",
          "cost_of_credits_delivery"
        ]
      }
    },
    "recommended_upsell_starship_quote": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string"
          },
          "model": {
            "type": "string"
          },
          "min_crew": {
            "type": "string"
          },
          "MGLT": {
            "type": "string"
          },
          "num_days_to_travel": {
            "type": "string"
          },
          "cost_of_credits_delivery": {
            "type": "string"
          }
        },
        "required": [
          "name",
          "model",
          "min_crew",
          "MGLT",
          "num_days_to_travel",
          "cost_of_credits_delivery"
        ]
      }
    }
  },
  "required": [
    "sales_input",
    "cheapest_starship_quote",
    "fastest_starship_quote",
    "recommended_upsell_starship_quote"
  ]
}
```

## Run
### Pre-requisites
- macOS or Linux OS
- Python 3.11
- (Optional for containerization) Docker Engine 28.3.2

### Run on Host Directly
1. Clone the repository using `https://github.com/SrijaGanguly/sw_delivery_quote_generator.git`
2. Install python virtualenv using `pip install virtualenv`
3. Start a python virtualenv in local bash terminal/console using the following steps:
   ```shell
    cd sw_delivery_quote_generator/

    python -m venv swquotenv

    source swquotenv/bin/activate
    ```
4. Install project requirements from the root of the project using `pip install -r requirements.txt`
5. Run the code using `python main.py`
6. Code will ask for user inputs after pulling the data. 
   - It will ask for the list of vehicles. Enter the list of exact vehicle names separated by commas as represented below:
      ```text
      Enter list of vehicles to deliver (separated by commas): Snowspeeder, Storm IV Twin-Pod cloud car
       ```
   - Then it will ask for the distance to deliver in MegaLights. Enter a number as represented below:
      ```text
      Enter distance (in MegaLights) to the delivery destination: 500 
      ```
7. Following the inputs, there will be console output of data analysis and the quotes will be generated in `output/` directory

### Run in Docker Container (Preferred)
1. Clone the repository using `https://github.com/SrijaGanguly/sw_delivery_quote_generator.git`
2. Ensure Docker Engine is installed before running the subsequent steps.
3. Build the docker image once using 
 ```shell
    cd sw_deliver_quote_generator/
    
    docker build -t sw_delivery_quote_generator .
 ```
4. Run the docker container from a preferred location `docker run -it -v $(pwd)/output:/app/output sw_delivery_quote_generator`
5. Code will ask for user inputs after pulling some starship data. 
   - It will ask for the list of vehicles. Enter the list of exact vehicle names separated by commas as represented below:
      ```text
      Enter list of vehicles to deliver (separated by commas): Snowspeeder, Storm IV Twin-Pod cloud car
       ```
   - Then it will ask for the distance to deliver in MegaLights. Enter a number as represented below:
      ```text
      Enter distance (in MegaLights) to the delivery destination: 500 
6. Following the inputs, there will be console output of data analysis and quotes will be available on the host in `output/` directory in the current location

## Output File Description
Outputs are in the form of json files. For information about the structure of the json files generated refer to the section [Output Structure](#output-structure)
The following quotes will be available in the `output/` directory:
1. `sales_vehicle_delivery_quote.json` - this is the quote in English for the sales team 
2. `sales_vehicle_delivery_quote_wookie.json` - this is the quote in Wookie for the sales team that can be forwarded to the Wookie customers
NOTE: These files are overwritten on every run
