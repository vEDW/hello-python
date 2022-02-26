pack build hello-python --buildpack gcr.io/paketo-buildpacks/python --builder paketobuildpacks/builder:base

docker tag hello-python ericdewitte/hello-python:latest
docker push ericdewitte/hello-python:latest