from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, sympify, residue, solve
import sympy

app = Flask(__name__)
CORS(app, origins=["https://vite-react-nu-gilt.vercel.app"])

@app.route("/api/evaluate", methods=["POST"])
def evaluate():
    data = request.get_json()
    z = symbols('z')
    try:
        f = sympify(data['function'])
        contour = data['contour']
        poles = solve(1 / f, z)
        residues = {str(p): str(residue(f, z, p)) for p in poles}
        integral = str(2 * sympy.pi * sympy.I * sum(residue(f, z, p) for p in poles))
        return jsonify({
            "success": True,
            "singularities": [str(p) for p in poles],
            "residues": residues,
            "integral": integral
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
