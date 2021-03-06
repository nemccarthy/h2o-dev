import sys
sys.path.insert(1, "../../../")
import h2o

def benign(ip,port):
    # Connect to h2o
    h2o.init(ip,port)

    training_data = h2o.import_frame(h2o.locate("smalldata/logreg/benign.csv"))

    Y = 3
    X = [x for x in range(2,11) if x != Y]

    #Log.info("Build the model")
    model = h2o.glm(y=training_data[Y].asfactor(), x=training_data[X], family="binomial", n_folds=0, alpha=[0], Lambda=[1e-5])
    #model = h2o.glm(y=training_data[Y].asfactor(), x=training_data[X], family="binomial", n_folds=5, alpha=[0], Lambda=[1e-5])

    #Log.info("Check that the columns used in the model are the ones we passed in.")
    #Log.info("===================Columns passed in: ================")
    in_names = [training_data.names()[i] for i in X]
    #Log.info("===================Columns passed out: ================")
    out_names = [model._model_json['output']['coefficients_table'].cell_values[c][0] for c in range(len(X))]
    assert in_names == out_names

if __name__ == "__main__":
  h2o.run_test(sys.argv, benign)

