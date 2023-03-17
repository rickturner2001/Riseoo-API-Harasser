from sqlalchemy.orm import Session

from database.models import Sponsor, RegisteredUser
from database.initialize import Base
from sqlalchemy.orm import sessionmaker
from database.initialize import engine


def get_session():
    Session = sessionmaker(bind=engine)
    return Session()


def create_sponsor(db: Session, sponsor_username: str):
    sponsor = Sponsor(sponsor_username=sponsor_username)
    db.add(sponsor)
    db.commit()
    db.refresh(sponsor)
    return sponsor


def get_sponsor_by_id(db: Session, sponsor_id: int):
    return db.query(Sponsor).filter(Sponsor.id == sponsor_id).first()


def get_sponsor_by_username(db: Session, sponsor_username: str):
    return db.query(Sponsor).filter(Sponsor.sponsor_username == sponsor_username).first()


def get_all_sponsors(db: Session):
    return db.query(Sponsor).all()


# Users
def create_registered_user(db: Session, user: str, password: str, email: str, sponsor_username: str):
    registered_user = RegisteredUser(
        user=user, password=password, email=email, sponsor_username=sponsor_username)
    db.add(registered_user)
    db.commit()
    db.refresh(registered_user)
    return registered_user


def get_registered_user_by_id(db: Session, registered_user_id: int):
    return db.query(RegisteredUser).filter(RegisteredUser.id == registered_user_id).first()


def get_all_registered_users(db: Session):
    return db.query(RegisteredUser).all()


def get_registered_users_by_sponsor_username(db: Session, sponsor_username: str):
    return db.query(RegisteredUser).filter(RegisteredUser.sponsor_username == sponsor_username).all()


def update_registered_user(db: Session, registered_user_id: int, user: str, password: str, email: str, sponsor_username: str):
    registered_user = db.query(RegisteredUser).filter(
        RegisteredUser.id == registered_user_id).first()
    if registered_user:
        registered_user.user = user
        registered_user.password = password
        registered_user.email = email
        registered_user.sponsor_username = sponsor_username
        db.commit()
        db.refresh(registered_user)
    return registered_user


def delete_registered_user(db: Session, registered_user_id: int):
    registered_user = db.query(RegisteredUser).filter(
        RegisteredUser.id == registered_user_id).first()
    if registered_user:
        db.delete(registered_user)
        db.commit()
    return registered_user
