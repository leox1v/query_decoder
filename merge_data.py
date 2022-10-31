#!/usr/bin/env python
"""Script to merge the traversal data with the msmarco corpus."""
from absl import app, flags, logging
import json
import os
from typing import Dict
from tqdm import tqdm

FLAGS = flags.FLAGS

flags.DEFINE_string(
    "traversal_data_dir",
    "data/GTR_base_no_embeddings",
    "The directory with the traversal data. If you run the download.sh script as described in the README, it is either "
    "GTR_base_no_embeddings or GTR_base_with_embeddings.",
)
flags.DEFINE_string(
    "corpus_file", "data/msmarco/corpus.jsonl", "The jsonl file of the msmarco corpus."
)
flags.DEFINE_string(
    "merged_data_file", "data/merged_data.jsonl", "The output path for the merged data."
)
flags.DEFINE_integer(
    "num_examples",
    -1,
    "The number of traversal examples to load and merge. If <= 0, load all of them.",
)


def traversal_data_iterator(base_dir: str):
    assert os.path.isdir(
        base_dir
    ), f'"{base_dir}" not found. Did you forget to run "bash download.sh"?'
    fnames = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if ".json" in f]
    for fname in fnames:
        with open(fname, "r") as f:
            for line in f.readlines():
                ex = json.loads(line)
                yield ex


def update_traversal_example_with_paragraph_content(ex: Dict, corpus: Dict):
    for doc in ex["original"]["documents"]:
        doc["content"] = corpus.get(doc["doc_id"], "")
    for v in ex["variants"]:
        for doc in v["documents"]:
            doc["content"] = corpus.get(doc["doc_id"], "")
    return ex


def load_msmarco_corpus(corpus_file: str):
    assert os.path.isfile(
        corpus_file
    ), f'"{corpus_file}" not found. Did you forget to run "bash download.sh"?'
    corpus = {}
    with open(corpus_file, "r") as f:
        for line in tqdm(f.readlines(), "Load MSMarco corpus"):
            ex = json.loads(line)
            corpus[ex["_id"]] = ex
    return corpus


def main(argv):
    # Load the corpus from MSMarco.
    corpus = load_msmarco_corpus(FLAGS.corpus_file)

    # Get the traversal data iterator.
    data_iter = traversal_data_iterator(FLAGS.traversal_data_dir)

    # Go through the data and add the paragraph contents.
    data = []
    for i, ex in tqdm(
        enumerate(data_iter),
        desc="Merge traversal data and msmarco paragraphs",
        total=FLAGS.num_examples if FLAGS.num_examples > 0 else None,
    ):
        ex = update_traversal_example_with_paragraph_content(ex, corpus)
        data.append(ex)
        if 0 < FLAGS.num_examples <= i:
            break

    # Save the data.
    with open(FLAGS.merged_data_file, "w") as f:
        f.write(json.dumps(data))
    logging.info(f"Saved merged data to {FLAGS.merged_data_file}.")


if __name__ == "__main__":
    app.run(main)
