import argparse
import os

from numpy import save

from .binary_tree import BinaryTree
from .graph import Graph
from .random_walker import RandomWalker
from .skipgram import SkipGram


def main(config):
    graph = Graph(config)

    # Binary tree for applying hierarchical softmax.
    binary_tree = BinaryTree(
        num_nodes_in_graphs=len(graph.nodes),
        num_dimensions=config.n_dims,
    )

    walker = RandomWalker(graph)
    walker.process(
        walks_per_node=config.walks_per_node,
        steps_per_walk=config.steps_per_walk,
    )

    skipgram = SkipGram(
        binary_tree=binary_tree,
        random_walks=walker.traces,
        window_size=config.skipgram_window_size,
        config=config,
    )
    skipgram.train()

    embeddings = binary_tree.get_node_embeddings()
    save(os.path.join(config.output_dir), embeddings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="DeepWalk"
    )
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--walks_per_node", type=int, default=5)
    parser.add_argument("--steps_per_walk", type=int, default=10)
    parser.add_argument("--n_dims", type=int, default=16)
    parser.add_argument("--skipgram_window_size", type=int, default=2)
    parser.add_argument("--lr", type=float, default=0.025)
    directionality = parser.add_mutually_exclusive_group()
    directionality.add_argument("--undirected", action="store_true")
    directionality.add_argument("--directed", action="store_true")
    parser.add_argument('--gpu', type=str, default=None)
    config = parser.parse_args()
    main(config)
