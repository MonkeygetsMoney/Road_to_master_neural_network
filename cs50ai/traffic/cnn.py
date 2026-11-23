import tensorflow as tf

flower_mnist = tf.keras.datasets.cifar10

(train_images, train_labels), (test_images, test_labels) = flower_mnist.load_data()

# normalize pixel values to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0

# the image is 32x32 with 3 color inputs

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(32,32,3)),
    # do some convolution to get a specific feature out of the images

    tf.keras.layers.MaxPool2D((2,2)),
    # reduce the size of the image, get faster computation

    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPool2D((2,2)),

    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_images, train_labels, epochs=10)
model.evaluate(test_images, test_labels, verbose=2)