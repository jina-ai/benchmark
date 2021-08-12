---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.3311 | 0.0015 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.18 | 5 | 0.3177 | 0.0012 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.17 | 5 | 0.3348 | 0.0014 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.16 | 5 | 0.3349 | 0.0018 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.15 | 5 | 0.338 | 0.0017 | {'num_docs_append': 100000, 'file_format': 'binary'} |
## Document Array Load

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.1853 | 0.0022 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.18 | 5 | 0.1821 | 0.0007 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.17 | 5 | 0.1871 | 0.0014 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.16 | 5 | 0.1884 | 0.0016 | {'num_docs_append': 100000, 'file_format': 'binary'} |
| 2.0.15 | 5 | 0.1974 | 0.0022 | {'num_docs_append': 100000, 'file_format': 'binary'} |
