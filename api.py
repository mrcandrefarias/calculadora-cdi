from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="static")
CORS(app)
# Parâmetros fixos
CDI_ANUAL =  0.1465 

# Tabela do IR regressivo (renda fixa)
def calcular_ir(prazo_dias):
    if prazo_dias <= 180:
        return 0.225
    elif prazo_dias <= 360:
        return 0.20
    elif prazo_dias <= 720:
        return 0.175
    else:
        return 0.15


@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/calcular", methods=["POST"])
def calcular():
    data = request.get_json()

    valor_investido = float(data.get("valor_investido", 0))
    percentual_cdi = float(data.get("percentual_cdi", 100)) / 100  # Ex: 100% vira 1.0
    dias = int(data.get("prazo_dias", 0))

    # CDI diário aproximado
    cdi_diario = (1 + CDI_ANUAL) ** (1 / 252) - 1
    rendimento_total = (1 + cdi_diario * percentual_cdi) ** dias - 1
    valor_bruto = valor_investido * (1 + rendimento_total)

    # Imposto de renda
    aliquota_ir = calcular_ir(dias)
    imposto = (valor_bruto - valor_investido) * aliquota_ir
    valor_liquido = valor_bruto - imposto

    resultado = {
        "valor_investido": round(valor_investido, 2),
        "valor_bruto": round(valor_bruto, 2),
        "imposto": round(imposto, 2),
        "valor_liquido": round(valor_liquido, 2),
        "rentabilidade_percentual": round(rendimento_total * 100, 2),
        "aliquota_ir": f"{aliquota_ir*100:.1f}%"
    }

    return jsonify(resultado)

if __name__ == "__main__":
    app.run(debug=True)

