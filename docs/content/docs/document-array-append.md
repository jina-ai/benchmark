---
title: Document Array Append
---
# Document Array Append

## Docarray Append

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.0079 | 0.0013 | {'num_docs_append': 10000} |
| 2.0.18 | 5 | 0.0068 | 0.0009 | {'num_docs_append': 10000} |
| 2.0.17 | 5 | 0.0083 | 0.0003 | {'num_docs_append': 10000} |
## Document Array Memmap Append

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.1097 | 0.0058 | {'num_docs_append': 10000, 'flush': False} |
| 2.0.18 | 5 | 0.1011 | 0.0014 | {'num_docs_append': 10000, 'flush': False} |
| 2.0.17 | 5 | 0.1036 | 0.0005 | {'num_docs_append': 10000, 'flush': False} |
