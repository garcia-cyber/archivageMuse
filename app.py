from flask import Flask ,  render_template   



app = Flask(__name__)



#
# acceuil 
@app.route('/')
def home():
    return 'hello'






## boucle 

if __name__ == '__main__':
    app.run(debug=True)