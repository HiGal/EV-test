## Установка

### Python
```bash
git clone https://github.com/HiGal/EV-test.git
cd EV-test/
```
```bash
## установка виртуальной среды
pip install virtualenv

python3 -m venv env

source env/bin/activate

## установка необходимых пакетов
pip install -r requirements.txt
```
### Сборка из Docker образа
```bash
git clone https://github.com/HiGal/EV-test.git
cd EV-test/
```
```bash
docker build --tag=<tag_name> .
```
## Запуск веб-приложения

### Docker
```bash
docker run -p 4000:80 <tag_name>
```
```http
http://localhost:4000/
```

### Python
```bash
python app.py
```
```http
http://localhost:5000/
```
