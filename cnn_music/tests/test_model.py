from ..model import get_model_inputs, get_model
from unittest import TestCase, main
from numpy import array

class TestModel(TestCase):
    def test_get_model_inputs(self):
        int_notes = [0, 1, 1, 0]
        sequence_length = 2;
        expected = ([[0, 1], [1, 1]], [1, 0])
        model_inputs = get_model_inputs(int_notes, 2)
        self.assertEqual(model_inputs, expected)
    
    def test_get_model(self):
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
                "validation": 0.2
                }
        x = x.reshape((x.shape[0]), x.shape[1], 1)
        model = get_model(x, y, parameters)

if __name__ == '__main__':
    main()
