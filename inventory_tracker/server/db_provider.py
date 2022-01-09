import sqlite3
import os.path
import inventory_item, item

class DbProvider:
    def __init__(self, db_filepath):
        db_exists = os.path.exists(db_filepath)
        self.con = sqlite3.connect(db_filepath)
        if db_exists:
            return
        cur = self.con.cursor()
        # Create tables for items and stock
        cur.execute('''CREATE TABLE items
                       (name text, description text)''')
        cur.execute('''CREATE TABLE stock
                       (item_id integer, quantity integer)''')

        # Save (commit) the changes
        self.con.commit()

    def get_items(self):
        cur = self.con.cursor()
        item_list = []
        for row in cur.execute('SELECT rowid, name, description FROM items'):
            item_list.append(item.Item(row[0], row[1], row[2]))
        return item_list

    def get_item(self, id):
        cur = self.con.cursor()
        db_result = cur.execute(f'SELECT rowid, name, description FROM items WHERE rowid = {id}')
        result = db_result.fetchone()
        if result is None:
            raise Exception(f'Item with id = {id} not found')
        return item.Item(result[0], result[1], result[2])

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
        for row in cur.execute('SELECT rowid, item_id, quantity FROM stock'):
            item = inventory_item.InventoryItem(row[0], row[1], row[2])
            inventory_list.append(item)
        return inventory_list

    def create_inventory(self, inventory):
        cur = self.con.cursor()
        db_result = cur.execute(f'SELECT rowid FROM stock WHERE item_id = {inventory.item_id}')
        if db_result.fetchone() is not None:
            raise Exception(f'Inventory with item_id = {inventory.item_id} already exists')
        cur.execute(f'''INSERT INTO stock VALUES 
                       ({inventory.item_id}, {inventory.quantity})''')
        self.con.commit()
        return cur.lastrowid

    def edit_quantity(self, id, quantity):
        cur = self.con.cursor()
        cur.execute(f'UPDATE stock SET quantity = {quantity} WHERE rowid = {id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Inventory with id = {id} does not exist')

    def delete_inventory(self, id):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM stock WHERE rowid = {id}')
        self.con.commit()
        if cur.rowcount == 0:
            raise Exception(f'Inventory with id = {id} does not exist')

