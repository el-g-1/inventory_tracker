import sqlite3
import os.path
import inventory_item, item, shipment

class DbProvider:
    def __init__(self, db_filepath):
        db_exists = os.path.exists(db_filepath)
        self.con = sqlite3.connect(db_filepath)
        if db_exists:
            return
        cur = self.con.cursor()
        # Create tables for items and inventory_items
        cur.execute('''CREATE TABLE items
                       (name text, description text)''')
        cur.execute('''CREATE TABLE inventory_items
                       (item_id integer, quantity integer)''')
        cur.execute('''CREATE TABLE shipments
                       (address text)''')
        cur.execute('''CREATE TABLE shipment_inventory_items
                       (shipment_id integer, item_id integer, quantity integer)''')
        # Save (commit) the changes
        self.con.commit()

    def get_items(self, ids=None):
        """Fetches all items by id, duplicates are allowed"""
        query = 'SELECT rowid, name, description FROM items'
        if ids:
            query += ' WHERE ' + ' OR '.join([f'rowid = {id}' for id in ids])
        cur = self.con.cursor()
        item_list = []
        for row in cur.execute(query):
            item_list.append(item.Item(row[0], row[1], row[2]))
        return item_list

    def get_item(self, id):
        return self.get_items(ids=[id])[0]

    def create_item(self, item_instance):
        cur = self.con.cursor()
        cur.execute(f'''INSERT INTO items VALUES 
                       ("{item_instance.name}", "{item_instance.description}")''')
        self.con.commit()
        return cur.lastrowid

    def edit_item(self, item_instance):
        cur = self.con.cursor()
        cur.execute(f'UPDATE items SET name = "{item_instance.name}", '
                    f'description = "{item_instance.description}" WHERE rowid = {item_instance.id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Item with id = {item_instance.id} does not exist')

    def delete_item(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM items WHERE rowid = {id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Item with id = {id} does not exist')

    def get_inventory(self):
        cur = self.con.cursor()
        inventory_list = []
        for row in cur.execute('SELECT rowid, item_id, quantity FROM inventory_items'):
            item = inventory_item.InventoryItem(row[0], row[1], row[2])
            inventory_list.append(item)
        return inventory_list

    def get_full_inventory(self):
        inventory_list = self.get_inventory()
        item_list = self.get_items([inv.item_id for inv in inventory_list])
        return inventory_list, item_list

    def create_inventory(self, inventory):
        cur = self.con.cursor()
        self.get_item(inventory.item_id)
        db_result = cur.execute(f'SELECT rowid FROM inventory_items WHERE item_id = {inventory.item_id}')
        if db_result.fetchone() is not None:
            raise Exception(f'Inventory with item_id = {inventory.item_id} already exists')
        cur.execute(f'''INSERT INTO inventory_items VALUES 
                       ({inventory.item_id}, {inventory.quantity})''')
        self.con.commit()
        return cur.lastrowid

    def edit_quantity(self, id, quantity):
        cur = self.con.cursor()
        cur.execute(f'UPDATE inventory_items SET quantity = {quantity} WHERE rowid = {id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Inventory with id = {id} does not exist')

    def delete_inventory(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM inventory_items WHERE rowid = {id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Inventory with id = {id} does not exist')

    def get_shipments(self):
        cur = self.con.cursor()
        shipments_list = []
        for row in cur.execute('SELECT rowid, address FROM shipments'):
            item = shipment.Shipment(row[0], row[1])
            shipments_list.append(item)
        return shipments_list

    def get_shipment_inventory_items(self):
        cur = self.con.cursor()
        shipment_inventory_items = []
        for row in cur.execute(f'SELECT rowid, shipment_id, item_id, quantity FROM shipment_inventory_items'):
            shipment_inventory = shipment.ShipmentInventoryItem(row[0], row[1], row[2], row[3])
            shipment_inventory_items.append(shipment_inventory)
        return shipment_inventory_items

    def get_full_shipment(self):
        shipment_list = self.get_shipments()
        shipment_item_list = self.get_shipment_inventory_items()
        items = self.get_items([shipment_inventory_item.item_id for shipment_inventory_item in shipment_item_list])
        return shipment_list, shipment_item_list, items

    def create_shipment(self, address):
        cur = self.con.cursor()
        cur.execute(f'''INSERT INTO shipments VALUES ("{address}")''')
        self.con.commit()
        return cur.lastrowid

    def create_shipment_inventory(self, shipment_inventory):
        cur = self.con.cursor()
        shipment_id = shipment_inventory.shipment_id
        item_id = self.get_item(shipment_inventory.item_id)
        if cur.execute(f'SELECT rowid FROM shipment_inventory_items WHERE shipment_id = {shipment_inventory.shipment_id} AND item_id = {shipment_inventory.item_id}').fetchone() is not None:
            raise Exception(f'Shipment with id = {shipment_inventory.shipment_id} and item with id = {shipment_inventory.item_id} already exists')
        db_result = cur.execute(f'SELECT rowid, item_id, quantity FROM inventory_items WHERE item_id = {shipment_inventory.item_id}').fetchone()
        if db_result is None or db_result[2] < shipment_inventory.quantity:
            """Item not in stock"""
            raise Exception(f'{shipment_inventory.quantity} item(s) with id = {shipment_inventory.item_id} not available')
        elif db_result[2] == shipment_inventory.quantity:
            """We deplete the stock"""
            cur.execute(f'''INSERT INTO shipment_inventory_items VALUES 
                           ({shipment_inventory.shipment_id}, {shipment_inventory.item_id}, {shipment_inventory.quantity})''')
            self.delete_inventory(db_result[0])
        else:
            """There is enough in stock"""
            cur.execute(f'''INSERT INTO shipment_inventory_items VALUES 
                           ({shipment_inventory.shipment_id}, {shipment_inventory.item_id}, {shipment_inventory.quantity})''')
            self.edit_quantity(db_result[0], db_result[2] - shipment_inventory.quantity)
        self.con.commit()
        return cur.lastrowid