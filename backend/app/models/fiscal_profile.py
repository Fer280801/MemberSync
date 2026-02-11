from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class FiscalProfile(Base):
    __tablename__ = "fiscal_profiles"
    __table_args__ = (UniqueConstraint("user_id", name="uq_fiscal_profile_user"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tax_id: Mapped[str | None] = mapped_column(String(50))
    legal_name: Mapped[str | None] = mapped_column(String(255))
    address: Mapped[str | None] = mapped_column(String(255))

    user = relationship("User", back_populates="fiscal_profile")
