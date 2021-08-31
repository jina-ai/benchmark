---
title: Document Graph Construction
---
# Document Graph Construction

## Graph Add Edges Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 23359.8 | 944.25 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 45811 | 233.36 | -96.11% | 10000 | 20000 | 1000 |
## Graph Add Edges Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 272 | 2.35 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 259.4 | 3.29 | +4.63% | 10000 | 20000 | 1000 |
## Graph Add Single Edge Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 6500.2 | 21.17 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 6383.4 | 82.74 | +1.8% | 10000 | 20000 | 1000 |
## Graph Add Single Edge Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 29763.6 | 376.5 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 57585.2 | 2169.4 | -93.48% | 10000 | 20000 | 1000 |
## Graph Add Single Node

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 21146.4 | 865.56 | 0.0% | 10000 | 5 |
| 2.0.21 | 42926.2 | 331.25 | -103.0% | 10000 | 1000 |
## Graph Add Nodes

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev12 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev12 | 38.4 | 0.89 | 0.0% | 10000 | 5 |
| 2.0.21 | 34 | N/A | +11.46% | 10000 | 1000 |
