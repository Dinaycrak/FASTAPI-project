from fastapi import FastAPI
from routes.user_routes import router as user_router
from routes.document_type_routes import router as document_type_router
from routes.comments_routes import router as comments_router
from routes.delivery_status_routes import router as delivery_status_router
from routes.document_routes import router as document_router
from routes.progress_routes import router as progress_router
from routes.project_rol_routes import router as project_rol_router
from routes.project_routes import router as project_router
from routes.research_line_routes import router as research_line_router
from routes.rol_routes import router as rol_router
from routes.scheduled_delivery_routes import router as scheduled_delivery_router
from routes.status_history_routes import router as status_history_router
from routes.status_routes import router as status_router
from routes.student_routes import router as student_router
from routes.user_project_routes import router as user_project_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    #"http://localhost.tiangolo.com",
    "ep-royal-smoke-afutcih1-pooler.c-2.us-west-2.aws.neon.tech",
    "http://localhost"
    #"http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(document_type_router)
app.include_router(comments_router)
app.include_router(delivery_status_router)
app.include_router(document_router)
app.include_router(progress_router)
app.include_router(project_router)
app.include_router(project_rol_router)
app.include_router(research_line_router)
app.include_router(rol_router)
app.include_router(scheduled_delivery_router)
app.include_router(status_history_router)
app.include_router(status_router)
app.include_router(student_router)
app.include_router(user_project_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)