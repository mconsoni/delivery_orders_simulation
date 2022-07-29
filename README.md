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
Examples:
Running the simulations with default parameters:
```
# python3 cli.py test/dispatch_orders.json
```
Running the simulations with 3 cooks in the kitchen and 5 orders per second:
```
# python3 cli.py -c 3 -o 5 test/dispatch_orders.json
```

### Output:
Print events to the console.  When each simulation is finished prints the average waiting time for orders and couriers.
```
16:36:05   ORDER RECEIVED       a8cfcb76-7f24-4420-a5ba-d46dd77bdffd   Banana Split
16:36:05   ORDER RECEIVED       58e9b5fe-3fde-4a27-8e98-682e58a4a65d   McFlury
16:36:05   ORDER RECEIVED       2ec069e3-576f-48eb-869f-74a540ef840c   Acai Bowl
16:36:05   ORDER RECEIVED       690b85f7-8c7d-4337-bd02-04e04454c826   Yogurt
16:36:05   ORDER RECEIVED       972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a   Chocolate Gelato
16:36:05   COURIER DISPATCHED   e4b2d700-94b5-4529-9ee8-866a80444b30   DELAY 7.003385030306367 ORDER ASSIGNED a8cfcb76-7f24-4420-a5ba-d46dd77bdffd
16:36:05   COURIER DISPATCHED   80cf3d06-10f3-44b5-a900-a59036596f55   DELAY 6.974098867608262 ORDER ASSIGNED 58e9b5fe-3fde-4a27-8e98-682e58a4a65d
16:36:05   COURIER DISPATCHED   4661a49b-5957-4dc5-bf89-87db3099b091   DELAY 13.472421603211682 ORDER ASSIGNED 2ec069e3-576f-48eb-869f-74a540ef840c
16:36:05   COURIER DISPATCHED   198f10f7-9bab-4494-9429-8416feecfd74   DELAY 14.078698091620359 ORDER ASSIGNED 690b85f7-8c7d-4337-bd02-04e04454c826
16:36:05   COURIER DISPATCHED   a064f515-bc54-4f0c-a335-cee47fe8fdeb   DELAY 11.635124745311433 ORDER ASSIGNED 972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a
16:36:08   ORDER PREPARED       2ec069e3-576f-48eb-869f-74a540ef840c   Acai Bowl
16:36:09   ORDER PREPARED       a8cfcb76-7f24-4420-a5ba-d46dd77bdffd   Banana Split
16:36:10   ORDER PREPARED       58e9b5fe-3fde-4a27-8e98-682e58a4a65d   McFlury
16:36:12   COURIER ARRIVED      80cf3d06-10f3-44b5-a900-a59036596f55   ORDER ASSIGNED 58e9b5fe-3fde-4a27-8e98-682e58a4a65d
16:36:12   ORDER PICKED UP      58e9b5fe-3fde-4a27-8e98-682e58a4a65d   McFlury COURIER: 80cf3d06-10f3-44b5-a900-a59036596f55
           ORDER WAIT TIME: 1.899562 s.
           COURIER WAIT TIME: 0.022399 s.
16:36:12   COURIER ARRIVED      e4b2d700-94b5-4529-9ee8-866a80444b30   ORDER ASSIGNED a8cfcb76-7f24-4420-a5ba-d46dd77bdffd
16:36:12   ORDER PICKED UP      a8cfcb76-7f24-4420-a5ba-d46dd77bdffd   Banana Split COURIER: e4b2d700-94b5-4529-9ee8-866a80444b30
           ORDER WAIT TIME: 2.999895 s.
           COURIER WAIT TIME: 0.099712 s.
16:36:14   ORDER PREPARED       690b85f7-8c7d-4337-bd02-04e04454c826   Yogurt
16:36:16   ORDER PREPARED       972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a   Chocolate Gelato
16:36:16   COURIER ARRIVED      a064f515-bc54-4f0c-a335-cee47fe8fdeb   ORDER ASSIGNED 972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a
16:36:16   ORDER PICKED UP      972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a   Chocolate Gelato COURIER: a064f515-bc54-4f0c-a335-cee47fe8fdeb
           ORDER WAIT TIME: 0.599717 s.
           COURIER WAIT TIME: 0.06482 s.
16:36:18   COURIER ARRIVED      4661a49b-5957-4dc5-bf89-87db3099b091   ORDER ASSIGNED 2ec069e3-576f-48eb-869f-74a540ef840c
16:36:18   ORDER PICKED UP      2ec069e3-576f-48eb-869f-74a540ef840c   Acai Bowl COURIER: 4661a49b-5957-4dc5-bf89-87db3099b091
           ORDER WAIT TIME: 10.400058 s.
           COURIER WAIT TIME: 0.027011 s.
16:36:19   COURIER ARRIVED      198f10f7-9bab-4494-9429-8416feecfd74   ORDER ASSIGNED 690b85f7-8c7d-4337-bd02-04e04454c826
16:36:19   ORDER PICKED UP      690b85f7-8c7d-4337-bd02-04e04454c826   Yogurt COURIER: 198f10f7-9bab-4494-9429-8416feecfd74
           ORDER WAIT TIME: 5.000247 s.
           COURIER WAIT TIME: 0.021012 s.
========================================================================================================================
=== RESULTS ============================================================================================================
AVG ORDER WAIT TIME: 4.1799s
AVG COURIER WAIT TIME: 0.0470s
========================================================================================================================
```
If --print_info option is present prints a table with orders and couriers details after each simulation:
```
...
16:36:19   COURIER ARRIVED      198f10f7-9bab-4494-9429-8416feecfd74   ORDER ASSIGNED 690b85f7-8c7d-4337-bd02-04e04454c826
16:36:19   ORDER PICKED UP      690b85f7-8c7d-4337-bd02-04e04454c826   Yogurt COURIER: 198f10f7-9bab-4494-9429-8416feecfd74
           ORDER WAIT TIME: 5.000247 s.
           COURIER WAIT TIME: 0.021012 s.
========================================================================================================================
=== SIMULATION =========================================================================================================
- STRATEGY: FIFO
- ORDERS PER SECOND: 5
- COOKS IN KITCHEN: 3
- COURIER ARRIVAL MIN TIME: 3
- COURIER ARRIVAL MAX TIME: 15
------------------------------------------------------------------------------------------------------------------------
- ORDERS
                                   ID                     Name Time     Added   Started  Finished Delivered      Wait
 2ec069e3-576f-48eb-869f-74a540ef840c                Acai Bowl   3s  16:40:23  16:40:23  16:40:26  16:40:30    4.2953s
 a8cfcb76-7f24-4420-a5ba-d46dd77bdffd             Banana Split   4s  16:40:23  16:40:23  16:40:27  16:40:32    5.5001s
 58e9b5fe-3fde-4a27-8e98-682e58a4a65d                  McFlury   5s  16:40:23  16:40:23  16:40:28  16:40:34    5.9963s
 690b85f7-8c7d-4337-bd02-04e04454c826                   Yogurt   6s  16:40:23  16:40:26  16:40:32  16:40:36    4.2998s
 972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a         Chocolate Gelato   7s  16:40:23  16:40:27  16:40:34  16:40:37    3.2020s
------------------------------------------------------------------------------------------------------------------------
- COURIERS
                                   ID                             Order ID   Arrival  Delivery      Wait
 85faa713-0a00-45e3-a0bb-75734a9404db 2ec069e3-576f-48eb-869f-74a540ef840c  16:40:30  16:40:30    0.0004s
 c054c210-2aff-41e3-bc76-2722a8a25514 a8cfcb76-7f24-4420-a5ba-d46dd77bdffd  16:40:32  16:40:32    0.1021s
 7c21195f-47a6-4350-afca-f4f1a0e2cc59 58e9b5fe-3fde-4a27-8e98-682e58a4a65d  16:40:34  16:40:34    0.0013s
 543a67e6-8ad1-48bf-a44e-ea2d4fd22cad 690b85f7-8c7d-4337-bd02-04e04454c826  16:40:36  16:40:36    0.0995s
 69296fbe-063e-4670-9081-f23d9e13a910 972aa5b8-5d83-4d5e-8cf3-8a1a1437b18a  16:40:37  16:40:37    0.0147s
========================================================================================================================
=== RESULTS ============================================================================================================
AVG ORDER WAIT TIME: 4.6587s
AVG COURIER WAIT TIME: 0.0436s
========================================================================================================================

```
