from app import create_app
from app.extensions import db
from app.utils import crear_datos_demo
import os

app = create_app()

with app.app_context():
    db.create_all()
    crear_datos_demo()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
