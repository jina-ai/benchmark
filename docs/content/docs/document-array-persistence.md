---
title: Document Array Persistence
---
# Document Array Persistence

## Document Array Save

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.21.dev38 | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.21.dev38 | 318.4 | 1.52 | 0.0% | 100000 | binary | 5 |
| 2.0.21.dev36 | 330.6 | 0.89 | -3.83% | 100000 | binary | 5 |
| 2.0.21.dev35 | 331 | 1.87 | -3.96% | 100000 | binary | 5 |
| 2.0.21.dev34 | 311 | 0.71 | +2.32% | 100000 | binary | 5 |
| 2.0.21.dev33 | 332.2 | 1.3 | -4.33% | 100000 | binary | 5 |
| 2.0.21.dev30 | 324.2 | 1.92 | -1.82% | 100000 | binary | 5 |
| 2.0.20 | 333.6 | 1.14 | -4.77% | 100000 | binary | 5 |
| 2.0.19 | 314.31 | 1.87 | +1.29% | 100000 | binary | 5 |
| 2.0.18 | 317.75 | 1.17 | +0.2% | 100000 | binary | 5 |
| 2.0.17 | 321.4 | 2.07 | -0.94% | 100000 | binary | 5 |
| 2.0.16 | 336.83 | 1.67 | -5.79% | 100000 | binary | 5 |
| 2.0.15 | 338.0 | 1.66 | -6.15% | 100000 | binary | 5 |
| 2.0.14 | 316.2 | 2.17 | +0.69% | 100000 | binary | 5 |
| 2.0.13 | 451.2 | 0.84 | -41.71% | 100000 | binary | 5 |
| 2.0.12 | 428 | 2.0 | -34.42% | 100000 | binary | 5 |
## Document Array Load

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.21.dev38 | Num Docs Append | File Format | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.21.dev38 | 177.4 | 0.55 | 0.0% | 100000 | binary | 5 |
| 2.0.21.dev36 | 183.6 | 2.3 | -3.49% | 100000 | binary | 5 |
| 2.0.21.dev35 | 184.6 | 0.55 | -4.06% | 100000 | binary | 5 |
| 2.0.21.dev34 | 175 | 1.22 | +1.35% | 100000 | binary | 5 |
| 2.0.21.dev33 | 184.2 | 1.64 | -3.83% | 100000 | binary | 5 |
| 2.0.21.dev30 | 190.4 | 1.14 | -7.33% | 100000 | binary | 5 |
| 2.0.20 | 183 | 0.71 | -3.16% | 100000 | binary | 5 |
| 2.0.19 | 179.93 | 1.14 | -1.43% | 100000 | binary | 5 |
| 2.0.18 | 182.07 | 0.7 | -2.63% | 100000 | binary | 5 |
| 2.0.17 | 176.8 | 1.3 | +0.34% | 100000 | binary | 5 |
| 2.0.16 | 184.67 | 1.29 | -4.1% | 100000 | binary | 5 |
| 2.0.15 | 197.36 | 2.15 | -11.25% | 100000 | binary | 5 |
| 2.0.14 | 120.2 | 1.1 | +32.24% | 100000 | binary | 5 |
| 2.0.13 | 154.8 | 1.64 | +12.74% | 100000 | binary | 5 |
| 2.0.12 | 150.6 | 1.14 | +15.11% | 100000 | binary | 5 |