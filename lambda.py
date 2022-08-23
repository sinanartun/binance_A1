import os
import json
import mysql.connector



def lambda_handler(event, context):
    load_data_sql = "LOAD DATA FROM S3 's3://dsmlbc9/data_1_min/1661193720.tsv' INTO TABLE builk.BTCUSDT FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n' (bid, parameter, price, quantity, time, maker);"

    cnx = mysql.connector.connect(host=os.environ['RDS_HOSTNAME'], user=os.environ['RDS_USERNAME'], passwd=os.environ['RDS_PASSWORD'],
                                  database=os.environ['RDS_DB_NAME'], port=os.environ['RDS_PORT'])
    cur = cnx.cursor()
    cur.execute(load_data_sql)
    cnx.commit()
    cnx.close()

    return {'statusCode': 200, 'body': json.dumps("OK", indent=0, sort_keys=True, default=str)}