import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

kinesis = boto3.client('kinesis')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
  evnet_data = json.dumps(event,
    ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',',': ')
  )

  logging.info('Event' + evnet_data)
  # SNSからの通知メッセージ
  message = json.loads(event['Records'][0]['Sns']['Message'])
  logging.info("Message: " + str(message))

  alarm_name = message['AlarmName']
  stream_name = message['Trigger']['Dimensions'][0]['value']

  if alarm_name == 'kinesis-mon':
    #現在のオープンシャードサマリを取得
    stream_summary = kinesis.describe_stream_summary(
      StreamName=stream_name
    )
    current_open_shard_count = stream_summary['StreamDescriptionSummary']['OpenShardCount']
    
    #シャード数の変更
    target_shard_count = current_open_shard_count * 2
    logger.info("begin kinesis update")
    try:
      response = kinesis.update_shard_count(
        StreamName=stream_name,
        TargetShardCount=target_shard_count,
        ScalingType='UNIFORM_SCALING'
      )
      logger.info(response)
    except Exception as e:
      logger.info(e)

    logger.info("end kinesis update")

    #閾値の変更
    new_threshold = target_shard_count*1000*0.8
    logger.info("Set a threshold value to "+ str(new_threshold))
    response = cloudwatch.put_metric_alarm(
      ALarmName='kinesis-mon',
      MetricName='IncomingRecords',
      Namespace='AWS/Kinesis',
      Period=60,
      EvaluationPeriods=1,
      ComparisonOperator='GreaterThanThreshold',
      Threshold=new_threshold,
      Statistic='Sum'
    )