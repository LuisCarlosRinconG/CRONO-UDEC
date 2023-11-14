# Crear y almacenar objetos en la base de datos

class User:
    def __init__(self, nombre, email, cumple, password,roll):
        self.nombre= nombre
        self.email= email
        self.cumple = cumple
        self.password = password
        self.roll=roll
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'nombre':self.nombre,
            'email': self.email,
            'cumple':self.cumple,
            'password': self.password,
            'roll':self.roll
        }