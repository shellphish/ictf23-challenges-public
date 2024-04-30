import json

import numpy as np
import tensorflow as tf
from PIL import Image


def predict(architecture, weights, img):
    with open(architecture, 'r') as json_file:
        loaded_model_json = json_file.read()

    with open(weights, 'r') as json_file:
        loaded_weights_json = json.load(json_file)

    loaded_model = tf.keras.models.model_from_json(loaded_model_json)
    loaded_weights = [np.array(arr) for arr in loaded_weights_json]

    image = Image.open(img).convert("L")

    resized_image = image.resize((64, 64))
    image_array = np.array(resized_image, dtype=np.float32) / 255.0
    image_array = np.expand_dims(image_array, axis=-1)
    image_tensor = tf.convert_to_tensor(image_array, dtype=tf.float32)

    loaded_model.set_weights(loaded_weights)
    loaded_model.compile(optimizer='adam',
                         loss='categorical_crossentropy',
                         metrics=['accuracy'])

    results = list(loaded_model.predict(image_tensor[np.newaxis, ...])[0])
    number = results.index(max(results))

    print(f' Number detected is :{number}')
    print(f' Confidence is :{round(max(results)*100, 2)}%')


def main():
    BANNER = """
                ▓█████ ██▒   █▓ ██▓ ██▓        ███▄ ▄███▓ ▒█████  ▓█████▄ ▓█████  ██▓    
                ▓█   ▀▓██░   █▒▓██▒▓██▒       ▓██▒▀█▀ ██▒▒██▒  ██▒▒██▀ ██▌▓█   ▀ ▓██▒    
                ▒███   ▓██  █▒░▒██▒▒██░       ▓██    ▓██░▒██░  ██▒░██   █▌▒███   ▒██░    
                ▒▓█  ▄  ▒██ █░░░██░▒██░       ▒██    ▒██ ▒██   ██░░▓█▄   ▌▒▓█  ▄ ▒██░    
                ░▒████▒  ▒▀█░  ░██░░██████▒   ▒██▒   ░██▒░ ████▓▒░░▒████▓ ░▒████▒░██████▒
                ░░ ▒░ ░  ░ ▐░  ░▓  ░ ▒░▓  ░   ░ ▒░   ░  ░░ ▒░▒░▒░  ▒▒▓  ▒ ░░ ▒░ ░░ ▒░▓  ░
                 ░ ░  ░  ░ ░░   ▒ ░░ ░ ▒  ░   ░  ░      ░  ░ ▒ ▒░  ░ ▒  ▒  ░ ░  ░░ ░ ▒  ░
                   ░       ░░   ▒ ░  ░ ░      ░      ░   ░ ░ ░ ▒   ░ ░  ░    ░     ░ ░   
                   ░  ░     ░   ░      ░  ░          ░       ░ ░     ░       ░  ░    ░  ░
                    ░                                       ░                     """
    print(BANNER)
    architecture = './model_architecture.json'
    weights = './model_weights.json'

    try:
        while True:
            img = input('image file name (eg test.jpg) : ')
            predict(architecture=architecture, weights=weights, img=img)

    except KeyboardInterrupt:
        print("\nBye!!")

if __name__ == '__main__':
    main()