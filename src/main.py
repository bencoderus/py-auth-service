from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.auth.router import auth_router
from src.user.router import user_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_messages = [f"{err['loc'][-1]}: {err['msg']}" for err in errors]
    return JSONResponse(
        status_code=422,
        content={"status": False, "message": "Validation error", "errors": error_messages}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": False, "message": "An internal server error occurred"}
    )

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
def root():
    return {"status": True, "message": "Auth service is running"}