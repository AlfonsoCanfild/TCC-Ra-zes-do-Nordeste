from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

# Este módulo define handlers personalizados para lidar com diferentes tipos de exceções os quais
# podem ocorrer durante o processamento das requisições na API.
# Ele inclui handlers para exceções HTTP, erros de validação do Pydantic e erros genéricos não tratados.
# Cada handler retorna uma resposta JSON estruturada com informações sobre o erro, 
# incluindo um código de status, uma mensagem de erro, detalhes adicionais, um timestamp e o caminho da requisição.
# Módulo adicionado para atender a necessidade de tratamento de erros, exceções e as regras de negócios.

# Handler para exceções HTTP (404, 409, 401, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "ERRO",
            "message": exc.detail if isinstance(exc.detail, str) else str(exc.detail),
            "details": [],
            "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
            "path": str(request.url.path)
        }
    )


# Handler para erros de validação do Pydantic (422)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    erros = [
        {
            "campo": ".".join(str(loc) for loc in erro["loc"] if loc != "body"),
            "mensagem": erro["msg"]
        }
        for erro in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Erro de validação nos dados enviados",
            "details": erros,
            "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
            "path": str(request.url.path)
        }
    )


# Handler para qualquer erro não tratado (500)
async def generic_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Erro interno no servidor",
            "details": [],
            "timestamp": datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
            "path": str(request.url.path)
        }
    )