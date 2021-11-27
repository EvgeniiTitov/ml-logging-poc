import pickle

from sklearn import datasets, model_selection, ensemble

from ml_logging import NewRun


def main() -> int:
    ml_run = NewRun(auto_logging=True)
    run_id = ml_run.run_id
    print("ML run id:", run_id)

    data = datasets.load_iris()
    print("Data loaded")

    (
        train_data,
        test_data,
        train_lagels,
        test_labels,
    ) = model_selection.train_test_split(
        data.data, data.target, train_size=0.80
    )
    print("Dataset split into train and test")
    ml_run.log_hyper_param("TrainSplitRatio", 0.80)

    model = ensemble.RandomForestClassifier(n_estimators=500)
    ml_run.log_hyper_param("RFC N estimators", 500)

    model.fit(train_data, train_lagels)
    print("Model trained")

    result = model.score(test_data, test_labels)
    print("Training results:", result)

    model_save_path = "iris_model.pkl"
    pickle.dump(model, open(model_save_path, "wb"))
    print("Model saved locally")
    ml_run.log_asset(model_save_path)

    ml_run.log_image("retrowave.jpeg")
    print("Image logged")

    # TODO: Explicit vs implicit stop?
    ml_run.complete_experiment()

    return 0


if __name__ == "__main__":
    main()
