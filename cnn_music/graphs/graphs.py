import matplotlib.pyplot as plt
import pickle
import argparse, sys
import json
from keras.callbacks.callbacks import History
from typing import Dict, Union, List

def plot_graph(history: History, graph_desc: Dict[str, Union[str, List[str]]]):
    """
    :param history: Model history 
    :param graph_desc: Dict with graph description 
    """
    print('HISTORY')
    print(str(history))
    plt.plot(history.history[graph_desc['name']])
    plt.plot(history.history['val_' + graph_desc['name']])
    plt.title(graph_desc['title'])
    plt.ylabel(graph_desc['ylabel'])
    plt.xlabel(graph_desc['xlabel'])
    plt.legend(graph_desc['legend'], loc = graph_desc['legend_location'])
    plt.savefig(graph_desc['path'])
    plt.close()

if __name__ == "__main__":
    input_parser = argparse.ArgumentParser('Prints charts')
    input_parser.add_argument('-c','--config',
            metavar='config.json',
            type=str,
            help='path to config json; configs/charts/config.json assumed if not specifyed'
        )
    input_parser.add_argument('-m','--model',
            metavar='models/model',
            type=str,
            help='path to model; models/model assumed if not specifyed'
        )
    args = input_parser.parse_args()
    configpath = args.config if args.config else 'configs/charts/config.json'
    modelpath = args.model if args.model else 'models/model'

    train_output_file = open(modelpath,'rb')
    train_output = pickle.load(train_output_file)
    graphs_desc = json.load(open(configpath))['graphs'];
    for g in graphs_desc:
        plot_graph(train_output['history'], g)
