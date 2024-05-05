# Mini mini fonction pour tester si tout fonctionne

from flask import Flask, render_template

app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'fG4gH45smP!481Mps52me' 

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('Templates/hello.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)