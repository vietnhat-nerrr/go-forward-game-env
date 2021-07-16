from sys import modules
import numpy
import numpy.random
import json

def sigmoid(x):
    return(1/(1 + numpy.exp(-x)))

class ANN():
    def __init__(self, layers_unit, supervise=False, brain=None) -> None:
        """Create ANN netword

        Args:
            layers_unit (array): a list of number of unit for each layer, first layer is input layer
            supervise (bool, optional): will it be supervise. Defaults to False.
            brain (list of numpy array, optional): the layers that will be suppervise. Defaults to None.
        """

        self.layers_unit = layers_unit
        self.input_shape = layers_unit[0]
        self.layers_amount = len(layers_unit)
        self.layers = []

        if not supervise:
            for layer in self.layers_unit:
                self.layers.append(numpy.random.rand(layer)*2-1)
        else:
            if not brain:
                raise ValueError('Please provide brain to supervise')
            else:
                for i, layer in enumerate(brain):
                    if len(layer) != layers_unit[i]:
                        raise ValueError('Brain shape wrong at layer:', i)
                self.layers = brain

    def f_forward(self, x, w1):
        o1 = x.dot(w1)
        o1 = sigmoid(o1)
        return o1

    def get_step(self, x):
        x = numpy.asarray(x)

        if x.shape[0] != self.input_shape:
            raise ValueError('Input shape must have same length with first layer units')

        for index, layer in enumerate(self.layers):
            if index < self.layers_amount-1:
                output = self.f_forward(x, layer)
                x = numpy.ones(self.layers_unit[index+1]) * output
            else:
                return x

    def fuck_with(self, fwb, mutation=0.2):
        """Generate a new ANN model from 2

        Args:
            fwb (ANN): another model that will be crossover with
            mutation (float): a number between [0,1] for mutation ratio

        Returns:
            ANN: new model from input
        """
        if fwb.layers_unit != self.layers_unit:
            raise ValueError('2 Neural structure not match')

        child_layers = []
        
        for index, layer in enumerate(self.layers_unit):
            bed = numpy.concatenate([self.layers[index], fwb.layers[index]])
            numpy.random.shuffle(bed)

            child_seed = bed[:-layer]
    
            mutated = numpy.random.rand(layer)
            is_mutation = numpy.random.rand(layer) <= mutation
            child_seed[is_mutation] = mutated[is_mutation]
            child_layers.append(child_seed)

        child = ANN(layers_unit=self.layers_unit, supervise=True, brain=child_layers)
        return child

    def export_model(self, path):
        data = {}
        data['layers_unit'] = self.layers_unit
        for i in range(self.layers_amount):
            self.layers[i]
            data[i] = self.layers[i].tolist()
        with open(path, 'w') as f:
            f.write(json.dumps(data))
        pass

    @staticmethod
    def load_model(path):
        with open(path) as f:
            data = json.load(f)
            layers = []
            layers_unit = []
            for v in enumerate(data.values()):
                layers_unit.append(len(v))
                layers.append(v)
            return ANN(layers_unit=layers_unit, supervise=True, brain=layers)