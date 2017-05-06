# -*- coding: utf-8 -*-
import boto3
import datetime

def handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    ordersTable = dynamoDB.Table('orders')
    menusTable = dynamoDB.Table('menus')

    print "Fetching detail for order no: %s " % event.get('order_id')
    ordersResponse = ordersTable.get_item(
        Key = {
            "order_id": event.get('order_id')
        }
    )
    order = ordersResponse['Item']

    print "Fetching {%s} menu detail for selected order" % order['menu_id']
    menuResponse = menusTable.get_item(
            Key = {
                "menu_id": order['menu_id']
            }
    )
    menu = menuResponse['Item']

    
    if 'order_detail' in order:
        if 'selection' in order['order_detail']:
            menuOptions = menu['size']
            selection = menuOptions[int(event.get('input'))-1]

            costOptions = menu['price']
            costs = costOptions[int(event.get('input'))-1]

            ordersTable.update_item(
            Key = {
                "order_id": event.get('order_id')
            },
            UpdateExpression = 'set order_status = :val1, order_detail = :val2',
            ExpressionAttributeValues = {
                ':val1': "processing",
                ':val2':  {'selection' : order['order_detail']['selection'],'size' : selection, 'costs' : costs,
                 'order_time' : datetime.datetime.now().strftime("%m-%d-%y@%I:%M:%S")}
            }
        )

        returnMsg =  "Your order costs $%s. We will email you when the order is ready. Thank you!" % costs

    else:
        menuOptions = menu['selection']
        selection = menuOptions[int(event.get('input'))-1] #if selection is 1 then it represent 0 index 
        print "Selecting the menu option %s for the given order %s" % (selection, event.get('order_id'))

        ordersTable.update_item(
            Key = {
                "order_id": event.get('order_id')
            },
            UpdateExpression = 'set order_detail = :val1',
            ExpressionAttributeValues = {
                ':val1': {'selection' : selection}
            }
        )    

        selectionOption = ''         
        for index, value in enumerate(menu['size']):
            selectionOption += str(index+1) + ". " + value + "  " 

        returnMsg = "Which size do you want? "  + selectionOption

    print returnMsg
    return {
        "message" : returnMsg
    }
