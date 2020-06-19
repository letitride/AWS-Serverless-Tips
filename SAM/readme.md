パッケージング
```
$ aws cloudformation package --template-file sample-sam.yaml --output-template-file sample-sam-output.yaml --s3-bucket serverless-app-sam-letitride
```

デプロイ
```
$ aws cloudformation deploy --template-file sample-sam-output.yaml --stack-name sample-sam-stack --capabilities CAPABILITY_IAM
```

SAM ローカル環境用開発ツール
```
$ npm install -g aws-sam-local
```

SAM ローカル環境コンテナ起動 Docker engineが起動していること
```
$ sam local start-api --template sample-sam.yaml
```