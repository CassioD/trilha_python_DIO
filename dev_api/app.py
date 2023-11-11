from flask import Flask, jsonify, request
import json

app = Flask(__name__)

desenvolvedores = [
    {'nome': 'Cassio',
     'habilidades': ['Python', 'Flask']
     },
    {'nome': 'Daniel',
     'habilidades': ['Python', 'MongoDB']
     }
]


@app.route('/dev/<int:id>/', methods = ['GET', 'PUT', 'DELETE'])
def desenvolvedor(id):
    if request.method == 'GET':
        try:
            response = desenvolvedores[id]
        except IndexError:
            mensagem = 'Desenvolvedor de ID {} não existe'.format(id)
            response = {'status': 'erro', 'mensagem': mensagem}
        return jsonify(response)

    elif request.method == 'PUT':
        dados = json.loads(request.data)
        desenvolvedores[id] = dados
        return jsonify(dados)
    elif request.method == 'DELETE':
        desenvolvedores.pop(id)
        return jsonify({'status': 'sucesso', 'mensagem': 'Registro excluído'})


@app.route('/dev/', methods = ['GET', 'POST'])
def lista_desenvolvedores():
    if request.method == 'POST':
        dados = json.loads(request.data)
        desenvolvedores.append(dados)
        return jsonify({'status': 'sucesso', 'mensagem': 'Registro inserido'})



if __name__ == '__main__':
    app.run(debug=True)
