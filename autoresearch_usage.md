# Autoresearch Usage

## One-Time Setup

```bash
pip install modal
modal setup    # opens browser to authenticate, stores token in ~/.modal/
```

## Test the Setup

```bash
cd /path/to/autoresearch
modal run launch.py   # provisions H100, prepares data, runs baseline training
```

First run is slower (~2-3 min extra) — Modal builds the Docker image and `prepare.py` downloads/tokenizes the data. Subsequent runs use cached image + volume.

## Run Experiments

From the `dot_claude` project, invoke:

```
/autoresearch
```

Or with a custom repo path:

```
/autoresearch /path/to/autoresearch
```

The agent will ask for run parameters (budget cap, max experiments, convergence patience, metric, research direction) then loop autonomously until a stop condition is hit.
