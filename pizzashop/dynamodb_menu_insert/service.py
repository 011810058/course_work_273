# -*- coding: utf-8 -*-
import boto3

def handler(event, context):
    dynamoDB = boto3.resource('dynamodb')
    table = dynamoDB.Table('menus')
    table.put_item(
        Item = event
    )
    return "OK"
