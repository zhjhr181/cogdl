import random
import numpy as np

import torch

from utils import print_result, set_random_seed, get_dataset, get_extra_args
from cogdl.tasks import build_task
from cogdl.datasets import build_dataset
from cogdl.utils import build_args_from_dict

DATASET_REGISTRY = {}


def build_default_args_for_graph_classification(dataset):
    cpu = not torch.cuda.is_available()
    args = {
        "lr": 0.001,
        "weight_decay": 5e-4,
        "max_epoch": 500,
        "patience": 100,
        "cpu": cpu,
        "device_id": [0],
        "seed": [0],
        "hidden_size": 64,
        "degree_feature": False,
        "gamma": 0.5,
        "kfold": False,
        "uniform_feature": False,
        "train_ratio": 0.7,
        "test_ratio": 0.1,
        "num_layers": 3,
        "dropout": 0.5,
        "batch_size": 128,
        "kernel_size": 5,
        "k": 30,
        "out_channels": 32,
        "task": "graph_classification",
        "model": "sortpool",
        "dataset": dataset,
    }
    args = get_extra_args(args)
    return build_args_from_dict(args)


def register_func(name):
    def register_func_name(func):
        DATASET_REGISTRY[name] = func
        return func

    return register_func_name


@register_func("mutag")
def mutag_config(args):
    return args


@register_func("imdb-b")
def imdb_b_config(args):
    args.degree_feature = True
    return args


@register_func("imdb-m")
def imdb_m_config(args):
    args.degree_feature = True
    return args


@register_func("proteins")
def proteins_config(args):
    return args


@register_func("collab")
def collab_config(args):
    args.degree_feature = True
    return args


def run(dataset_name):
    args = build_default_args_for_graph_classification(dataset_name)
    args = DATASET_REGISTRY[dataset_name](args)
    dataset, args = get_dataset(args)
    results = []
    for seed in args.seed:
        set_random_seed(seed)
        task = build_task(args, dataset=dataset)
        result = task.train()
        results.append(result)
    return results


if __name__ == "__main__":
    datasets = ["mutag", "imdb-b", "imdb-m", "proteins", "collab"]
    results = []
    for x in datasets:
        results += run(x)
    print_result(results, datasets, "sortpool")
