# this is where I will experiment with TensorFlow and its syntax

import tensorflow as tf
import numpy as np

# print('TensorFlow version:', tf.__version__)

mnist = tf.keras.datasets.mnist
# load the dataset of handwritten number

(x_train, y_train), (x_test, y_test) = mnist.load_data()
# dividing data set into training and testing would something similar to traffic assignment

x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
    # define the input layer
    tf.keras.layers.Flatten(input_shape=(28, 28)),

    # define the hidden layers and the activation function
    # the only way I can think of activation function is
    # it applies to the sum weight and then output a result that used for the next layer
    # it kind of like a probability in some case, how likely it will impact
    # that may be the weight job as well
    tf.keras.layers.Dense(128, activation='relu'),

    # define a probability that some of the neural net will be removed
    # avoid overfitting
    tf.keras.layers.Dropout(0.2),

    # output layers
    tf.keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
# logits scores, number divide between each number guess

probabilities = tf.nn.softmax(predictions).numpy()
# turn those scores into probabilites
# probabilities closed to 0.1, guess one out of ten

loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
# since guessing randomly with equal probabilities,
# can use the formula -tf.math.log(1/10) ~= 2.3 to predict the loss function for untrained model

# call before training the model
model.compile(optimizer = 'adam', # try to reduce the cost function
              loss = loss_fn, # loss function
              metrics = ['accuracy'])# reporting the probabilities of accuracy

model.fit(x_train, y_train, epochs = 5)
# fit method is used to adjust the model parameters and minimize loss
# epoch is how many time we want to train the model

model.evaluate(x_test, y_test, verbose=2)
# evaluate the model after training, print percentage of guess wrong and guess accruately
#print(loss_fn(y_train[:1], predictions).numpy())
