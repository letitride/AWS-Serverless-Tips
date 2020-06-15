S3 bucketの作成
```
$ aws s3 mb s3://your-application-bucket --region ap-northeast-1
```

S3 webホスティングのindexドキュメントの設定
```
$ aws s3 website s3://your-application-bucket/ --index-document index.html
```

bucketポリシーの設定
```
$ aws s3api put-bucket-policy --bucket your-application-bucket \
--policy file://policy.json
```

webapp s3アップロード
```
$ aws s3 sync ./webapp/ s3://your-application-bucket/
```

dynamodb table作成
```
$ aws dynamodb create-table --table-name photos \
--attribute-definitions AttributeName=photo_id,AttributeType=S \
--key-schema AttributeName=photo_id,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

画像用s3 bucketの作成
```
$ aws s3 mb s3://your-photos-bucket --region ap-northeast-1
$ aws s3 website s3://your-photos-bucket/ --index-document index.html
$ aws s3api put-bucket-policy --bucket your-photos-bucket \
--policy file://policy-of-photo-bucket.json
```

lambda用IAMロールの作成
```
$ aws iam create-role --role-name lambda-dynamodb-access \
--assume-role-policy-document file://trustpolicy.json
$ aws iam put-role-policy --role-name lambda-dynamodb-access \
--policy-name dynamodb-access \
--policy-document file://permission.json
```

sam デプロイ用bucketの作成
```
$ aws s3 mb s3://your-sam-bucket
```

```
$ aws cloudformation package --template-file template.yaml \
--output-template-file template-output.yaml \
--s3-bucket your-sam-bucket
```

```
$ aws cloudformation deploy --template-file template-output.yaml \
--stack-name your-sam-bucket --capabilities CAPABILITY_IAM \
--region ap-northeast-1 
```

APIのテスト実行
```
$ curl -X POST https://yourapiid.execute-api.ap-northeast-1.amazonaws.com/Prod/images -d '{"type":"image/jpeg","size":1}'

$ curl -X PUT -d '{"photo_id":"c9d06468-c508-4d5f-b8cf-7235e7989b3a","timestamp":1592126341,"status":"Uploaded"}' https://yourapiid.execute-api.ap-northeast-1.amazonaws.com/Prod/images

$ curl -X GET https://yourapiid.execute-api.ap-northeast-1.amazonaws.com/Prod/images

$ curl -X GET https://yourapiid.execute-api.ap-northeast-1.amazonaws.com/Prod/images/c9d06468-c508-4d5f-b8cf-7235e7989b3a
```

