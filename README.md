# Stilt - Tech Assessment: Real-time simulation for the fulfillment of delivery orders for a kitchen

## Instalation

Clone the repository:
```bash
git clone https://github.com/mconsoni/delivery_orders_simulation.git
```
Create Python environment:
```bash
python3 -m venv env
```
Activate the environment:
```bash
source env/bin/activate
```
Upgrade pip and install requirements:
```bash
pip3 install -U pip; pip3 install -r requirements.txt
```

## Usage

The system receives a JSON file representing a list of orders with the following format:
```json
[
  {  
    "id": UUID v4 string,
    "name": string, 
    "prepTime": int
  }, 
  ...
]
```
For example:
```json
[
  {
    "id": "a8cfcb76-7f24-4420-a5ba-d46dd77bdffd",
    "name": "Banana Split",
    "prepTime": 4
  },
  {
    "id": "58e9b5fe-3fde-4a27-8e98-682e58a4a65d",
    "name": "McFlury",
    "prepTime": 5
  } 
]
```

Two simulations are run:<br />
The first one using the 'FIFO' strategy for couriers where the courier picks up the next available order.<br />
The second one using the 'MATCHED' strategy for couriers where each courier has an order assigned and may only pick up that order.


### Running the simulations:
```
# python3 cli.py [OPTIONS] FILENAME
```
OPTIONS are parameters used by simulations that can be listed with `--help` option:
```
# python3 cli.py --help

Usage: cli.py [OPTIONS] FILENAME

  -o, --orders_per_second INTEGER
                                  Number of orders per second for the Kitchen.
                                  [default: 2]
  -c, --cooks_in_kitchen INTEGER  Number of orders that can be processed in
                                  parallel.  [default: 1]
  -tmin, --courier_arrival_time_min INTEGER
                                  Min time for a courier to arrival.
                                  [default: 3]
  -tmax, --courier_arrival_time_max INTEGER
                                  Max time for a courier to arrival.
                                  [default: 15]
  --print_info                    Print Simulation info with Orders and
                                  Courier data.
  --help                          Show this message and exit.

```
Example:
```
# python3 cli.py test/dispatch_orders.json
```
