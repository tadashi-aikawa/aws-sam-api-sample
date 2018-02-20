aws-sam-api-sample
==================


For developer
-------------

### Package

```
$ aws cloudformation package \
    --template-file template.yaml \
    --output-template-file output-template.yaml \
    --s3-bucket mamansoft-aws-sam-api-sample
```

### Deploy

```
$ aws cloudformation deploy \
    --template-file output-template.yaml \
    --stack-name test \
    --capabilities CAPABILITY_IAM
```

### Run locally

Need to create `event.json`.

```
$ sam local invoke 'TestFunction' -e event.json
```

