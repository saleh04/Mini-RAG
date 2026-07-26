# Mini RAG APP
This repository contains my implementation of the RAG course by Abu Bakr Soliman, focusing on writing production-ready code rather than relying on Jupyter notebooks.

You can find the course playlist [here](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)

## Requirements
- Python 3.8 or later

### Install Python using MiniConda
1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/concepts/anaconda-or-miniconda#quick-command-line-install)
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python=3.8
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```
## Installation

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Setup the environment variables
```bash
$ cp .env.example .env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

