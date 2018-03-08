aws-sam-api-sample
==================


For developer
-------------

### Develop

```
make init
```


### Test

Prerequirements: `make init`

```
make test
```

### Run

#### Before run

```
make init-aws-local
make install-packages
```

`init-aws-local` shows

* MySQL
  * `docker-entrypoint-initdb.d/db-init.sql`
* S3
  * `s3/{bucket}/**`

#### As Lambda locally

```
make dev EVENT=<*.json> FUNCTION=*
```

* `<*.json>` accepts json files in a events directory

#### As API locally

```
make run-as-api
```

#### Show database

```
make db-clien
```

#### After run

```
make clean-aws-local
```


### Deploy

```
$ make deploy
```

