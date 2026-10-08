from fastapi import FastAPI, File, UploadFile, HTTPException
import pandas as pd
from io import BytesIO

from app.agent.agent import build_agent
from app.tools.data_profiler import profile_dataframe
from api.schemas import AnalyzeRequest


app = FastAPI(
    title="DataMind AI API",
    description="API REST para análise inteligente de dados",
    version="1.0.0",
)


@app.get("/api/v1/health")
def health_check():

    return {
        "status": "online",
        "service": "DataMind AI API",
        "version": "1.0.0",
    }


@app.post("/api/v1/analyze")
def analyze(request: AnalyzeRequest):

    try:

        if not hasattr(app.state, "dataframe"):
            raise HTTPException(
                status_code=400,
                detail="Nenhum arquivo foi carregado.",
            )

        dataframe = app.state.dataframe
        profile = profile_dataframe(dataframe)

        agent = build_agent()

        result = agent.invoke(
            {
                "question": request.question,
                "dataframe": dataframe,
                "file_name": app.state.file_name,
                "profile": profile,
                "messages": [],
            }
        )

        return {
            "question": request.question,
            "tool": result.get("tool"),
            "response": result.get(
                "response",
                "Não foi possível gerar uma resposta.",
            ),
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@app.post("/api/v1/upload")
async def upload_file(file: UploadFile = File(...)):

    allowed_extensions = {
        ".csv",
        ".xlsx",
        ".xls",
        ".parquet",
    }

    filename = file.filename or ""

    extension = filename.lower().rsplit(".", 1)[-1]

    if f".{extension}" not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Formato não suportado. "
                "Use CSV, XLSX, XLS ou Parquet."
            ),
        )

    try:

        contents = await file.read()

        if extension == "csv":

            dataframe = pd.read_csv(
                BytesIO(contents)
            )

        elif extension in {"xlsx", "xls"}:

            dataframe = pd.read_excel(
                BytesIO(contents)
            )

        elif extension == "parquet":

            dataframe = pd.read_parquet(
                BytesIO(contents)
            )

        app.state.dataframe = dataframe
        app.state.file_name = filename

        return {
            "message": "Arquivo carregado com sucesso.",
            "file_name": filename,
            "rows": int(dataframe.shape[0]),
            "columns": int(dataframe.shape[1]),
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar arquivo: {exc}",
        )
