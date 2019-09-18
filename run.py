from app_folder import app, db
from app_folder.models import User, Product, Category

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Product': Product, 'Category': Category}

app.run()
