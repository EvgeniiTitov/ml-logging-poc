from ml_logging import ExistingRun


# TODO: Think if using Go's approach to handling errors is a good idea.
#       Doesnt seem like it?


def main() -> int:
    ml_run = ExistingRun("dd14e13a-459b-4a68-8c6d-4414cc5069a8")
    images = ml_run.list_images()
    print("Images:", images)

    assets = ml_run.list_assets()
    print("Assets:", assets)

    ok, err = ml_run.get_asset("iris_model.pkl", "/Users/1213669/Downloads")
    if ok:
        print("Downloaded the model")
    else:
        print(err)

    ok, err = ml_run.get_image("retrowave.jpeg", "/Users/1213669/Downloads")
    if ok:
        print("Downloaded the image")
    else:
        print(err)

    return 0


if __name__ == "__main__":
    main()
