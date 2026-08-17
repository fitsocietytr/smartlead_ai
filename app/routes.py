from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import AIServiceError, ai_service


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__, url_prefix="/api")
@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "basari": True,
        "durum": "healthy"
    }), 200


@pages_bp.route("/")
def index():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(silent=True) or {}
    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({"basari": False, "hata": "Mesaj gerekli."}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({"basari": True, "cevap": cevap}), 200

    except AIServiceError as exc:
        return jsonify({"basari": False, "hata": str(exc)}), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    data = request.get_json(silent=True) or {}

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:
        return jsonify(
            {
                "basari": False,
                "hata": "İsim ve telefon zorunludur.",
            }
        ), 400

    try:
        lead_ekle(isim, telefon, mesaj)

        return jsonify(
            {
                "basari": True,
                "mesaj": "Bilgileriniz başarıyla kaydedildi.",
            }
        ), 201

    except Exception:
        return jsonify(
            {
                "basari": False,
                "hata": "Kayıt sırasında bir hata oluştu.",
            }
        ), 500


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    try:
        leads = tum_leadler()

        sonuc = [dict(lead) for lead in leads]

        return jsonify(
            {
                "basari": True,
                "leads": sonuc,
            }
        ), 200

    except Exception:
        return jsonify(
            {
                "basari": False,
                "hata": "Kayıtlar alınırken bir hata oluştu.",
            }
        ), 500