import numpy as np

class mlp:
    def __init__(self, inputs, targets, nhidden):
        self.beta = 1
        self.eta = 0.1
        self.momentum = 0.0
        self.nhidden = nhidden
        self.target_len = len(targets[0])

        # Create weights with random numbers spanning from -0.5 to 0.5
        self.input_weights = np.random.uniform(-2,2,(nhidden,len(inputs[0])+1))
        self.hidden_weights = np.random.uniform(-2,2,(len(targets[0]), nhidden+1))

    def earlystopping(self, inputs, targets, valid, validtargets):
        """Runs the training of the network
        Trains the network for a given (100) number of epochs
        and for each such iteration checks with the controlset
        of valid-inputs/-targets if the network has indeed improved
        since last iteration. If the improvement is negative or too
        small the network will stop training to avoid over-fitting.

        Arguments:
        inputs (numpy-array):          Inputs for training the MLP
        targets (numpy-array):         Target outputs for the inputs        
        valid (numpy-array):           Control-set of inputs
        validtargets (numpy-array):    Control-set of output
        """
        old_error1 = 100002
        old_error2 = 100001
        new_error = 100000
        
        # add bias nodes to the input-arrays
        inputs = self.add_bias_node(inputs)
        valid = self.add_bias_node(valid)
       
        while (((old_error1-new_error)>0.001) or ((old_error2 - old_error1)>0.001)):
            # train the network
            self.train(inputs,targets)
            old_error2 = old_error1
            old_error1 = new_error
            # save the errors from control-set
            valid_hidden, valid_out = self.forward(valid)
            valid_error = np.zeros((len(validtargets),len(validtargets[0])))
            for i in range(len(valid_error)):
                for j in range(len(valid_error[i])):
                    valid_error[i,j] = validtargets[i,j] - valid_out[i,j]
            valid_error = self.array_sum(valid_error)
            new_error = 0.5*(valid_error**2)

    def train(self, inputs, targets, iterations=100):
        """Trains the network
        Using the inputs the training function runs the
        values forward through the network in one epoch per iteration.
        Then it takes the actual outputs of the output- and
        hidden-layer and evaluates new values for the weights
        using the backpropagation function.
        
        Arguments:
        inputs (numpy-array):          Inputs to train the network
        targets (numpy-array):         Target values for output layer
        iterations (integer):          Number of epochs to run
        Returns:
        """
        for i in range(iterations):
            actual_hidden, actual_out = self.forward(inputs)
            self.back_propagation(inputs, actual_hidden, actual_out, targets)

    def forward(self, inputs):
        """ Runs the network forward
        Feeds the network with the inputs and calculates
        values of the hidden neurons and the output layer
        based on the input and the current value in the weights.
        Activates the neurons using the sigmoid-functions.

        Arguments:
        inputs (numpy-array):          List of inputs
        Return:
        actual_hidden (numpy-array):   List of outputs from the output layer
        actual_output (numpy-array):   List of outputs from the hidden layer
        """

        # Find actual values for nodes in hidden layer from inputs
        actual_hidden = np.zeros((len(inputs),self.nhidden))
        for i in range(len(inputs)):
            for w in range(len(self.input_weights)):
                for j in range (len(inputs[i])):
                    actual_hidden[i,w] += inputs[i,j]*self.input_weights[w,j]
        
        # Hidden layer activation
        for i in range(len(actual_hidden)):
            for j in range(len(actual_hidden[i])):
                actual_hidden[i,j] = self.sigmoid(self.beta*actual_hidden[i,j])
        actual_hidden = self.add_bias_node(actual_hidden)

        # Find actual values in outputs from hidden layer
        actual_output = np.zeros((len(inputs), self.target_len))
        for i in range(len(actual_hidden)):
            for w in range(len(self.hidden_weights)):
                for j in range(len(actual_hidden[i])):
                    actual_output[i,w] += actual_hidden[i,j]*self.hidden_weights[w,j]
        
        # Output activation
        for i in range(len(actual_output)):
            for j in range(len(actual_output[i])):
                actual_output[i][j] = self.threshold_activation(self.beta*actual_output[i][j])
        return actual_hidden, actual_output

    def back_propagation(self, inputs, actual_hidden, actual_output, targets):
        """Back propagation for correcting weights
        Finds the error value of the actual output of the output-layer
        and hidden layer of the MLP and adjusts the weights.

        Arguments:
        inputs (numpy-array):          List of the given inputs
        actual_hidden (numpy-array):   Output values of the hidden layer
        actual_output (numpy-array):   Output value of the output layer
        targets (numpy-array):         List of correct targets for the MLP
        """

        # output_delta = (output-targets)*actual*(1-actual)
        output_delta = np.zeros((len(actual_output),len(actual_output[0])))
        for i in range(len(output_delta)):
                for j in range(len(output_delta[i])):
                    output_delta[i,j] = (actual_output[i,j] - targets[i,j])
        # hidden_delta = (outputdeltas*hidden_weights)*actual_hidden*(1-actual_hidden)
        hidden_delta = np.zeros((len(output_delta), self.nhidden))
        # for each run
        for i in range(len(output_delta)):
            # for each hidden node
                for j in range(self.nhidden):
                    # for each output
                        for o in range(len(output_delta[i])):
                            hidden_delta[i,j] += output_delta[i,o]*self.hidden_weights[o,j]*(1-self.hidden_weights[o,j])
        
        # Weights -= eta(learningrate) * layer_delta * input
        # for each hidden node + bias
        for i in range(self.nhidden+1):
            # for each output
            for j in range(len(self.hidden_weights)):
                # for each run
                for r in range(len(actual_hidden)):
                    self.hidden_weights[j,i] -= output_delta[r,j]*actual_hidden[r,i]

        # for each input node + bias
            for i in range(len(self.input_weights[0])):
                # for each hidden node
                for j in range(len(self.input_weights)):
                    # for each run
                    for r in range(len(inputs)):
                        self.input_weights[j,i] -= hidden_delta[r,j]*inputs[r,i]

    def add_bias_node(self, array):
        """ Add bias node to node-array(neurons)
        Adds bias nodes with value 1.0 to the last 
        column in the array.

        Arguments:
        array (numpy-array):    Sets of nodes
        Returns:
        array (numpy-array):    Sets with bias
        """
        ret_array = np.ones((len(array),len(array[0])+1))
        for i in range(len(array)):
            for j in range(len(array[i])):
                ret_array[i,j] = array[i][j]
        return ret_array

    def array_sum(self, array):
        """Returns sum of array
        Adds all individual values in a 2D-array
        together and returns the sum.

        Arguments:
        array (numpy-array):    2D-array of values
        Result:
        summed (integer):       Sum of the array

        """
        summed = 0.0
        for i in range(len(array)):
            for j in range(len(array[i])):
                summed += array[i,j]
        return summed

    def threshold_activation(self, x):
        """Activates the output node
        Activates the activation node if the
        input from the hidden nodes*weights
        evaluates to more than zero.

        Arguments:
        x (float):      Given x for activation
        Returns:
        value (float):  Results of activation
        """
        if x > 0:
            return 1.0
        else:
            return 0.0

    def sigmoid(self, x):
        """Sigmoid function for "x"
        Returns the value given by the
        sigmoid function for the value "x"

        Arguments:
        x (float):      Given x for function
        Returns:
        value (float):  Result of function
        """
        return 1/(1+np.exp(-x))

    def confusion(self, inputs, targets):
        """Prints a confusion table for the MLP
        Sends in a control set of inputs and compares
        it with the correct targets in a 2D-matrix
        where one axis is the targets and the
        other is the solutions found by the MLP.

        Arguments:
        inputs (numpy-array):   List of inputs
        targets (numpy-array):  List of targets

        """
        confusion_matrix = np.zeros((len(targets[0]),len(targets[0])))
    
        inputs = self.add_bias_node(inputs)
        actual_hidden, actual_output = self.forward(inputs)

        for i in range(len(targets)):
            for j in range(len(targets[i])):
                if(targets[i,j] == 1.0):
                    confusion_matrix[j,j] += targets[i,j]
                    for k in range(len(actual_output[i])):
                        confusion_matrix[k,j] += actual_output[i,k]
        correct = 0
        for i in range(len(confusion_matrix)):
            correct += confusion_matrix[i,i]

        incorrect = self.array_sum(confusion_matrix) - correct
        print("hidden nodes:  ", self.nhidden)
        print("correct:       ", correct)
        print("incorrect:     ", incorrect)
        print("%.2f" %((correct/(correct+incorrect))*100),"percent correct")
        print(confusion_matrix)