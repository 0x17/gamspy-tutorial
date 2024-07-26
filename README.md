# Collection of GAMSPy models for SOAK PhD day tutorial

## What is this?

This repository contains multiple GAMSPy models which I plan to show partially explain step by step on Oct. 23rd 2024 during a 1.5h GAMSPy tutorial presented on the PhD day of the [SOAK](https://soaf.se/soak/) conference. This conference is organized by the [SOAF](https://soaf.se/) (Svenska Operationsanalysföreningen).

## Table of contents (model repository)

* 1. Introductionary examples
  * 1.1. `1_hellogams.py` - hello GAMSPy "minimize free variable x s.t. x==23"
  * 1.2. `2_simplemip.py` - bit less trivial MIP taken from Dr. Alireza Soroudi
  * 1.3. `3_trnsport.py` - GAMS favorite example model taken from Dantzig

* 2. Intermediate examples
  * 2.1. `1_knapsack.py` - rudimentary binary knapsack model
  * 2.2. `2_scheduling.py` - machine scheduling problem (one stage jobs, unrelated machines, minimize makespan) with Gantt chart (horizontal bars) visualization
  * 2.3. `3_tsp.py` - minimalistic TSP showing the effect of toggling subtour elimination constraints with visualization as directed graph

* 3. TSP for [Hittaut](https://koncept.orientering.se/provapaaktiviteter/hittaut/)
  * 3.1. `collect_data.py` - fetches required exogenous data for model
  * 3.2. `tsp-hittaut.py` - contains actual TSP model and map solution visualization

## Setup virtual environment

```
pip install virtualenv
virtualenv venv
# Windows
./venv/Scripts/activate
# Linux
source venv/bin/activate
pip install -r requirements.txt
```
