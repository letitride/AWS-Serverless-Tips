kinesis streamの作成
```
$ aws kinesis create-stream --stream-name twitter-stream \
--shard-count 1
```

dynamodb tableの作成 partition=id, sort=timestamp
```
$ aws dynamodb create-table --table-name tweet-data \
--attribute-definitions AttributeName=id,AttributeType=N \
AttributeName=timestamp,AttributeType=N \
--key-schema AttributeName=id,KeyType=HASH \
AttributeName=timestamp,KeyType=RANGE \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

```
$ pip3 install TwitterAPI
```

lambdaの実行ロールの作詞
```
$ aws iam create-role --role-name process-tweet-data-role \
--assume-role-policy-document file://trustpolicy.json
```

```permission.json```
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:ListStreams",
        "logs:*",
        "kinesis:GetRecords"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:BatchWriteItem",
        "kinesis:GetShardIterator",
        "kinesis:DescribeStream"
      ],
      "Resource": [
        "arn:aws:kinesis:ap-northeast-1:****:stream/twitter-stream",
        "arn:aws:dynamodb:ap-northeast-1:****:table/tweet-data"
      ]
    }
  ]
}
```

作成したロールにポリシーを付与する
```
$ aws iam put-role-policy --role-name process-tweet-data-role \
--policy-name dynamodb-access --policy-document file://permission.json
```

デプロイパッケージの作成
```
$ cd  lambda && zip ../process-tweet-data.zip process-tweet-data.py && cd ../
```

デプロイ
```
$ aws lambda create-function --function-name process-tweet-data \
--zip-file fileb://process-tweet-data.zip \
--role arn:aws:iam::****:role/process-tweet-data-role \
--handler process-tweet-data.lambda_handler \
--runtime python3.6 \
--environment Variables={TABLE_NAME=tweet-data}
```

Lambda関数の起動トリガー
```
$ aws lambda create-event-source-mapping \
--event-source-arn arn:aws:kinesis:ap-northeast-1:****:stream/twitter-stream \
--function-name process-tweet-data \
--enabled --starting-position LATEST
```

アプリケーションの実行
```
$ python get-tweets.py
```