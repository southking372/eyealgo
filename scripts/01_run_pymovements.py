import pymovements as pm


def main():
    dataset = pm.Dataset(
        "ToyDataset",
        path="data/raw_public/ToyDataset",
    )

    print("downloading dataset ...")
    dataset.download()

    print("loading dataset ...")
    dataset.load()

    print("running pix2deg ...")
    dataset.pix2deg()

    print("running pos2vel ...")
    dataset.pos2vel()

    print("detecting ivt fixations ...")
    dataset.detect_events("ivt")

    print("detecting microsaccades ...")
    dataset.detect_events("microsaccades", minimum_duration=8)

    print("\n=== pipeline finished ===")
    print(dataset)

    if len(dataset.gaze) > 0:
        print("\n=== first gaze frame head ===")
        print(dataset.gaze[0].frame.head())

    if len(dataset.events) > 0:
        print("\n=== first event frame head ===")
        print(dataset.events[0].frame.head())


if __name__ == "__main__":
    main()
