from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import your models so that they are registered with the db instance
from .admin_model import Admin
# from .roles_model import Role
# from .topic_model import Topic
# from .resources_model import Resource
# from .explanation_model import Explanation