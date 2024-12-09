import cv2
from fer import FER
from fer.utils import draw_annotations
import matplotlib.pyplot as plt
import os
import pandas as pd
import config

detector = FER()

def detect_and_display_emotions():
    
    cap = cv2.VideoCapture(0)  # Открываем камеру

    emotions_data = []  # Список для хранения данных эмоций
    
    while True:
        ret, frame = cap.read()  # Считываем кадры с камеры
        if not ret:
            break
        
        # Детекция эмоций
        emotions = detector.detect_emotions(frame)
        frame = draw_annotations(frame, emotions)  # Добавляем аннотации с эмоциями на кадр
        
        # Сохраняем данные эмоций, если они есть
        if emotions:
            emotions_data.append(emotions[0]['emotions'])
        
        # Преобразуем кадр в формат JPEG
        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        
        if config.session_ended:
            process_emotions_data(emotions_data)
            break
        
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()

def process_emotions_data(emotions_data):
    """Функция для обработки и сохранения данных о эмоциях (построение графиков и таблиц)."""
    # Сохранение данных эмоций и графика после завершения анализа
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Преобразование данных эмоций в DataFrame
    emotions_df = pd.DataFrame(emotions_data)

    if not emotions_df.empty:
        # Заменяем английские названия эмоций на русские
        emotions_df.columns = ['Злость', 'Отвращение', 'Страх', 'Счастье', 'Грусть', 'Удивление', 'Нейтральное']

        # Применяем скользящее среднее для сглаживания
        smoothed_emotions_df = emotions_df.rolling(window=5, min_periods=1).mean()

        # Построение графика эмоций по времени
        plt.figure(figsize=(12, 6))
        for emotion in smoothed_emotions_df.columns:
            plt.plot(smoothed_emotions_df.index, smoothed_emotions_df[emotion], label=emotion)

        plt.title("Изменение эмоций с течением времени")
        plt.xlabel("Время (кадры)")
        plt.ylabel("Интенсивность эмоции")
        plt.legend()

        # Сохранение графика
        plot_path = os.path.join(output_dir, "emotion_timeline.png")
        try:
            plt.savefig(plot_path)
            print(f"График сохранен по пути: {plot_path}")
        except Exception as e:
            print(f"Ошибка при сохранении графика: {e}")
        plt.close()  # Закрыть график, чтобы освободить ресурсы

        # Суммарные значения эмоций за всё время с округлением до сотых
        total_emotions = emotions_df.sum().round(2)  # Получаем сумму для каждой эмоции и округляем до сотых
        total_emotions_df = pd.DataFrame({
            'Человеческие эмоции': total_emotions.index,
            'Значение эмоций из видео': total_emotions.values
        })

        # Сохранение таблицы с суммарными эмоциями
        table_path = os.path.join(output_dir, "total_emotion_data.html")
        try:
            total_emotions_df.to_html(table_path, index=False, escape=False)
            print(f"Таблица сохранена по пути: {table_path}")
        except Exception as e:
            print(f"Ошибка при сохранении таблицы: {e}")
        
        return plot_path, table_path