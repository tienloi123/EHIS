import base64
import logging

import cv2
import numpy as np
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from keras_facenet import FaceNet
from mtcnn import MTCNN
from starlette import status

from app.constant import AppStatus
from app.core import error_exception_handler
from app.cruds import user_crud
from app.models import User
from app.schemas import AuthLogin, UserUpdate, AuthLoginFace, Face
from app.utils import verify_password
from app.apis.depends.authorization import create_access_token, create_refresh_token

mtcnn = MTCNN()
model = FaceNet()

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, auth_data: AuthLogin):
        user = await user_crud.get(self.session, User.email == auth_data.email)

        if user is None:
            logger.error(AppStatus.ERROR_404_USER_NOT_FOUND.message,
                         exc_info=ValueError(AppStatus.ERROR_404_USER_NOT_FOUND))
            raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)

        if not verify_password(password=auth_data.password, hashed_password=user.hashed_password):
            logger.error(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD.message,
                         exc_info=ValueError(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD)

        data = {"user_id": user.id, "role": user.role}

        access_token = create_access_token(data=data)
        refresh_token = create_refresh_token(data=data)

        await user_crud.update(session=self.session,
                               obj_in=UserUpdate(access_token=access_token, refresh_token=refresh_token), db_obj=user)

        return {"access_token": access_token, "refresh_token": refresh_token, "full_name": user.name}

    async def login_face(self, auth_face_data: AuthLoginFace):
        data = await self.recognize(images=auth_face_data.images)
        return data

    async def record(self, face_data: Face, user):
        try:
            user_id = user.id
            frames = [self.load_image_from_base64(image) for image in face_data.images]
            for frame in frames:
                faces = mtcnn.detect_faces(frame)
                await self.handle_faces(faces, user_id, frame)
            return {"status": "success", "message": "Face data processed successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing face data: {str(e)}"
            )

    async def handle_faces(self, faces, user_id: int, frame):
        person_embeddings = {}

        for face in faces:
            embedding = self.extract_embedding(face, frame)
            if embedding is not None:
                if user_id in person_embeddings:
                    person_embeddings[user_id].append(embedding)
                else:
                    person_embeddings[user_id] = [embedding]

        for user_id, embeddings_list in person_embeddings.items():
            mean_embedding = np.mean(embeddings_list, axis=0).tolist()
            user = await user_crud.get(self.session, User.id == user_id)
            if not user:
                raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)

            await user_crud.update(session=self.session, obj_in=UserUpdate(embedding=mean_embedding), db_obj=user)
        return "Thành công! Bạn đã ghi nhận khuôn mặt."

    async def recognize(self, images):
        try:
            frames = [self.load_image_from_base64(image) for image in images]
            for frame in frames:
                faces = mtcnn.detect_faces(frame)
                if faces:
                    for face in faces:
                        embedding = self.extract_embedding(face, frame)
                        if embedding is not None:
                            recognized_label = await self.match_embedding(embedding)
                            user = await user_crud.get(self.session, User.id == recognized_label)
                            if not user:
                                raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)
                            user_id = user.id
                            role= user.role
                            if user is None:
                                raise "ABC"
                            else:

                                data_token = {"user_id": user_id, "role": role}

                                access_token = create_access_token(data=data_token)

                                refresh_token = create_refresh_token(data=data_token)

                                await user_crud.update(session=self.session,
                                                       obj_in=UserUpdate(access_token=access_token,
                                                                         refresh_token=refresh_token), db_obj=user)
                                return {"access_token": access_token, "refresh_token": refresh_token,
                                        "full_name": user.name}
        except Exception as e:
            print(e)
            raise error_exception_handler(app_status=AppStatus.ERROR_500_INTERNAL_SERVER_ERROR)

    async def match_embedding(self, embedding: np.ndarray):
        try:
            users = await user_crud.get_all(self.session)
            for user in users:
                if user.embedding:
                    stored_embedding = np.array(user.embedding)
                    similarity = np.dot(embedding, stored_embedding) / (
                            np.linalg.norm(embedding) * np.linalg.norm(stored_embedding))
                    print('++++++++++++', similarity)
                    if similarity >= 0.7:
                        return user.id
            return None
        except Exception as e:
            print(e)
            return None

    def extract_embedding(self, face, frame):
        try:
            x, y, width, height = face['box']

            # Ensure the coordinates are within the image boundaries
            if x < 0 or y < 0 or x + width > frame.shape[1] or y + height > frame.shape[0]:
                return None

            # Extract the face region from the image
            face_region = frame[y:y + height, x:x + width]

            # Validate if the face_region is a valid numpy array
            if face_region is None or face_region.size == 0:
                return None

            rgb_face = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
            resized_face = cv2.resize(rgb_face, (160, 160))  # Resize to (160, 160)
            input_face = np.expand_dims(resized_face, axis=0)  # Shape (1, 160, 160, 3)

            embeddings = model.embeddings(input_face)
            if embeddings is not None and embeddings.shape[0] > 0:
                return embeddings[0]
            else:
                return None
        except Exception as e:
            return None

    def load_image_from_base64(self, image_base64: str):
        try:
            img_data = base64.b64decode(image_base64.split(',')[1])
            np_array = np.frombuffer(img_data, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
            if frame is None or frame.size == 0:
                return None
            return frame
        except Exception as e:
            return None

    async def logout(self, user):
        logger.info(f"logout called by {user.email}.")
        access_token = ""
        refresh_token = ""
        await user_crud.update(session=self.session, obj_in=UserUpdate(access_token=access_token,
                                                                       refresh_token=refresh_token), db_obj=user)
        logger.info(f"logout called successfully with access_token:{access_token}, refresh_token:{refresh_token}")
        return {"access_token": access_token, "refresh_token": refresh_token}
