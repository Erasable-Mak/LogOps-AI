import typer, json
from core.ingest import read_jsonl
from app.deps import get_pipeline
import dotenv
dotenv.load_dotenv()

app = typer.Typer(add_completion=False)

@app.command()
def train_if():
    stats = get_pipeline().train_iforest()
    typer.echo(json.dumps(stats, indent=2))

@app.command()
def detect(file: str):
    records = list(read_jsonl(file))
    out = get_pipeline().detect(records)
    typer.echo(json.dumps(out, indent=2))

if __name__ == "__main__":
    app()
