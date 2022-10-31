# Decoding a Neural Retriever's Latent Space for Query Suggestion

_Leonard Adolphs, Michelle Chen Huebscher, Christian Buck, Sertan Girgin, Olivier Bachem, Massimiliano Ciaramita, Thomas Hofmann_

# Traversal Data
You can download and decompress the traversal data together with the associated msmarco corpus by running the provided download script:
```
bash download.sh
```

To merge the traversal data with the paragraphs from the MSMarco dataset, we provide a merge script that you can run as
```
python merge_data.py
```

The merged jsonl data has the following structure
```
[
    {"original": {
        "query": "the original query",
        "documents": [{
            "doc_id": "123",
            "score": 99, # the retrieval score
            "content": {"text": "The paragraph's text"}
            }, {...}, ... ]
    }, "variants": [ 
         # the list of reformulations with their search results
        {"query": "the first reformulated query",
        "documents": [{
            "doc_id": "124",
            "score": 100, # the retrieval score
            "content": {"text": "Another paragraph's text"}
            }, ... ]}, {...}, ...
        ]
    }, {...}, ...
]
```
