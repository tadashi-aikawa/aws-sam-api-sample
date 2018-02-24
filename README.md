aws-sam-api-sample
==================


For developer
-------------

### Run locally

1. `make init-db` (Only once)
2. `make build-with-install` (Only once)
3. `make dev EVENT=<*.json>`

* `<*.json>` accepts json files in a events directory
* Run `make clean-db` if you remove db and networks


### Package

```
$ aws cloudformation package \
    --template-file template.yaml \
    --output-template-file output-template.yaml \
    --s3-bucket mamansoft-aws-sam-sample
```

### Deploy

```
$ aws cloudformation deploy \
    --template-file output-template.yaml \
    --stack-name test \
    --capabilities CAPABILITY_IAM
```

