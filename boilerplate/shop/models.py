from typing import Optional, Any
import enum

from sqlalchemy import String, ForeignKey, UniqueConstraint, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..common.models import TimestampMixin
from ..rollup import BaseModel


class ShopType(enum.Enum):
    KITCHEN = 'Kitchen'
    STORE = 'Store'
    SERVICE = 'Service'


class Shop(TimestampMixin, BaseModel):
    __tablename__ = 'shop'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(255))
    type: Mapped[ShopType]
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    address: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[Optional[str]] = mapped_column(String(100))


class Category(BaseModel):
    __tablename__ = 'category'
    __table_args__ = (
        UniqueConstraint('title_en', name='category_title_en_uniquekey'),
        UniqueConstraint('title_fa', name='category_title_fa_uniquekey'),
        UniqueConstraint('title_ar', name='category_title_ar_uniquekey'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title_en: Mapped[str] = mapped_column(String(50))
    title_fa: Mapped[str] = mapped_column(String(50))
    title_ar: Mapped[str] = mapped_column(String(50))
    icon: Mapped[str] = mapped_column(String(255))

    def todict(self):
        return dict(
            id=self.id,
            title_en=self.title_en,
            title_fa=self.title_fa,
            title_ar=self.title_ar,
            icon=self.icon,
        )


class Brand(BaseModel):
    __tablename__ = 'brand'
    __table_args__ = (
        UniqueConstraint('title', name='brand_title_uniquekey'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    logo: Mapped[str] = mapped_column(String(255))

    def todict(self):
        return dict(
            id=self.id,
            title=self.title,
            logo=self.logo,
        )


class Good(TimestampMixin, BaseModel):
    __tablename__ = 'good'

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    brand_id: Mapped[int] = mapped_column(ForeignKey('brand.id'))
    shop_id: Mapped[int] = mapped_column(ForeignKey('shop.id'))

    title_en: Mapped[str] = mapped_column(String(50))
    title_fa: Mapped[str] = mapped_column(String(50))
    title_ar: Mapped[str] = mapped_column(String(50))

    description_en: Mapped[str] = mapped_column(String(1024))
    description_fa: Mapped[str] = mapped_column(String(1024))
    description_ar: Mapped[str] = mapped_column(String(1024))

    images: Mapped[list[str]] = mapped_column(ARRAY(String))
    kinds: Mapped[list['Kind']] = relationship(back_populates='good')
    spec: Mapped[dict[str, Any]]

    def todict(self):
        return dict(
            id=self.id,
            title_en=self.title_en,
            title_fa=self.title_fa,
            title_ar=self.title_ar,
            description_en=self.description_en,
            description_fa=self.description_fa,
            description_ar=self.description_ar,
            images=self.images,
            spec=self.spec,
        )


class Kind(BaseModel):
    __tablename__ = 'kind'

    id: Mapped[int] = mapped_column(primary_key=True)

    title_en: Mapped[str] = mapped_column(String(50))
    title_fa: Mapped[str] = mapped_column(String(50))
    title_ar: Mapped[str] = mapped_column(String(50))

    image: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    count: Mapped[int]

    good_id: Mapped[int] = mapped_column(ForeignKey('good.id'))
    good: Mapped[Good] = relationship(back_populates='kinds')

    def todict(self):
        return dict(
            id=self.id,
            good_id=self.good_id,
            title_en=self.title_en,
            title_fa=self.title_fa,
            title_ar=self.title_ar,
            image=self.image,
            price=self.price,
            count=self.count,
        )
