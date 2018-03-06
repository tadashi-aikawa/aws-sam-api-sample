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


### Run lambda locally

1. `make init-db` (Only once)
2. `make build-with-install` (Only once)
3. `make dev EVENT=<*.json> FUNCTION=*`

* `<*.json>` accepts json files in a events directory
* Run `make clean-db` if you remove db and networks


### Run API locally

1. `make init-db` (Only once)
2. `make build-with-install` (Only once)
3. `make api`

* Run `make clean-db` if you remove db and networks


### Deploy

```
$ make deploy
```

