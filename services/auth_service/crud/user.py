#  services/auth_service/crud/user.py
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime

from common.models.user import User
from common.models.subscriptions import UserSubscription
from services.auth_service.utils.security import hash_password, verify_password
from services.auth_service.schemas.user import UserCreate

#  Регистрация пользователя
def create_user(db: Session, user: UserCreate):
    db_user = User(
        login=user.login,
        password=hash_password(user.password)
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Користувач з таким логіном вже існує")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Помилка під час реєстрації: {str(e)}")


#  Аутентификация
def authenticate_user(db: Session, login: str, password: str):
    user = db.query(User).filter(User.login == login).first()

    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    if user.is_blocked:
        raise HTTPException(status_code=403, detail="Акаунт заблоковано")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Невірний пароль")

    return user

#  Всі користувачі
def get_all_users(db: Session):
    return db.query(User).all()

#  Запит на скидання пароля
def forgot_password(db: Session, email: str):
    user = db.query(User).filter(User.login == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    return {"message": f"Лист для скидання пароля надіслано на {email}"}

#  Скидання пароля
def reset_password(db: Session, email: str, new_password: str):
    user = db.query(User).filter(User.login == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    user.password = hash_password(new_password)
    db.commit()
    return {"message": "Пароль успішно змінено"}

#  Пошук користувача з підпискою
def get_user_by_login(db: Session, login: str):
    user = db.query(User).options(
        joinedload(User.uploads),
        joinedload(User.subscriptions).joinedload(UserSubscription.subscription)
    ).filter(User.login == login).first()

    if user:
        active_sub = next((s for s in user.subscriptions if s.is_active), None)
        user.subscription_type = active_sub.subscription.name if active_sub else "none"
    return user

#  Зміна пароля
def change_password(db: Session, login: str, old_password: str, new_password: str):
    user = get_user_by_login(db, login)
    if not user or not verify_password(old_password, user.password):
        return None
    user.password = hash_password(new_password)
    db.commit()
    return user

#  Видалення користувача
def delete_user_by_id(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Помилка при видаленні користувача: {str(e)}")