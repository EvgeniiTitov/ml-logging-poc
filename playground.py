import logging

from ml_logging import GCSBackend
from ml_logging.messages import *



logging.basicConfig(level=logging.INFO)


def main():
    # backend = GCSBackend(run_folder_name="run_789")
    # # backend.upload_asset("/Users/1213669/Coding/WooliesX/Chapter/ml-logging-poc/requirements.txt",
    # #                      "new_name2.txt")
    # backend.upload_image("/Users/1213669/Downloads/20211115_132529.jpg", "ugly_me")
    # # backend.upload_hyper_parameter("Learning rate", 0.005)
    # # backend.upload_hyper_parameter("Batch size", 64)
    # # backend.upload_hyper_parameter("Epochs", 1000)
    # #
    # # assets_list = backend.list_assets()
    # # print("ASSET LIST:", assets_list)
    # #
    # # images_list = backend.list_images()
    # # print("IMAGE LIST:", images_list)
    #
    # backend.download_asset("new_name.txt", "/Users/1213669/Downloads/KEK2.txt")
    # backend.download_image("ugly_me", "/Users/1213669/Downloads")
    # print("\nDone")
    get = GetMessage()
    get.set_text("Some text")
    get.set_kernel("KEK kernel")

    print(get)

if __name__ == '__main__':
    main()
