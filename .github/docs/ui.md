# Benchmark UI

To imitate the [Benchmark UI Example](https://docs.google.com/spreadsheets/d/1-HM5miV5iIPb-ZsLud_e1lmrPgjEevtEyCiYGRwbGKs/edit?usp=sharing) in our website, we need to write the results in a `JSON` file in `docs/static/artifacts` directory. The `JSON` filename should be `$JINA_VERSION.json` e.g. `2.10.0.json`. The content might be as follows:

```json
{
   "Document":{
      "__init__()":100,
      "__getter__()":200
   },
   "DocumentArray":{
      "__init__()":100,
      "__getter__()":200
   },
   "DocumentArrayMemMap":{
      "__init__()":100,
      "__getter__()":200
   }
}
```

The left menubar of the website would look like that:

- [Document](#)
    - [__init__()](#)
    - [__getter__()](#)
- [DocumentArray](#)
    - [__init__()](#)
    - [__getter__()](#)
- [DocumentArrayMemMap](#)
    - [__init__()](#)
    - [__getter__()](#)