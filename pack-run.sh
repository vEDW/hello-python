pack build hello-nkp --buildpack gcr.io/paketo-buildpacks/python --builder paketobuildpacks/builder:base

docker tag hello-nkp ericdewitte/hello-nkp:latest
docker push ericdewitte/hello-nkp:latest