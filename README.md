# Comparison of binary search tree efficiency.

## Description

This module examines spped of finding 10000 words in an alphabet of nearly 250000 words using various approaches. Data structures compared: Python built-in list, binary search tree created by adding words in the alphabetical order from the dictionary, binary search tree created by adding words in a random order, and a balanced binary tree.

## Usage

To get efficiency report simply run module named linkedbst.py:
```python
python3 linkedbst.py
```

## Result

The module will be running for about 50 minutes due to long time of creating a binary search tree by adding words in an alphabetical order.

At the end you will see this messsage in the console:

```bash
Time to find in list: 10.90720001200134 sec.
Time to find in alpahbetic tree: 1.0115760925666715 min.
Time to find in random tree: 0.04462501600210089 sec.
Time to find in balanced tree: 0.03563430700160097 sec.
```