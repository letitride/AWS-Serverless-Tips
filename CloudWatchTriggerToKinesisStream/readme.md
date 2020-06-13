```
$ pip3 install boto3
```

kinesis data stream の作成 
```
$ aws kinesis create-stream --stream-name sample --shard-count 1
```

SNS トピックの作成
```
$ aws sns create-topic --name sample
```

CloudWatch メトリクスアラームの設定
```
$ aws cloudwatch put-metric-alarm \
--alarm-name kinesis-mon --metric-name IncomingRecords \
--namespace AWS/Kinesis --statistic Sum --period 60 \
--threshold 10 --comparison-operator GreaterThanThreshold \
--dimensions Name=StreamName,Value=sample \
--evaluation-periods 1 \
--alarm-actions arn:aws:sns:ap-northeast-1:****:sample
```

```--metric-name IncomingRecords```:モニタリング対象とするメトリクス
```--statistic```:取得する統計

```--period 60```:期間

```--threshold 10```:しきい値

```--comparison-operator GreaterThanThreshold```:比較条件

```--dimensions```:監視する属性

```--evaluation-periods```:アラートを上げるまでの連続発生回数

```--alarm-actions arn:aws:sns:ap-northeast-1:****:sample```:アラートの通知先

参考: https://docs.aws.amazon.com/ja_jp/streams/latest/dev/monitoring-with-cloudwatch.html


アラート状態の手動変更
```
$ aws cloudwatch set-alarm-state --alarm-name kinesis-mon \
--state-reason ‘initializing’ --state-value ALARM
```

lambdaの実行ロール作成
```
$ aws iam create-role --role-name resharding_function_role \
--assume-role-policy-document file://trustpolicy.json
```

作成したロールにポリシーをアタッチ
```
$ aws iam put-role-policy --role-name resharding_function_role \
--policy-name basic-permission \
--policy-document file://permission.json
```

lambda関数デプロイパッケージの作成
```
$ cd resharding-function/
$ zip -r9 ../resharding-function.zip *
```

lambda関数のデプロイ
```
$ aws lambda create-function --function-name resharding-function \
--zip-file fileb://resharding-function.zip \
--handler resharding-function.lambda_handler --runtime python3.6 \
--role arn:aws:iam::****:role/resharding_function_role 
```
```
$  aws lambda update-function-code --function-name resharding-function \
--zip-file fileb://resharding-function.zip
```

作成したLambda関数をSNSトピックの通知先として紐づける
```
$ aws lambda add-permission --function-name resharding-function \
--statement-id 1 --action "lambda:InvokeFunction" \
--principal sns.amazonaws.com \
--source-arn arn:aws:sns:ap-northeast-1:****:sample 
```

SNSサブスクリプションの登録
```
$ aws sns subscribe \
--topic-arn arn:aws:sns:ap-northeast-1:****:sample \
--protocol lambda --notification-endpoint arn:aws:lambda:ap-northeast-1:****:function:resharding-function
```

```
$ python put-records.py
$ aws kinesis describe-stream-summary --stream-name sample
```