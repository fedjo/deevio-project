# deevio predictionsapp

## Scope
Modern manufacturing processes have a high degree of automation and at the same time high
quality requirements. Our machine vision solution helps ensuring these quality requirements are
met by providing means for automatic recognition of defects. In addition to the recognition, it is
essential to store the data about defects. This is mandatory for us to constantly improve our
models. Also, our customers need be able to analyze for example common defect types.

## Prerequisites
The service runs on a docker container and set up was implemented using
docker-compose

## Requirements
- git
- docker
- docker-compose

## Usage
1. Clone this repo and go to repo folder
```
git clone https://github.com/fedjo/deevio-project.git && cd deevio-project
```
2. Build docker image of the developed web service
```
$ ./build.sh <TAG>
```
3. Set docker containers running
```
docker-compose up -d
```
4. Examine app logs
```
docker-compose logs -f app
```

For more info please read the [docs](doc/)
