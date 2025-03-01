from pathlib import Path
import tempfile

from fastapi.responses import FileResponse

try:
    import nbconvert  # type: ignore
except Exception:
    nbconvert = None

from jupyverse import JAPIRouter


def init(jupyverse):
    router.init(jupyverse)
    return router


class NbconvertRouter(JAPIRouter):
    def init(self, jupyverse):
        self.jupyverse = jupyverse
        self.jupyverse.app.include_router(router)


router = NbconvertRouter()


@router.get("/api/nbconvert")
async def get_nbconvert_formats():
    if nbconvert is None:
        return {}
    return {
        name: {
            "output_mimetype": nbconvert.exporters.get_exporter(name).output_mimetype
        }
        for name in nbconvert.exporters.get_export_names()
    }


@router.get("/nbconvert/{format}/{path}")
async def get_nbconvert_document(format: str, path: str, download: bool):
    exporter = nbconvert.exporters.get_exporter(format)
    if download:
        media_type = "application/octet-stream"
    else:
        media_type = exporter.output_mimetype
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_path = tmp_dir / (Path(path).stem + exporter().file_extension)
    with open(tmp_path, "wt") as f:
        f.write(exporter().from_filename(path)[0])
    return FileResponse(tmp_path, media_type=media_type, filename=tmp_path.name)
