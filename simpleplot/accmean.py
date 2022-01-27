import argparse
import json
import matplotlib.pyplot as plt

if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("json_file")
    args = a.parse_args()
    
    with open(args.json_file, "r") as fh:
        data = json.load(fh)

    fig, ax = plt.subplots()
    ax.plot(data['val_acc_mean'], color='b', label='val')
    ax.plot(data['acc_mean'], color='r', label='train')
    ax.set_ylim([70, 100])
    ax.set_xlabel('epoch')
    ax.legend(loc='best')
    plt.savefig('{}.png'.format(args.json_file))
    for i in zip(data['acc_mean'], data['val_acc_mean']):
        print(i)
