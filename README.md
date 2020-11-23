## Instructions

Ensure you have both docker and docker-compose installed. Go to the project root and run the following command.

```
$ docker-compose up
```

### Troubleshooting

I've noticed some odd errors with docker-compose on windows based machines - if you're seeing database related errors in the logs, odds are the `depends` key in the configs aren't being respected. Cleaning the slate and restarting seems to work well.

```
$ docker-compose down --volume && docker-compose build --no-cache && docker-compose stop && docker-compose rm -f && docker-compose up
```
