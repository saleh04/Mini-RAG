from fastapi import APIRouter, Depends, FastAPI, UploadFile, status
from fastapi.responses import JSONResponse
from controllers import DataController, ProjectController
from helpers.config import Settings, get_settings
import aiofiles
from models import ResponseSignal
import logging

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_V1_data"] )

@data_router.post("/upload/{project_id}")
async def upload_file(project_id: str, file: UploadFile,
                       app_settings: Settings = Depends(get_settings)):  

    datacontroller = DataController()

    is_valid, response_message = datacontroller.validate_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": response_message}
        )


    file_path, file_id = datacontroller.generate_unique_filepath(
        original_filename=file.filename, project_id=project_id)

    try:
        async with aiofiles.open(file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error occurred while saving the file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                 "file_ID": file_id}
    )
