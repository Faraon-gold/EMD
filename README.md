# EMD v 1.01
EDM - приложения для распознавания человеческих эмоций на основе видеоизображения. Приложение поддерживает два способа предоставления видео: просмотр в реальном времени и на основе готового видео. После обработки видео в папке `output` появятся график изменений эмоций с течением времени и таблица в которой отражены эмоции и суммарная их сила на протяжении всего видео.
В приложении реализовано распознавание 7 видов эмоций: Злость, Отвращение, Страх, Счастье, Грусть, Удивление, Нейтральное.

# Установка библиотек
## Автоматическая установка
Чтобы автоматически установить все библиотеки необходимо запустить файл `auto_requirements.bat` и дождаться установки всех библиотек
## Ручная установка
Чтобы установить библиотеки в ручном режиме необходимо в командной строке `cmd` прописать `pip install` и название библиотек поочередно. Или можно также в командной строке `cmd` прописать следующие команды:
`cd путь к файлу requirements.txt` после этого команду `pip install -r requirements.txt`
# Запуск EMD
Запуск приложения осуществляется файлом `run.bat`. После появится окно в котором нужно выбрать способ предоставления видеоизображения.

