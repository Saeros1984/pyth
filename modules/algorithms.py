#learning algorithms here

class backPropagation():
    def getOutMistake(layer): #Computing mistake for output neurons
        for n in layer.neurons:
            n.q=n.out*(1-n.out)*n.mistake

