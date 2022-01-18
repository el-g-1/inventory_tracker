# Inventory Tracker

This is a demo project to track inventory.

This product demonstrates basic CRUD functionality:

* Create inventory items
* Edit Them
* Delete Them
* View a list of them

In addition, it supports the following:

* Ability to create “shipments” and assign inventory to the shipment, and adjust inventory appropriately

## Prerequisites

To install dependencies:

* `cd` into the project's root directory (where setup.py is located)
* run: `pip install -e .` or `python setup.py install`

## Usage

To start the server, run:

```bash
python inventory_tracker/server/server.py
```

The server listens on port 5000, i.e. to access WebUI open <http://localhost:5000/>.

## Implementation Details

The server exposes API endpoints to create, edit, delete inventory items, as well as created shipments.

In case of an error, the server replies with code 500 and data in the `{"error": "<error message>"}` format.

Endpoints:

* GET `/api/items/list`  \
  Returns the list of items as list of:

  ```
    {"id": <id of the item>, "name": "<name of the item>", "description": "<description of the item>"}
    ```
  
* POST `/api/items/create` \
  Creates a new item based on the data in the following format:

  ```
    {"name": "<name of the item>", "description": "<description of the item>"}
   ```

  Returns `{"id": <ID of the new item>}`.

* POST `/api/items/edit` \
  Edits the item's name or description. The data format:

  ```
    {"id": <id of the item>, "name": "<name of the item>", "description": "<description of the item>"}
    ```
  
* DELETE `/api/items/delete` \
  Deletes the item, based on the data in the `{"id": <ID of the item>}` format.
  
* GET `/api/inventory/list` \
  Returns the list of items' inventories as list of:

    ```
    {"id": <id of the inventory item>, "item_id": <id of the item>, "quantity": <quantity>}
    ```
  
* POST `/api/inventory/create` \
  Creates a new inventory item based on the data in the following format:

  ```
    {"item_id": <id of the item>, "quantity": <quantity>}
   ```

  Returns `{"id": <ID of the new inventory item>}`.

* POST `/api/inventory/edit` \
  Edits the quantity of the inventory item. The data format:

  ```
    {"id": <id of the inventory item>, "quantity": <quantity>}
   ```
  
* DELETE `/api/inventory/delete` \
  Deletes the inventory item, based on the data in the `{"id": <ID of the inventory item>}` format.
  
* GET `/api/shipments/list` \
  Returns the list of shipments as list of:

    ```
    {"id": <id of the shipment>, "address": "<address of the shipment>"}
    ```
  
* POST `/api/shipments/create` \
  Creates a new shipment based on the data in the following format:

  ```
    {"address": "<address of the shipment>"}
   ```

  Returns `{"id": <ID of the new shipment>}`.

* GET `/api/shipment_inventory/list` \
   Returns the list of shipment inventories as list of:

  ```
    {"id": <id of the shipment inventory>, "shipment_id": <id of the shipment>, "item_id": <id of the item>, "quantity": <quantity>}
   ```

* POST `/api/shipment_inventory/create` \
  Creates a new shipment inventory based on the data in the following format:

  ```
    {"id": <id of the shipment inventory>, "shipment_id": <id of the shipment>, "item_id": <id of the item>, "quantity": <quantity>}
   ```

  Returns `{"id": <ID of the new shipment inventory item>}`.
