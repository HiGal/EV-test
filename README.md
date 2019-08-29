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

### Функционал

![image](https://user-images.githubusercontent.com/35590424/63963836-88c89100-ca9e-11e9-9ba3-8924de53c567.png)
![image](https://user-images.githubusercontent.com/35590424/63963951-b9102f80-ca9e-11e9-9561-2f01124cbcc7.png)
![image](https://user-images.githubusercontent.com/35590424/63963981-c4fbf180-ca9e-11e9-9345-d3f91120f0d3.png)

**Изображения на вкладке Result отображаются последовательно в порядке исчез/появился, после окончания процесса детектирования, обработанное видео будет доступно для загрузки**

![image](https://user-images.githubusercontent.com/35590424/63963804-78b0b180-ca9e-11e9-9184-33512b010c72.png)
