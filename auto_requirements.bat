@echo off
echo Installing required libraries...

pip install matplotlib
pip install "keras>=2.0.0"
pip install opencv-python
pip install opencv-contrib-python
pip install pandas
pip install Pillow
pip install requests
pip install facenet-pytorch
pip install "tqdm>=4.62.1"
pip install "moviepy==1.0.3"
pip install deepface
pip install tf_keras
pip install tk


echo Installation complete.
pause
