from typing import Optional
import datetime

from sqlalchemy import String, DateTime, UniqueConstraint, ARRAY, Boolean
from sqlalchemy.orm import mapped_column, Mapped

from ..common.models import TimestampMixin
from ..rollup import BaseModel, app

from .basedata import GODS


class Member(TimestampMixin, BaseModel):
    __tablename__ = 'member'
    __table_args__ = (
        UniqueConstraint('email', name='email_unique_constraint'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100))
    nickname: Mapped[str] = mapped_column(String(20))
    name: Mapped[Optional[str]] = mapped_column(String(30))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    locale: Mapped[str] = mapped_column(String(5), default='en-US')
    timezone: Mapped[str] = mapped_column(String(6), default='00:00')

    nickname_isdirty = mapped_column(Boolean, nullable=False, default=True)
    roles = mapped_column(ARRAY(String), nullable=True)
    email_changed_at = mapped_column(DateTime, nullable=True)
    oauth2_server = mapped_column(String(30), nullable=True)
    oauth2_refreshtoken = mapped_column(String(2048), nullable=True)
    oauth2_accesstoken = mapped_column(String(1024), nullable=True)
    oauth2_avatar = mapped_column(String(1024), nullable=True)

    @classmethod
    def ensure(cls, session, email, name, locale, avatar,
               oauth2_refreshtoken, oauth2_accesstoken):
        member = session.query(cls).filter(cls.email == email).first()

        if member is None:
            member = Member(
                email=email,
                nickname=email.split('@')[0],
                nickname_isdirty=True,
                name=name,
                oauth2_server='google',
                # created_at=datetime.datetime.now(datetime.UTC),
                # modified_at=datetime.datetime.now(datetime.UTC),
            )

            if email in GODS:
                member.roles = ['god']

            session.add(member)

        member.locale = locale
        member.oauth2_avatar = avatar
        member.oauth2_refreshtoken = oauth2_refreshtoken
        member.oauth2_accesstoken = oauth2_accesstoken
        member.modified_at = datetime.datetime.now(datetime.UTC)
        session.flush()

        return member

    def set_refreshtoken(self, req):
        app.auth.set_refreshtoken(req, self.id, dict(
            roles=self.roles
        ))

    def create_token(self, app):
        payload = dict(
            nickname=self.nickname,
            timezone=self.timezone,
            locale=self.locale,
            avatar=self.oauth2_avatar,
            roles=self.roles,
        )
        return app.auth.dump(self.id, payload)

    def todict(self, safe=False):
        data = dict(
            nickname=self.nickname,
            nickname_isdirty=self.nickname_isdirty,
            timezone=self.timezone,
            locale=self.locale,
            avatar=self.oauth2_avatar,
            roles=self.roles,
            created_at=self.created_at.isoformat(timespec='seconds'),
            modified_at=self.modified_at.isoformat(timespec='seconds'),
        )

        if safe:
            data.update(
                id=self.id,
                email=self.email,
                name=self.name,
                phone=self.phone,
            )

        return data
