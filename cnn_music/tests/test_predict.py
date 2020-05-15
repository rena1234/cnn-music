from unittest import TestCase, main
from ..predict import predict_next
from numpy import array
from ..model import get_model

class TestModel(TestCase):
    def test_predicted_next(self):
        x = array([[0, 1, 1], [1, 1, 1], [0, 1, 1], [1, 1, 1]])
        y = array([1, 0, 1, 1])
        parameters = {
                "filters": 64,
                "kernel_size": 2,
                "activation": "relu",
                "pool_size": 2,
                "optimizer": "adam",
                "loss": "mse",
                "epochs": 1000,
                "verbose": 0,
                "dense_units": 50,
                "groups_size": 3,
                "validation": 0.2,
                }
        x = x.reshape((x.shape[0]), x.shape[1], 1)

        model = get_model(x, y, parameters)
        input = array([0, 1, 1])
        input = input.reshape((1,3,1))
        predict_next(input, model, 2)

if __name__ == '__main__':
    main()
