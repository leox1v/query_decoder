#!/bin/bash

mkdir data
# Download and decompress the traversal data without the provided embeddings.
wget -O data/msmarco_traversal.zip https://polybox.ethz.ch/index.php/s/DNUTQfe4mrB0UDf/download
unzip data/msmarco_traversal.zip -d data
rm data/msmarco_traversal.zip
xz -d -v data/GTR_base_no_embeddings/*.xz

# Download and decompress the msmarco data.
wget -O data/msmarco.zip https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/msmarco.zip
unzip data/msmarco.zip -d data
rm data/msmarco.zip