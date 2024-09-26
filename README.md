# q2-viromics

A [QIIME 2](https://qiime2.org) Plugin for detecting viral genomes and assessing their quality.

###  Install development version of `q2-viromics`
Clone the repository:
```shell
git clone https://github.com/bokulich-lab/q2-viromics.git
cd q2-viromics
```

Then, run:

```shell
mamba create -n q2-viromics -c conda-forge -c bioconda -c https://packages.qiime2.org/qiime2/2024.10/metagenome/passed/ -c defaults q2cli q2-types checkv genomad pyhmmer
```

###  Activate q2-viromics environment
```shell
conda activate q2-viromics
```



### Test it out!
#### Download sample input [datasets](https://polybox.ethz.ch/index.php/s/9jlQ4oyDWvWyvpB)

Fetch the geNomad database.
```bash
qiime viromics genomad-fetch-db --o-database genomad_db.qza --verbose
```

Run the geNomad analysis.
```bash
qiime viromics genomad-analysis --i-sequences input_sequences.qza --i-database genomad_db.qza --p-num-threads 8 --p-splits 8 --output-dir genomad_output --verbose
```

Fetch the checkV database.
```bash
qiime viromics checkv-fetch-db --o-database checkV_db.qza --verbose
```

Run the CheckV analysis.
```bash
qiime viromics checkv-analysis --i-sequences genomad_output/viruses.qza --i-database checkV_db.qza --p-num-threads 4 --output-dir checkV_output --verbose
```
