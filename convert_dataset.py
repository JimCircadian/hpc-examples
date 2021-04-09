import argparse
import glob
import logging
import os
import re
import sys

from concurrent.futures import ProcessPoolExecutor

import numpy as np
import tensorflow as tf

##python convert_dataset.py -s 5 /users/jambyr/hpc/icenet.testing/results/icenet2_linear_trend_input_6runs_absrad/cache output

def get_args():
    a = argparse.ArgumentParser()
    a.add_argument("-s", "--batch-size", type=int, default=5)
    a.add_argument("-v", "--verbose", default=False, action="store_true")
    a.add_argument("-w", "--workers", type=int, default=4)
    a.add_argument("input", help="Input directory")
    a.add_argument("output", help="Output directory")
    return a.parse_args()


def convert_batch(tf_path, data):
    logging.info("{} with {} samples".format(tf_path, data[0].shape[0]))

    with tf.io.TFRecordWriter(tf_path) as writer:
        logging.info("Processing batch file {}".format(tf_path))

        for i in range(data[0].shape[0]):
            logging.info("Processing input {}/{}".format(i, data[0].shape[0]))

            (x, y) = (data[0][i,...], data[1][i, ...])

            logging.debug("x shape {}, y shape {}".format(x.shape, y.shape))

            record_data = tf.train.Example(features=tf.train.Features(feature={
                "x": tf.train.Feature(float_list=tf.train.FloatList(value=x.reshape(-1))),
                "y": tf.train.Feature(float_list=tf.train.FloatList(value=y.reshape(-1))),
            })).SerializeToString()

            writer.write(record_data)


# TODO: Generic globbing of input data?
def convert_data(x_data, y_data, output_dir, workers=4, batch_size=1, wildcard="*"):
    x_data = np.load(x_data)
    y_data = np.load(y_data)

    options = tf.io.TFRecordOptions()
    batch_number = 0

    os.makedirs(output_dir)

    def batch(x, y, num):
        i = 0
        while i < x.shape[0]:
            yield x[i:i+num], y[i:i+num]
            i += num

    tasks = []

    for data in batch(x_data, y_data, batch_size):
        tf_path = os.path.join(output_dir, "{:05}.tfrecord".format(batch_number))

        tasks.append((tf_path, data))
        batch_number += 1

    with ProcessPoolExecutor(max_workers=workers) as executor:
        for args in tasks:
            executor.submit(convert_batch, *args)


if __name__ == "__main__":
    args = get_args()
    log_state = logging.DEBUG if args.verbose else logging.INFO
    logging.getLogger().setLevel(log_state)

    if not os.path.exists(args.input):
        raise RuntimeError("Input directory {} does not exist".format(args.input))
    if os.path.exists(args.output):
        raise RuntimeError("Output directory {} already exists".format(args.output))

    # TODO: Would be more generic to just pick up a train/test/val named file
    for data in [("X_train_all", "y_train_all"), ("X_val_all", "y_val_all"), ("X_test_all", "y_test_all")]:
        x_data = os.path.join(args.input, "{}.npy".format(data[0]))
        y_data = os.path.join(args.input, "{}.npy".format(data[1]))

        if not os.path.exists(x_data) or not os.path.exists(y_data):
            logging.warning("Skipping {}, one does not exist.".format(data))
            continue 

        set_type = re.search(r"(train|test|val)", data[0], re.IGNORECASE).group(1)
        output_path = os.path.join(args.output, set_type)
        convert_data(x_data, y_data, output_path, workers=args.workers, batch_size=args.batch_size)

