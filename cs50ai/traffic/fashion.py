import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

# try to make a neural network that can classifies images of clothing
# kind of a 'hello work' of ML programs for computer vision

fashion_mnist = tf.keras.datasets.fashion_mnist

# divide into train datasets and test datasets
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

# 28x28 arrays, with pixels values range from 0 to 255
# label ranges from 0 to 9 for each type of clothings
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# inspect the first image from range of 0 to 255
# plt.figure()
# plt.imshow(train_images[0], cmap=plt.cm.binary)
# plt.colorbar()
# plt.grid(False)
# plt.show()

# have to process those value from 0 to 1 by divide 255
train_images = train_images / 255.0
test_images = test_images / 255.0

# show 25 images in black and white
# plt.figure(figsize=(10, 10))
# for i in range(25):
#     plt.subplot(5,5,i+1) # moving position
#     plt.xticks([])
#     plt.yticks([])
#     plt.grid(False)
#     plt.imshow(train_images[i])
#     plt.xlabel(class_names[train_labels[i]], cmap=plt.cm.binary)
#     # show images in binary code
# plt.show()

# build the model
model = tf.keras.Sequential([
    # flatten is for input shape
    tf.keras.layers.Flatten(input_shape=(28,28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])

# compile the model - tell the model the way it's going to learn
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs = 10)
model.evaluate(test_images, test_labels, verbose=2)

# the fit accuracy or training come out to around 91%
# while the evaluate accuracy come out to only 88%
# this gap show overfitting, which is why we can incorporate dropout
# we can also add weight regularization
# can also combine them both

# Making predictions
probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)

def plot_image(i, predictions_array, true_label, img):
    true_label, img = true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    # check if the predict label is correct
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel('')

def plot_value_array(i, predictions_array, true_label):
    true_label = true_label[i]
    plt.grid(False)
    plt.xticks(range(10)) # label number 0 - 9
    plt.yticks([])
    thisplot = plt.bar(range(10), predictions_array, color='#777777')
    plt.ylim([0,1])
    predicted_label = np.argmax([predictions_array])

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')

# show the prediction scores for 15 images
num_rows = 5
num_cols = 3
num_images = num_cols*num_rows
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
    plt.subplot(num_rows, 2*num_cols, 2*i+1)
    plot_image(i, predictions[i], test_labels, test_images)
    plt.subplot(num_rows, 2*num_cols, 2*i+2)
    plot_value_array(i, predictions[i], test_labels)
plt.tight_layout()
plt.show()
