# q2-viromics

A [QIIME 2](https://qiime2.org) Plugin for detecting viral genomes and assessing their quality.

## Installation
_q2-viromics_ is available as part of the QIIME 2 pathogenome distribution. For installation and usage instructions please consult the official [QIIME 2 documentation](https://docs.qiime2.org). 


## Usage
Start by downloading sample input [datasets](https://polybox.ethz.ch/index.php/s/9jlQ4oyDWvWyvpB).

Fetch the checkV database:
```bash
qiime viromics checkv-fetch-db --o-database checkV_db.qza --verbose
```

Run the CheckV analysis:
```bash
qiime viromics checkv-analysis --i-sequences genomad_output/viruses.qza --i-database checkV_db.qza --p-num-threads 4 --output-dir checkV_output --verbose
```
