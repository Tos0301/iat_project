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

    current_index = len(results)
    total_images = len(images)
    current_image = images[current_index]
    return render_template('index.html',
                           image=current_image,
                           progress=f"{current_index + 1} / {total_images}")



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
