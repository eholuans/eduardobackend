from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///musicas.db'
db = SQLAlchemy(app)

class Musicas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomemusica = db.Column(db.String(200), unique=True, nullable=False)

#homepage
@app.route('/')
def index():
    q = request.args.get('q', '')
    if q:
        musicas = Musicas.query.filter(Musicas.nomemusica.ilike(f'%{q}%')).all()
    else:
        musicas = Musicas.query.all()

    return render_template('index.html', musicas=musicas)

#criar musica
@app.route('/create', methods=['POST'])
def criarmusica():
    musica= request.form['nomemusica']
    existing_music = Musicas.query.filter_by(nomemusica=musica).first()
    if existing_music:
        return "Musica ja existe!", 400
    
    novamusica = Musicas(nomemusica=musica)
    db.session.add(novamusica)
    db.session.commit()
    return redirect('/')    
#deletar musica
@app.route('/delete/<int:id>', methods=['POST'])
def deletarmusica(id):
    musica = Musicas.query.get(id)
    if musica:
        db.session.delete(musica)
        db.session.commit()
    return redirect('/')
#atualizar musica
@app.route('/update/<int:id>', methods=['POST'])
def atualizarmusica(id):
    musica = Musicas.query.get(id)
    if musica:
        nova_nome = request.form['nomemusica']
        existing_music = Musicas.query.filter_by(nomemusica=nova_nome).first()
        if existing_music and existing_music.id != id:
            return "Musica ja existe!", 400
        
        musica.nomemusica = nova_nome
        db.session.commit()
    return redirect('/')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)