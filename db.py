#db.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# noinspection PyMethodMayBeStatic
class Tienda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)


    def __init__(self, nombre, descripcion=None):
        self.nombre = nombre
        self.descripcion = descripcion

    def agregar_producto(self, nombre_producto, precio, stock):
        producto = Producto(nombre=nombre_producto, precio=precio, stock=stock, tienda=self)
        db.session.add(producto)
        db.session.commit()

    def comprar_producto(self, id_producto, cantidad):
        producto = Producto.query.get(id_producto)
        if producto and producto.stock >= cantidad:
            # Realizar la lógica de compra, como restar la cantidad del stock
            producto.stock -= cantidad
            db.session.commit()
            return True
        else:
            return False

    def mostrar_productos(self):
        return self.productos

# Otros métodos y campos que puedas necesitar...

# noinspection PyMethodParameters
class Producto(db.Model):
    __tablename__ = 'producto'  # Reemplaza 'producto' con el nombre de tu tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def __init__(self, nombre, precio, stock) :
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

        print("compar realizada con exito")

    def __str__(self) :
        return f"producto(id={self.id}, nombre={self.nombre},precio={self.precio},stock={self.stock})"


class Carrito(db.Model) :
    __tablename__ = 'carrito'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"carrito(id={self.id}, producto_id={self.producto_id}, cantidad={self.cantidad})"


# noinspection PyMethodMayBeStatic
class Transaccion(db.Model) :
    __tablename__ = 'transaccion'
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    tipo_operacion = db.Column(db.String(20), nullable=False)
    fecha = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self) :
        return f"Transaccion(id={self.id}, producto_id ={self.producto_id },nombre={self.nombre}, cantidad={self.cantidad}, tipo_operacion={tipo_operacion}, fecha={fecha})"

    def transaccion_desde_carrito(self, carrito) :
        # Realizar la transacción desde el carrito a la tabla de transacciones
        self.producto_id = carrito.producto_id
        self.nombre = carrito.producto.nombre
        self.cantidad = carrito.cantidad
        self.tipo_operacion = 'Venta'  # o cualquier otra operación que desees
        carrito.producto.reducir_stock(carrito.cantidad)

        # Eliminar el artículo del carrito después de la transacción
        db.session.delete(carrito)

        # Agregar la transacción a la tabla de transacciones
        db.session.add(self)

        # Confirmar los cambios en la base de datos
        db.session.commit()

    def carrito(self) :
        # Devolver productos en el carrito asociado al usuario o la sesión actual
        # Aquí asumimos que guardas información de la sesión en Flask, ajusta según tu aplicación
        if 'carrito' in session :
            carrito = session['carrito']
            productos_en_carrito = Carrito.query.filter(Carrito.id.in_(carrito)).all()
            return productos_en_carrito
        else :
            return []

    def reducir_stock(self, cantidad) :
            if self.stock >= cantidad :
                self.stock -= cantidad
                return True
            else :
                return False


