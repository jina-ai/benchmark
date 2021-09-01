---
title: Document Graph Construction
---
# Document Graph Construction

## Graph Add Edges Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 20.61K | 140.4 | 0.0% | 10.00K | 20.00K | 5 |
| 2.0.22.dev12 | 23.36K | 944.2 | -13.3% | 10.00K | 20.00K | 5 |
| 2.0.22.dev9 | 20.61K | 139.7 | 0.0% | 10.00K | 20.00K | 5 |
| 2.0.21 | 45.81K | 233.4 | -122.2% | 10.00K | 20.00K | 1.00K |
## Graph Add Edges Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 253.2 | 3.3 | 0.0% | 10.00K | 20.00K | 5 |
| 2.0.22.dev12 | 272 | 2.3 | -7.4% | 10.00K | 20.00K | 5 |
| 2.0.22.dev9 | 257.6 | 5.7 | -1.7% | 10.00K | 20.00K | 5 |
| 2.0.21 | 259.4 | 3.3 | -2.4% | 10.00K | 20.00K | 1.00K |
## Graph Add Single Edge Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 6.71K | 38.2 | 0.0% | 10.00K | 20.00K | 5 |
| 2.0.22.dev12 | 6.50K | 21.2 | +3.1% | 10.00K | 20.00K | 5 |
| 2.0.22.dev9 | 6.58K | 47.1 | +2.0% | 10.00K | 20.00K | 5 |
| 2.0.21 | 6.38K | 82.7 | +4.9% | 10.00K | 20.00K | 1.00K |
## Graph Add Single Edge Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 27.95K | 203.6 | 0.0% | 10.00K | 20.00K | 5 |
| 2.0.22.dev12 | 29.76K | 376.5 | -6.5% | 10.00K | 20.00K | 5 |
| 2.0.22.dev9 | 28.24K | 137.9 | -1.1% | 10.00K | 20.00K | 5 |
| 2.0.21 | 57.59K | 2.17K | -106.0% | 10.00K | 20.00K | 1.00K |
## Graph Add Single Node

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 20.45K | 426.0 | 0.0% | 10.00K | 5 |
| 2.0.22.dev12 | 21.15K | 865.6 | -3.4% | 10.00K | 5 |
| 2.0.22.dev9 | 20.51K | 397.4 | -0.3% | 10.00K | 5 |
| 2.0.21 | 42.93K | 331.3 | -109.9% | 10.00K | 1.00K |
## Graph Add Nodes

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22 | 38.2 | 0.8 | 0.0% | 10.00K | 5 |
| 2.0.22.dev12 | 38.4 | 0.9 | -0.5% | 10.00K | 5 |
| 2.0.22.dev9 | 37.6 | 0.9 | +1.6% | 10.00K | 5 |
| 2.0.21 | 34 | N/A | +11.0% | 10.00K | 1.00K |
