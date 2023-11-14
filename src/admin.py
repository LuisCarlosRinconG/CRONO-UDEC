# Crear y almacenar objetos en la base de datos

class Admin:
    def __init__(self, publicacion, autor,fecha, comentario):
        self.publicacion= publicacion
        self.autor= autor
        self.fecha = fecha
        self.comentario = comentario
    
    # Metodo para almacenar los documentos
    def formato_doc(self):
        return{
            'publicacion':self.publicacion,
            'autor': self.autor,
            'fecha':self.fecha,
            'comentario': self.comentario
        }
