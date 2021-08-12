---
title: Document Array Construct
---
# Document Array Construct

## Construct Document Array From Repeated Container

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.0086 | 0.0008 | {'num_chunks': 10000} |
| 2.0.18 | 5 | 0.0069 | 0.0001 | {'num_chunks': 10000} |
| 2.0.17 | 5 | 0.0092 | 0.0005 | {'num_chunks': 10000} |
## Construct Document Array From Another Documentarray

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.0028 | 0.0006 | {'num_docs': 10000} |
| 2.0.18 | 5 | 0.0026 | 0.0005 | {'num_docs': 10000} |
| 2.0.17 | 5 | 0.0036 | 0.0004 | {'num_docs': 10000} |
## Construct Document Array From List Of Documents

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.0051 | 0.0006 | {'num_docs': 10000} |
| 2.0.18 | 5 | 0.0046 | 0.0008 | {'num_docs': 10000} |
| 2.0.17 | 5 | 0.0053 | 0.0008 | {'num_docs': 10000} |
## Construct Document Array From Tuple Of Documents

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.0051 | 0.0006 | {'num_docs': 10000} |
| 2.0.18 | 5 | 0.0044 | 0.0008 | {'num_docs': 10000} |
| 2.0.17 | 5 | 0.0055 | 0.0004 | {'num_docs': 10000} |
## Construct Document Array From Generator

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.5651 | 0.0098 | {'num_docs': 10000} |
| 2.0.18 | 5 | 0.5592 | 0.0088 | {'num_docs': 10000} |
| 2.0.17 | 5 | 0.5658 | 0.0109 | {'num_docs': 10000} |
## Construct Document Array From Another Documentarray Memmap

| version | iterations | mean_time | std_time | metadata |
| :---: | :---: | :---: | :---: | :---: |
| 2.0.19 | 5 | 0.1151 | 0.0024 | {'num_docs': 10000} |
| 2.0.18 | 5 | 0.1143 | 0.0026 | {'num_docs': 10000} |
| 2.0.17 | 5 | 0.1179 | 0.0021 | {'num_docs': 10000} |
