from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import lstm
import time


def prepare_data(historical_data):
    closes = ''
    rows = historical_data.split('\n')
    for row in rows:
        col_num = 0
        for col in row.split(','):
            if col_num == 4:
                closes += col + '\n'
                break
            col_num += 1
    return closes



def predict(currency, current_price, historical_data):
    X_train, y_train, X_test, y_test = lstm.load_data(prepare_data(historical_data), 50, True)
    model = Sequential()

    model.add(LSTM(
        input_dim=1,
        output_dim=50,
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        100,
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=1))
    model.add(Activation('linear'))

    start = time.time()
    model.compile(loss='mse', optimizer='rmsprop')
    print('compilation time : ', time.time() - start)
    model.fit(
        X_train,
        y_train,
        batch_size=512,
        nb_epoch=1,
        validation_split=0.05)
    predictions = lstm.predict_sequences_multiple(model, X_test, 50, 50)
    #lstm.plot_results_multiple(predictions, y_test, 50)

    p = predictions[len(predictions) - 1]
    pi = p[len(p) - 1]

    prediction = 'down'

    if pi >= 0:
        prediction = 'up'

    return prediction, str(int(round(abs(pi*100))))