---
title: Document Graph Construction
---
# Document Graph Construction

## Graph Add Edges Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 20613.8 | 139.7 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 45811 | 233.36 | -122.23% | 10000 | 20000 | 1000 |
## Graph Add Edges Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 257.6 | 5.73 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 259.4 | 3.29 | -0.7% | 10000 | 20000 | 1000 |
## Graph Add Single Edge Assuming All Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 6578.6 | 47.1 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 6383.4 | 82.74 | +2.97% | 10000 | 20000 | 1000 |
## Graph Add Single Edge Assuming No Nodes Present

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | N Edges | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 28243.2 | 137.88 | 0.0% | 10000 | 20000 | 5 |
| 2.0.21 | 57585.2 | 2169.4 | -103.89% | 10000 | 20000 | 1000 |
## Graph Add Single Node

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 20514.2 | 397.42 | 0.0% | 10000 | 5 |
| 2.0.21 | 42926.2 | 331.25 | -109.25% | 10000 | 1000 |
## Graph Add Nodes

| Version | Mean Time (ms) | Std Time (ms) | Delta w.r.t. 2.0.22.dev9 | N Nodes | Iterations |
| :---: | :---: | :---: | :---: | :---: | :---: |
| 2.0.22.dev9 | 37.6 | 0.89 | 0.0% | 10000 | 5 |
| 2.0.21 | 34 | N/A | +9.57% | 10000 | 1000 |
