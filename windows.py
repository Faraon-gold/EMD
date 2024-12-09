from flask import Flask, render_template, Response, request, send_file
import os
from werkzeug.utils import secure_filename
from realtime import detect_and_display_emotions  # Импортируем функцию для обработки видео
from main import process_file  # Импортируем функцию для обработки файла
import config 

app = Flask(__name__)

# Указываем директорию для сохранения загруженных файлов
OUTPUT_FOLDER = 'input'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}  # Пример поддерживаемых расширений

# Устанавливаем путь для загрузки
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Создаем папку для сохранения файлов, если она не существует
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    """Главная страница приложения"""
    return render_template('index.html')  # Шаблон с кнопками и пустыми блоками для видео и графиков

# Функция для проверки допустимых расширений
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/start_camera', methods=['GET'])
def start_camera():
    """Запуск камеры и обработка видео с эмоциями"""
    config.session_ended = False  # Обнуляем флаг завершения при начале новой сессии
    return Response(detect_and_display_emotions(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stop_session', methods=['POST'])
def stop_session():
    """Завершение сессии"""
    config.session_ended = True  # Устанавливаем флаг завершения сессии
    print(config.session_ended)
    return 'Сессия завершена!'

@app.route('/process_video', methods=['POST'])
def process_video():
    if 'file' not in request.files:
        return 'Нет файла', 400  # Если файл не найден в запросе, возвращаем ошибку
    
    file = request.files['file']  # Получаем файл из запроса
    if file.filename == '':
        return 'Файл не выбран', 400
    
    if file and allowed_file(file.filename):  # Проверка на разрешенные расширения
        filename = secure_filename(file.filename)  # Защищаем имя файла
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)  # Путь для сохранения файла
        file.save(file_path)  # Сохраняем файл на сервере
        
        try:
            # Обрабатываем файл с помощью вашей функции
            result_video_path = process_file(file_path)  # Получаем путь к результату обработки
            
            print(f"Файл обработан, путь к результату: {result_video_path}")
            
            # Проверка существования файла
            if not os.path.exists(result_video_path):
                return 'Ошибка: файл не найден после обработки.', 500
            
            # Возвращаем файл
            return send_file(result_video_path, mimetype='video/mp4')
        except Exception as e:
            return f"Ошибка при обработке файла: {str(e)}", 500  # Возвращаем ошибку обработки файла
    
    return 'Неверный формат файла', 400  # Если формат файла не поддерживается

if __name__ == '__main__':
    app.run(debug=True)
