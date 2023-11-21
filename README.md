# Moneytolia API Demo

Moneytolia projesi için demo
Şunlar kullanılarak yapıldı: Python, Django, Docker, PostgreSQL and Grafana, Prometheus


### Kurulum (Docker - with make file):

- Build docker image
 ```sh
    $ make build
 ```

- Start url shortener service
 ```sh
    $ make start
 ```

- Stop url shortener service
 ```sh
    $ make stop
 ```

- Run tests for this project
 ```sh
    $ make test
 ```

- make command usage details
 ```sh
     $ make help
 ```


### Kurulum (Docker - without make file):

- Build docker image
 ```sh
    $ docker compose build
 ```

- Start url shortener service
 ```sh
    $ docker compose up --build -d
 ```

- Stop url shortener service
 ```sh
    $ docker compose down
 ```

- Run tests for this project
 ```sh
    $ docker compose exec flask-app python test.py
 ```


### Kurulum (without Docker):


- Start url shortener service
 ```sh
öncelikle 
python3.8 ile bir venv kurulur ve aktive edilir. sonra aşağıdaki kod çalıştırılır
pip install -r requirements.txt
sonra postgresqli pcmize kurup 
postgresql://postgres:Moneytolia123@localhost:5432/url_shortener
bu config ile ayağa kaldırmamız gerek.
dbname:url_shortener
username:postgres
dbpassword:Moneytolia123
sonra aşağıdaki kod çalıştırılır
    $ python url_shortener.py
 ```


- Run tests for this project
 ```sh
    $ python test.py
 ```


### API Docs.

Proje bu url'de dökümante edildi `<hostname>/swagger/`,
exp: http://localhost:5000/swagger/


aşağıda swagger arayüzü görülebilmektedir.
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/swagger-img1.png)
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/swagger-img2.png)
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/swagger-img3.png)

servisleri ayağa kaldırdıktan sonra, uygulamamıza gelen metrikleri görebilmemiz için aşağıdaki adımları uygulayıp grafana ve prometheus'u bağlamamız gerek
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana1.png)
admin admin kullanıcı adı ve şifresiyle giriş yap
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana2.png)
password change etmeden skip et
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana3.png)
burda ekranda data source ekleme kısmına geliriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana4.png)
prometheus'u seçeriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana5.png)
docker ile ayağa kalkan prometheus servisimizin url'ini gireriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana6.png)
save and test butonuna tıklarız ve build a dashboard deriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana7.png)
add visualization butonuna tıklarız
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana8.png)
prometheus'u seçeriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana9.png)
sol alttan metricleri seçebiliriz
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/grafana10.png)
bu şekilde görselleştirmesini sağlarız

prometheus arayüzü aşağıdaki gibidir.
![Swagger](https://github.com/selcukakarin/url-shortener/blob/main/img/prometheus.png)

istek atabileceğiniz python kodu
```
import requests
import json

url = "http://localhost:5000/shorten"

payload = json.dumps({
  "original_url": "https://flask-restx.readthedocs.io/en/latest/quickstart.html"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

istek atabileceğiniz curl
```
curl --location 'http://localhost:5000/shorten' \
--header 'Content-Type: application/json' \
--data '
{
    "original_url": "https://flask-restx.readthedocs.io/en/latest/quickstart.html"
}'

```