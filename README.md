# q2-viromics

A [QIIME 2](https://qiime2.org) Plugin for assessing the quality and completeness of metagenome-assembled viral genomes.

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

After this completes, activate the new environment you created by running:

```shell
conda activate q2-viromics
```

```shell
make install
```

```shell
make dev
qiime dev refresh-cache
```
