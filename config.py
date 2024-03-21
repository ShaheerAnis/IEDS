import os


class Config:
    SECRET_KEY = 'your-secret-key'
    #Shaheer URI
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BServer%3DDESKTOP-EN20RGA%5CSQLEXPRESS%3BDatabase%3DAliMadad%3BTrusted_Connection%3Dyes%3BPort%3D1433"
    
    #Saib URI
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BODBC+Driver+17+for+SQL+Server%7D%3BServer%3DDESKTOP-Q7S1I2R%3BDatabase%3DAliMadad%3BTrusted_Connection%3Dyes%3BPort%3D1433"

    # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=DRIVER%3D%7BSQL+Server+Native+Client+11.0%7D%3BServer%3DDESKTOP-Q7S1I2R%5CSQLEXPRESS%3BDatabase%3DAliMadad%3BTrusted_Connection%3Dyes%3BPort%3D1433"
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://shaheertest_SQLLogin_1:2wfcyl22k8@Courses.mssql.somee.com/Courses?driver=SQL+Server+Native+Client+11.0"
    #SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://shaheertest_SQLLogin_1:2wfcyl22k8@Courses.mssql.somee.com/Courses"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = '465'
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'bizintro1@gmail.com'
    MAIL_PASSWORD = "mcgjjvnhbfbrabgo"
    SECRET_KEY = 'your-secret-key'
    
    SESSION_PERMANENT = True
    UPLOAD_FOLDER = 'uploads'

  
  