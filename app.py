from flask import Flask, render_template, request, redirect, url_for
import os
import csv

app = Flask(__name__)

IMAGE_FOLDER = 'static/images'
images = sorted([img for img in os.listdir(IMAGE_FOLDER) if img.endswith(('.jpg', '.png', '.jpeg'))])
results = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.form['image']
        rating = request.form['rating']
        results.append({'image': image, 'rating': rating})

        if len(results) >= len(images):
            with open('results.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['image', 'rating'])
                writer.writeheader()
                writer.writerows(results)
            return "ありがとうございました。調査は完了しました。"

        return redirect(url_for('index'))

    current_image = images[len(results)]
    return render_template('index.html', image=current_image)
