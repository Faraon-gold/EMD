import cv2
import os
import matplotlib.pyplot as plt
import pandas as pd
from deepface import DeepFace

# Загрузка каскада классификатора для обнаружения лиц
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_and_display_emotions():
    # Начало захвата видео
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Не удалось открыть камеру!")
        return

    emotions_data = []  # Список для хранения данных эмоций

    while True:
        # Захват кадра
        ret, frame = cap.read()
        if not ret:
            break

        # Преобразование кадра в оттенки серого
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Преобразование серого кадра в RGB-формат
        rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

        # Обнаружение лиц на кадре
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Извлечение области интереса (ROI) лица
            face_roi = rgb_frame[y:y + h, x:x + w]

            # Анализ эмоций на области лица
            result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

            # Сохраняем данные всех эмоций для каждого кадра
            emotions_data.append(result[0]['emotion'])

            # Определение доминирующей эмоции
            emotion = result[0]['dominant_emotion']

            # Рисование прямоугольника вокруг лица и отображение эмоции
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Отображение кадра с детекцией эмоций
        cv2.imshow('realtime', frame)  # Изменение названия окна

        # Обработчик закрытия окна: нажмите 'q' или закройте окно
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('realtime', cv2.WND_PROP_VISIBLE) < 1:
            break

    # Освобождение захвата и закрытие всех окон
    cap.release()
    cv2.destroyAllWindows()

    # Сохранение данных эмоций и графика после завершения анализа
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Преобразование данных эмоций в DataFrame
    emotions_df = pd.DataFrame(emotions_data)
    
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
    plt.savefig(plot_path)

    # Суммарные значения эмоций за всё время с округлением до сотых
    total_emotions = emotions_df.sum().round(2)  # Получаем сумму для каждой эмоции и округляем до сотых
    total_emotions_df = pd.DataFrame({
    'Человеческие эмоции': total_emotions.index, 
    'Значение эмоций из видео': total_emotions.values
    })

    # Сохранение таблицы с суммарными эмоциями
    table_path = os.path.join(output_dir, "total_emotion_data.html")
    total_emotions_df.to_html(table_path, index=False, escape=False)

