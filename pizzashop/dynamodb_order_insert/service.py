# -*- coding: utf-8 -*-
import boto3

def handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    ordersTable = dynamoDB.Table('orders')
    menusTable = dynamoDB.Table('menus')

    ordersTable.put_item(
        Item = {   
            "menu_id": event.get('menu_id'),
            "order_id": event.get('order_id'),
            "customer_name": event.get('customer_name'),
            "customer_email": event.get('customer_email')
        }
    )

    menuResponse = menusTable.get_item(
        Key = {
            "menu_id": event.get('menu_id')
        }
    )
    menu = menuResponse['Item']

    selectionOption = ''         
    for index, value in enumerate(menu['selection']):
        selectionOption += str(index+1) + ". " + value + "  " 

    returnMsg = "Hi {" + event.get('customer_name') + "}, please choose one of these selection: " + selectionOption
    
    return {
        "message" : returnMsg
    }
