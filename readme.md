build:
docker compose build --no-cache
run:
docker compose up -d
check:
docker compose ps
test:
curl http://localhost:8085/hello
curl http://localhost/api/hello
curl http://localhost/api/student
