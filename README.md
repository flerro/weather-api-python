# weather-api-python

A minimal serverless API implementation in Python

Features:

- Lambda + DynamoDB + HttpApi (a cheaper alternative to RestApi)
- dynamodb mapping via [pynamodb](https://github.com/pynamodb/PynamoDB)


See also [similar project in Java](https://github.com/flerro/weather-api) 

## Prerequisites

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) already configured with Administrator permission   
- [SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)


## Usage

Create deployable artifact (source code + dependecies from `requirements.txt`):

```
❯ bin/package.sh
```

Deploy:

```
❯ sam deploy --guided
```

Invoke the remote endpoint:

```
❯ url=https://????.execute-api.eu-west-1.amazonaws.com/

# Add some data

❯ http $url/events < sample-payloads/oxford.json
❯ http POST $url/events < sample-payloads/brooklin.json

# Query data

❯ http GET "$url/locations?loc=Oxford, UK"
```