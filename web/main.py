"""
DockDoctor Web - FastAPI 後端
"""

import sys
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

sys.path.insert(0, str(Path(__file__).parent.parent))

from analyzers.compose_analyzer import analyze_compose
from analyzers.port_checker import check_ports
from analyzers.docker_remote import check_containers_remote, analyze_logs_remote

app = FastAPI(title="DockDoctor Web")

static_dir = Path(__file__).parent / "static"


@app.get("/", response_class=HTMLResponse)
def index():
    return (static_dir / "index.html").read_text(encoding="utf-8")


app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.post("/api/scan")
async def scan(
    compose_file: UploadFile = File(...),
    docker_host: str = Form(...),
    project_name: str = Form(""),
):
    if not compose_file.filename.endswith((".yml", ".yaml")):
        raise HTTPException(status_code=400, detail="請上傳 .yml 或 .yaml 檔案")

    content = await compose_file.read()

    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        compose_result = analyze_compose(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)

    ports_result = check_ports(compose_result)

    proj = project_name.strip() or None
    containers_result = check_containers_remote(docker_host, proj)
    logs_result = analyze_logs_remote(docker_host, proj)

    return {
        "compose": compose_result,
        "ports": ports_result,
        "containers": containers_result,
        "logs": logs_result,
    }
