import time
import json
import boto3

ATHENA_DATABASE = 'jan23'
ATHENA_TABLE = 'events'
DYNAMODB_TABLE = 'events'
S3_OUTPUT = 's3://events-lambda-output'
S3_BUCKET = 'events-lambda-output'
PAGE_SIZE = 500
count = 0

# number of athena read retries
RETRY_COUNT = 10


def lambda_handler(event, context):
    count = 0

    # you will want a different query, obviously
    query = "SELECT * FROM %s.%s LIMIT 3000" % (ATHENA_DATABASE, ATHENA_TABLE)
    query = query.format(ATHENA_TABLE)

    athena = boto3.client('athena')

    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': ATHENA_DATABASE
        },
        ResultConfiguration={
            'OutputLocation': S3_OUTPUT,
        }
    )

    query_execution_id = response['QueryExecutionId']
    print("executing query {}".format(query_execution_id))

    for i in range(1, 1 + RETRY_COUNT):

        query_status = athena.get_query_execution(QueryExecutionId=query_execution_id)
        query_execution_status = query_status['QueryExecution']['Status']['State']

        if query_execution_status == 'SUCCEEDED':
            print("STATUS: {}".format(query_execution_status))
            break

        if query_execution_status == 'FAILED':
            raise Exception("STATUS: {}".format(query_execution_status))

        else:
            print("STATUS: {}... checking again in {} seconds".format(query_execution_status, i))
            time.sleep(i)
    else:
        athena.stop_query_execution(QueryExecutionId=query_execution_id)
        raise Exception('QUERY TIMED OUT')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    keys = None

    results_paginator = athena.get_paginator('get_query_results')
    results_iterator = results_paginator.paginate(
        QueryExecutionId=query_execution_id,
        PaginationConfig={
            'PageSize': PAGE_SIZE,
            'StartingToken': None
        }
    )

    for result in results_iterator:

        print("starting record set {}".format(count + 1))

        if not keys:
            keys = [c['VarCharValue'].encode('ascii', 'ignore') for c in result['ResultSet']['Rows'][0]['Data']]
            result['ResultSet']['Rows'].pop(0)

        with table.batch_writer() as batch:
            for row in result['ResultSet']['Rows']:
                values = [c.get('VarCharValue', '').encode('ascii', 'ignore') for c in row['Data']]
                item = dict(zip(keys, values))
                filtered = dict((k, v) for k, v in item.iteritems() if v)
                batch.put_item(Item=filtered)
                count += 1

        print("finished writing {} total records".format(count))

    return count

