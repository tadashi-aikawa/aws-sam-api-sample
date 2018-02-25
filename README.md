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


### Deploy

```
$ make deploy
```

