import modal
import subprocess
import sys

app = modal.App("autoresearch")

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install("torch==2.9.1", index_url="https://download.pytorch.org/whl/cu128")
    .pip_install("kernels>=0.11.7", "numpy>=2.2.6", "pyarrow>=21.0.0", "requests>=2.32.0", "rustbpe>=0.1.0", "tiktoken>=0.11.0")
)

vol = modal.Volume.from_name("autoresearch-cache", create_if_missing=True)

@app.function(
    image=image,
    gpu="H100",
    timeout=600,
    mounts=[modal.Mount.from_local_dir(".", remote_path="/root/autoresearch")],
    volumes={"/root/.cache/autoresearch": vol},
)
def train():
    import os
    os.chdir("/root/autoresearch")
    # Prepare data on first run (cached in volume for subsequent runs)
    if not os.path.exists("/root/.cache/autoresearch/fineweb10B"):
        subprocess.run([sys.executable, "prepare.py"], check=True)
        vol.commit()
    result = subprocess.run([sys.executable, "train.py"], timeout=540)
    sys.exit(result.returncode)

@app.local_entrypoint()
def main():
    train.remote()
