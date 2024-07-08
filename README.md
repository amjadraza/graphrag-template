<h1 align="center">
A Template Project for Graphrag
</h1>

This is a template project to get us started with [graphrag](https://github.com/microsoft/graphrag/tree/main)

[GraphRag Official Documentation](https://microsoft.github.io/graphrag/)

## 🔧 Features
- A template with `poetry` environment
- A test data (raw + processed)
- Jupyter Lab Notebooks
- A simple Streamlit app
- Using the pre-defined / prepared data

## 💻 Running Locally

1. Clone the repository📂

```bash
git clone https://github.com/amjadraza/graphrag-template.git
```

2. Install dependencies with [Poetry](https://python-poetry.org/) and activate virtual environment🔨

```bash
poetry install
poetry shell
```

3. Configure Environment Variables

given `.env.example`, rename to `.env` and replace the desired key with your OpenAI Key and Model

```bash

jupyter lab
```

4. Run the Jupyter Lab server🚀

```bash

jupyter lab
```
Explore the sampled notebooks with sample data

4. Run the Python Scripts

```bash

python src/global_search.py

or 

python src/local_search.py
```

5. Run the Streamlit server🚀

```bash

streamlit run --server.runOnSave=true  src/app.py
```

## Configure Indexing

`python -m graphrag.index --init --root ./ragtest`

## Credits / Resources

1. [Official Documentation](https://microsoft.github.io/graphrag/)
2. [GitHub Project](https://github.com/microsoft/graphrag)
3. [Release Blogpost](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)
4. [Video by Mervin Praison](https://www.youtube.com/watch?v=zDv8akdf6v4)
5. [Video by PrompmtEngineer](https://www.youtube.com/watch?v=vX3A96_F3FU)
