import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "gelistirme-gizli-anahtar")
    DATABASE_URL = os.environ.get("DATABASE_URL", "leads.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")

    BUSINESS_CONTEXT = """
    Sen Fit Society spor salonunun yapay zekâ asistanısın.
    Üyelik paketleri, spor salonu hizmetleri, ders programları
    ve ücretsiz deneme dersi hakkında bilgi ver.
    Ziyaretçiye kibar, samimi ve motive edici bir dille Türkçe cevap ver.
    Üyelik veya ücretsiz deneme dersi için iletişim bilgisi bırakmaya yönlendir.
    """

    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}