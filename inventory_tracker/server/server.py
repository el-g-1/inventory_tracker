from flask import Flask, request, make_response, render_template
import json
import db_provider
import inventory_item, item, shipment

app = Flask('inventory_tracker', template_folder='inventory_tracker/templates')

@app.route('/api/items/list')
def items():
    try:
        db = db_provider.DbProvider('test.db')
        id = request.args.get('id')
        if id is not None:
            return json.dumps(db.get_item(id).as_dict())
        return json.dumps([x.as_dict() for x in db.get_items()])
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/items/create', methods=['POST'])
def create_item():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        new_item = item.Item(id=None, name=req['name'], description=req['description'])
        return json.dumps({'id': db.create_item(new_item)})
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/items/edit', methods=['POST'])
def edit_item():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        new_item = item.Item(id=req['id'], name=req['name'], description=req['description'])
        db.edit_item(new_item)
        return make_response('', 200)
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/items/delete', methods=['DELETE'])
def delete_item():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        db.delete_item(req['id'])
        return make_response('', 200)
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/inventory/list')
def inventory():
    db = db_provider.DbProvider('test.db')
    full = request.args.get('full', default=False)
    if full:
        inventory_list, item_list = db.get_full_inventory()
        return json.dumps({"inventory": [x.as_dict() for x in inventory_list], "items": [x.as_dict() for x in item_list]})
    return json.dumps([x.as_dict() for x in db.get_inventory()])

@app.route('/api/inventory/create', methods=['POST'])
def create_inventory():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        new_item = inventory_item.InventoryItem(id=None, item_id=req['item_id'], quantity=req['quantity'])
        return json.dumps({'id': db.create_inventory(new_item)})
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/inventory/edit', methods=['POST'])
def edit_quantity():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        db.edit_quantity(req['id'], req['quantity'])
        return make_response('', 200)
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/inventory/delete', methods=['DELETE'])
def delete_inventory():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        db.delete_inventory(req['id'])
        return make_response('', 200)
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

# @app.route('/shipments/')
# def shipments():
#     try:
#         db = db_provider.DbProvider('test.db')
#         return json.dumps([x.as_dict() for x in db.get_shipments()])
#     except Exception as ex:
#         return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/shipments/list')
def shipments():
    db = db_provider.DbProvider('test.db')
    full = request.args.get('full', default=False)
    if full:
        shipment_list, shipment_item_list, items = db.get_full_shipment()
        return json.dumps({"shipments": [x.as_dict() for x in shipment_list], "shipment_inventory": [x.as_dict() for x in shipment_item_list], "items": [x.as_dict() for x in items]})
    # return json.dumps([x.as_dict() for x in db.get_inventory()])
    try:
        return json.dumps([x.as_dict() for x in db.get_shipments()])
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/shipments/create', methods=['POST'])
def create_shipment():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        return json.dumps({'id': db.create_shipment(address=req['address'])})
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/api/shipment_inventory/list')
def shipment_inventory():
    db = db_provider.DbProvider('test.db')
    return json.dumps([x.as_dict() for x in db.get_shipment_inventory_items()])

@app.route('/api/shipment_inventory/create', methods=['POST'])
def create_shipment_inventory():
    try:
        db = db_provider.DbProvider('test.db')
        req = request.get_json()
        new_item = shipment.ShipmentInventoryItem(id=None, shipment_id=req['shipment_id'], item_id=req['item_id'], quantity=req['quantity'])
        return json.dumps({'id': db.create_shipment_inventory(new_item)})
    except Exception as ex:
        return make_response(json.dumps({'error': str(ex)}), 500)

@app.route('/')
def index():
    return render_template('tables.html', title='Inventory tracker')

if __name__ == '__main__':
    app.run()