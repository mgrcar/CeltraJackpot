from flask import Flask
import random
app = Flask(__name__)

@app.route('/<example>/machines')
def machines(example):
    """
    Return number of machine for <example>
    :param example: specified example number
    :return:
    """
    try:
        return {
            '1': '2',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '10',
            '6': '2',
            '7': '2',
            '8': '3',
            '9': '4',
            '10': '10',
            '11': '10',
            }[example]
    except:
        return "ERR"

@app.route('/<example>/pulls')
def pulls(example):
    """
    Return length of session for specified <example>
    :param example: specified example number
    :return:
    """
    try:
        return {
            '1': '500',
            '2': '10000',
            '3': '1000',
            '4': '10000',
            '5': '10000',
            '6': '1000',
            '7': '15000',
            '8': '3000',
            '9': '30000',
            '10': '30000',
            '11': '30000',
        }[example]
    except:
        return "ERR"

@app.route('/<example>/<bandit>/<sequence>')
def pull(example, bandit, sequence):
    """
    Return reward for given example, arm and session sequence
    :param example:
    :param bandit:
    :param sequence:
    :return:
    """
    try:
        return {
            '1': {
                '1': ("1" if random.random() < 0.4 else "0") if 1 <= int(sequence) <= 500 else "ERR",
                '2': ("1" if random.random() < 0.6 else "0") if 1 <= int(sequence) <= 500 else "ERR"
            },
            '2': {
                '1': ("1" if random.random() < 0.03 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '2': ("1" if random.random() < 0.015 else "0") if 1 <= int(sequence) <= 10000 else "ERR"
            },
            '3': {
                '1': ("1" if random.random() < 0.2 else "0") if 1 <= int(sequence) <= 1000 else "ERR",
                '2': ("1" if random.random() < 0.15 else "0") if 1 <= int(sequence) <= 1000 else "ERR",
                '3': ("1" if random.random() < 0.1 else "0") if 1 <= int(sequence) <= 1000 else "ERR"
            },
            '4': {
                '1': ("1" if random.random() < 0.02 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '2': ("1" if random.random() < 0.0175 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '3': ("1" if random.random() < 0.02375 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '4': ("1" if random.random() < 0.0228 else "0") if 1 <= int(sequence) <= 10000 else "ERR"
            },
            '5': {
                '1': ("1" if random.random() < 0.010420 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '2': ("1" if random.random() < 0.010300 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '3': ("1" if random.random() < 0.010020 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '4': ("1" if random.random() < 0.010260 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '5': ("1" if random.random() < 0.010540 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '6': ("1" if random.random() < 0.009480 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '7': ("1" if random.random() < 0.009360 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '8': ("1" if random.random() < 0.010180 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '9': ("1" if random.random() < 0.009520 else "0") if 1 <= int(sequence) <= 10000 else "ERR",
                '10': ("1" if random.random() < 0.012880 else "0") if 1 <= int(sequence) <= 10000 else "ERR"
            },
            '6': {
                '1': ("1" if random.random() < 0.6 else "0") if 1 <= int(sequence) < 500
                else ("1" if random.random() < 0.4 else "0") if 500 <= int(sequence) <= 1000
                else "ERR",
                '2': ("1" if random.random() < 0.4 else "0") if 1 <= int(sequence) < 500
                else ("1" if random.random() < 0.6 else "0") if 500 <= int(sequence) <= 1000
                else "ERR",
            },
            '7': {
                '1': ("1" if random.random() < 0.03 else "0") if 1 <= int(sequence) < 3000
                else ("1" if random.random() < 0.02 else "0") if 3000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.03 else "0") if 12000 <= int(sequence) <= 15000
                else "ERR",
                '2': ("1" if random.random() < 0.015 else "0") if 1 <= int(sequence) < 3000
                else ("1" if random.random() < 0.04 else "0") if 3000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.015 else "0") if 12000 <= int(sequence) <= 15000
                else "ERR",
                },
            '8': {
                '1': ("1" if random.random() < 0.2 else "0") if 1 <= int(sequence) < 1400
                else ("1" if random.random() < 0 else "0") if 1400 <= int(sequence) <= 2200
                else ("1" if random.random() < 0.2 else "0") if 2200 <= int(sequence) <= 3000
                else "ERR",
                '2': ("1" if random.random() < 0.15 else "0") if 1 <= int(sequence) < 1400
                else ("1" if random.random() < 0.3 else "0") if 1400 <= int(sequence) <= 2200
                else ("1" if random.random() < 0.0 else "0") if 2200 <= int(sequence) <= 3000
                else "ERR",
                '3': ("1" if random.random() < 0.1 else "0") if 1 <= int(sequence) <= 3000 else "ERR"
            },
            '9': {
                '1': ("1" if random.random() < 0 else "0") if 1 <= int(sequence) < 11000
                else ("1" if random.random() < 0.021 else "0") if 11000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.021 else "0") if 12000 <= int(sequence) <= 13000
                else ("1" if random.random() < 0.02 else "0") if 13000 <= int(sequence) <= 14000
                else ("1" if random.random() < 0.018 else "0") if 14000 <= int(sequence) <= 15000
                else ("1" if random.random() < 0.021 else "0") if 15000 <= int(sequence) <= 16000
                else ("1" if random.random() < 0.019 else "0") if 16000 <= int(sequence) <= 17000
                else ("1" if random.random() < 0.021 else "0") if 17000 <= int(sequence) <= 18000
                else ("1" if random.random() < 0.022 else "0") if 18000 <= int(sequence) <= 19000
                else ("1" if random.random() < 0.021 else "0") if 19000 <= int(sequence) <= 20000
                else ("1" if random.random() < 0.0195 else "0") if 20000 <= int(sequence) <= 21000
                else ("1" if random.random() < 0.022 else "0") if 21000 <= int(sequence) <= 22000
                else ("1" if random.random() < 0.018 else "0") if 22000 <= int(sequence) <= 23000
                else ("1" if random.random() < 0.02 else "0") if 23000 <= int(sequence) <= 24000
                else ("1" if random.random() < 0.02 else "0") if 24000 <= int(sequence) <= 25000
                else ("1" if random.random() < 0.02 else "0") if 25000 <= int(sequence) <= 26000
                else ("1" if random.random() < 0.019 else "0") if 26000 <= int(sequence) <= 27000
                else ("1" if random.random() < 0.02 else "0") if 27000 <= int(sequence) <= 28000
                else ("1" if random.random() < 0.022 else "0") if 28000 <= int(sequence) <= 29000
                else ("1" if random.random() < 0.022 else "0") if 29000 <= int(sequence) <= 30000
                else "ERR",
                '2': ("1" if random.random() < 0 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '3': ("1" if random.random() < 0 else "0") if 1 <= int(sequence) < 11000
                else ("1" if random.random() < 0.018 else "0") if 11000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.02 else "0") if 12000 <= int(sequence) <= 13000
                else ("1" if random.random() < 0.023 else "0") if 13000 <= int(sequence) <= 14000
                else ("1" if random.random() < 0.027 else "0") if 14000 <= int(sequence) <= 15000
                else ("1" if random.random() < 0.025 else "0") if 15000 <= int(sequence) <= 16000
                else ("1" if random.random() < 0.022 else "0") if 16000 <= int(sequence) <= 17000
                else ("1" if random.random() < 0.025 else "0") if 17000 <= int(sequence) <= 18000
                else ("1" if random.random() < 0.023 else "0") if 18000 <= int(sequence) <= 19000
                else ("1" if random.random() < 0.02 else "0") if 19000 <= int(sequence) <= 20000
                else ("1" if random.random() < 0.0235 else "0") if 20000 <= int(sequence) <= 21000
                else ("1" if random.random() < 0.025 else "0") if 21000 <= int(sequence) <= 22000
                else ("1" if random.random() < 0.025 else "0") if 22000 <= int(sequence) <= 23000
                else ("1" if random.random() < 0.022 else "0") if 23000 <= int(sequence) <= 24000
                else ("1" if random.random() < 0.0245 else "0") if 24000 <= int(sequence) <= 25000
                else ("1" if random.random() < 0.022 else "0") if 25000 <= int(sequence) <= 26000
                else ("1" if random.random() < 0.023 else "0") if 26000 <= int(sequence) <= 27000
                else ("1" if random.random() < 0.023 else "0") if 27000 <= int(sequence) <= 28000
                else ("1" if random.random() < 0.02 else "0") if 28000 <= int(sequence) <= 29000
                else ("1" if random.random() < 0.02 else "0") if 29000 <= int(sequence) <= 30000
                else "ERR",
                '4': ("1" if random.random() < 0 else "0") if 1 <= int(sequence) <= 30000 else "ERR"
            },
            '10': {
                '1': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 6000
                else ("1" if random.random() < 0.02 else "0") if 6000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.01 else "0") if 12000 <= int(sequence) <= 30000
                else "ERR",
                '2': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 6000
                else ("1" if random.random() < 0.02 else "0") if 6000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.01 else "0") if 12000 <= int(sequence) <= 30000
                else "ERR",
                '3': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 6000
                else ("1" if random.random() < 0.02 else "0") if 6000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.01 else "0") if 12000 <= int(sequence) <= 30000
                else "ERR",
                '4': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 6000
                else ("1" if random.random() < 0.02 else "0") if 6000 <= int(sequence) <= 12000
                else ("1" if random.random() < 0.01 else "0") if 12000 <= int(sequence) <= 30000
                else "ERR",
                '5': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 12000
                else ("1" if random.random() < 0.02 else "0") if 12000 <= int(sequence) <= 24000
                else ("1" if random.random() < 0.01 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",
                '6': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 12000
                else ("1" if random.random() < 0.02 else "0") if 12000 <= int(sequence) <= 24000
                else ("1" if random.random() < 0.01 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",
                '7': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 12000
                else ("1" if random.random() < 0.02 else "0") if 12000 <= int(sequence) <= 24000
                else ("1" if random.random() < 0.01 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",
                '8': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 24000
                else ("1" if random.random() < 0.02 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",
                '9': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 24000
                else ("1" if random.random() < 0.02 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",
                '10': ("1" if random.random() < 0.01 else "0") if 1 <= int(sequence) < 24000
                else ("1" if random.random() < 0.02 else "0") if 24000 <= int(sequence) <= 30000
                else "ERR",

            },
            '11': {
                '1': ("1" if random.random() < 0.010420 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '2': ("1" if random.random() < 0.010300 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '3': ("1" if random.random() < 0.010020 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '4': ("1" if random.random() < 0.010260 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '5': ("1" if random.random() < 0.010540 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '6': ("1" if random.random() < 0.009480 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '7': ("1" if random.random() < 0.009360 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '8': ("1" if random.random() < 0.010180 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '9': ("1" if random.random() < 0.009520 else "0") if 1 <= int(sequence) <= 30000 else "ERR",
                '10': ("1" if random.random() < 0.012880 else "0") if 1 <= int(sequence) <= 30000 else "ERR"
            },


        }[example][bandit]
    except:
        return "ERR"

if __name__ == '__main__':
    app.run(debug=True)