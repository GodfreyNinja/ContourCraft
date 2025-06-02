from flask import Flask, request, jsonify
from flask_cors import CORS
from sympy import symbols, sympify, apart, residue, I, pi, simplify
from sympy.abc import z

app = Flask(__name__)
CORS(app)

@app.route('/api/evaluate', methods=['POST'])
def evaluate_integral():
    data = request.json
    f_str = data.get('function')
    contour = data.get('contour')

    try:
        f = sympify(f_str)
        singularities = []
        residues = {}
        integral_val = 0

        f_apart = apart(f, z)
        den = f_apart.as_numer_denom()[1]
        poles = den.as_poly(z).all_roots(multiple=True)

        for pole in poles:
            singularities.append(str(pole))
            res = residue(f, z, pole)
            residues[str(pole)] = str(simplify(res))
            integral_val += 2 * pi * I * res

        return jsonify({
            'success': True,
            'singularities': singularities,
            'residues': residues,
            'integral': str(simplify(integral_val))
        })

    except Exception as e:
        return jsonify({ 'success': False, 'error': str(e) })

if __name__ == '__main__':
    app.run(debug=True)
