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

$ curl -X DELETE -D - https://yourapiid.execute-api.ap-northeast-1.amazonaws.com/Prod/images/7f5e9a84-3207-4d29-a4b3-5aeb666fe2b2
```

vue cli projectの作成
```
$ vue init webpack serverless-spa
$ cd serverless-spa && npm install
$ npm run dev
```

vueアプリケーションのbuild
```
$ npm run build
```

S3 CORSの許可設定
```
$ aws s3api put-bucket-cors --bucket your-photos-bucket \
--cors-configuration file://cors.json
```

CORS設定確認
```
$ curl -I -X GET https://your-photos-bucket.s3-ap-northeast-1.amazonaws.com/example.png -H "Origin: http://example.com"
```

Cognito ユーザPoolの作成
```
$ aws cloudformation create-stack --stack-name your-user-pool-name \
--region ap-northeast-1 --template-body file://userpool-template.yaml
```
```
$ aws cloudformation describe-stacks --stack-name your-user-pool-name --region ap-northeast-1
```

Cognito SDKのインストール
```
$ npm install aws-sdk --save
$ npm install amazon-cognito-identity-js --save
```

spaのビルド & デプロイ
```
$ npm run build && cd dist
$ aws s3 sync . s3://your-application-bucket
```

kognition lambda関数の実行ロール
```
$ aws iam create-role --role-name lambda-imagerekognition-role \
--assume-role-policy-document file://trustpolicy_kognition.json
```
```
$ aws iam put-role-policy --role-name lambda-imagerekognition-role \
--policy-name lambda-imagerekognition-policy --policy-document file://permission_kognition.json
```

rekognition lambdaのデプロイ
```
$ cd lambda && aws cloudformation package --template-file template-rekognition.yaml --output-template-file template-rekognition-output.yaml --s3-bucket serverless-app-sam-letitride

$ aws cloudformation deploy --template-file template-rekognition-output.yaml --stack-name image-rekognition \
--capabilities CAPABILITY_IAM --region ap-northeast-1 
```

cloudformation stackのoutput確認
```
$ aws cloudformation describe-stacks --stack-name image-rekognition --region ap-northeast-1
```

lambda s3イベントリソースの設定 s3からの起動を許可
```
$ aws lambda add-permission --function-name image-rekognition-rekognizeImages-1L3ZDVBNMILN3 \
--action "lambda:InvokeFunction" --principal s3.amazonaws.com \
--source-arn "arn:aws:s3:::your-photos-bucket" \
--statement-id 1 --region ap-northeast-1
```

イベントリソースの定義
```
$ aws s3api put-bucket-notification-configuration --bucket your-photos-bucket --notification-configuration file://notification.json 
```