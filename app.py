#app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import stripe
import sqlite3
import db

app = Flask(__name__)

app.secret_key = 'tu_clave_secreta'
stripe.api_key = 'tu_clave_secreta_de_stripe'
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost/database'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import sqlite3

# Definir la tabla de productos globalmente
tabla_productos = {
    1: {"nombre": "Capita America º1", "precio": 15.95, "stock": 42},
    2: {"nombre": "El Invencible Iror Man", "precio": 15.95, "stock": 50},
    3: {"nombre": "El Poderoso Thor", "precio": 15.95, "stock": 30},
    4: {"nombre": "El Increible Hulk", "precio": 15.95, "stock": 50},
    5: {"nombre": "Ojo de Halcon:Reino Oscuro º1", "precio": 15.95, "stock": 50},
    6: {"nombre": "Viuda Negra:Las cosas que dicen de alla", "precio": 15.95, "stock": 50},
    7: {"nombre": "Capitan America:El primer vengador", "precio": 9.95, "stock": 50},
    8: {"nombre": "Capitana Marvel", "precio": 9.95, "stock": 50},
    9: {"nombre": "Iror Man: El hombre de acero", "precio": 9.95, "stock": 50},
    10: {"nombre": "El increible Hulk", "precio": 9.95, "stock": 50},
    11: {"nombre": "El Poderoso Thor", "precio": 9.95, "stock": 50},
    12: {"nombre": "Los Vengadores", "precio": 9.95, "stock": 50},
    13: {"nombre": "CamisetaMarvel", "precio": 12.50, "stock": 50},
    14: {"nombre": "SudaderasMarvel", "precio": 12.50, "stock": 50},
    15: {"nombre": "PijamasMarvel", "precio": 12.50, "stock": 50},
    16: {"nombre": "CalcetinesMarvel Set-3", "precio": 12.50, "stock": 50},
    17: {"nombre": "Peluchemarvel", "precio": 12.50, "stock": 50},
    18: {"nombre": "PosterMarvel", "precio": 12.50, "stock": 50},

}

def obtener_producto_por_id(producto_id):
    producto = tabla_productos.get(producto_id)
    print("----- producto -----", producto)
    print("linea 45")
    return producto

def obtener_informacion_del_carrito_desde_bd():
    try:
        # Conectar a la base de datos (asegúrate de tener la ruta correcta)
        print("antes")

        conexion = sqlite3.connect('C:\\Users\\usuario\\PycharmProjects\\pythonProject\\M6CURSO\\pythonMarvel\\database\\database.db')
        print("despues")
        # Crear un cursor
        cursor = conexion.cursor()

        # Ejecutar una consulta para obtener la información del carrito
        cursor.execute("SELECT id, nombre, precio, stock FROM productos")

        # Obtener los resultados
        resultados = cursor.fetchall()
        print("resultados", resultados)

        # Cerrar la conexión
        conexion.close()

        # Retornar los resultados
        return resultados
    except Exception as e:
        print(f"Error al obtener información del carrito desde la base de datos: {e}")
        return []

def agregar_al_carrito(carrito, producto_id, cantidad, productos) :
    print("Entro 10")
    # Asegúrate de que el producto exista en la tabla de productos
    if producto_id in productos :
        producto = productos[producto_id]

        # Asegúrate de que haya suficiente stock
        if cantidad <= producto["stock"] :
            # Agrega el producto al carrito
            carrito.append({"id" : producto_id, "nombre" : producto["nombre"], "precio" : producto["precio"],
                            "cantidad" : cantidad})
            # Reduce el stock del producto
            productos[producto_id]["stock"] -= cantidad
            print(f"Producto agregado al carrito: {producto['nombre']} x{cantidad}")
        else :
            print(f"No hay suficiente stock para {producto['nombre']}")
    else :
        print("Producto no encontrado en la tabla de productos")


def calcular_total(carrito) :
    total = 0
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    print(carrito)
    print("OOOOOOOOOOOOOOOOOOOOOOOOOOOO")
    for producto in carrito :
        print("---------------------")
        print(producto)
        print(producto[2], 1)
        total += float(producto[2]) * 1
        print(total)

        print("---------------------")

    return total


# Ejemplo de uso:
#mi_carrito = []

# Agrega algunos productos al carrito (supongamos que seleccionaste el producto 1 y el producto 2)
#agregar_al_carrito(mi_carrito, 1, 2, tabla_productos)
#agregar_al_carrito(mi_carrito, 2, 1, tabla_productos)

# Calcula el total
#total_compra = calcular_total(mi_carrito)

# Imprime el total
#print(f"El total de la compra es: {total_compra} €")


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

        return render_template('abrirTienda.html')

@app.route('/abrirTienda', methods=['GET', 'POST'])
def abrirTienda():
    # Obtener información del carrito desde la base de datos (ejemplo usando SQLAlchemy)
    carrito = obtener_informacion_del_carrito_desde_bd()

    # Calcular el total (puedes hacerlo en la función o en tu plantilla)
    total = calcular_total(carrito)

    return render_template('mostrar_carrito.html', carrito=carrito, total=total)


@app.route('/comprar', methods=['POST'])
def comprar():
    try:
        producto_id = request.form.get('producto_id')

        # Lógica para procesar la compra y mostrar un mensaje


        mensaje = '¡Gracias por tu compra!'
        flash(mensaje, 'success')

    except Exception as e:
        mensaje = f'Error, inténtelo de nuevo: {str(e)}'
        flash(mensaje, 'error')

    return redirect(url_for('pago'))


@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        try:
            # Crea un pago utilizando la biblioteca de Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=1000,  # Monto en centavos
                currency='usd',
            )
            return render_template('pago.html', client_secret=payment_intent.client_secret)

        except stripe.error.CardError as e:
            flash(f"Error al procesar la tarjeta: {e.error.message}", 'error')
    return render_template('pago.html')

@app.route('/pago_exitoso')
def pago_exitoso():
    flash('¡Pago exitoso!', 'success')
    return redirect(url_for('comprar_resultado.html'))

@app.route('/comprar_resultado', methods=['GET', 'POST'])
def comprar_resultado():
    if request.method == 'POST':
        # Lógica para manejar la solicitud POST, si es necesario
        resultado_compra = 'Gracias por tu compra'  # O el valor adecuado
        static_url = 'url_de_la_imagen/static/imgmarvel/cmp.jpg'  # O el valor adecuado
        return render_template('comprar_resultado.html', resultado_compra=resultado_compra, static_url=static_url)

    # Si es una solicitud GET, simplemente renderiza la plantilla
    return render_template('comprar_resultado.html')


@app.route('/initialize_database')
def initialize_database():
    with app.app_context():
        db.create_all()
    return 'Base de datos inicializada correctamente.'

@app.route('/agregar_al_carrito', methods=['POST'])
def agregar_al_carrito2():
    print("Entro 5")
    producto_id = request.form.get('producto_id')
    cantidad = request.form.get('cantidad')
    print("Entro 6")
    # Lógica para obtener información del producto y calcular producto_agregado
    producto = obtener_producto_por_id(producto_id)

    if producto and producto['stock'] > 0:
        if 'carrito' not in session:
            session['carrito'] = []

        for item in session['carrito']:
            if item['id'] == producto_id:
                item['cantidad'] += 1
                break
        else:
            item = {'id': producto_id, 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': 1}
            print(item)
            session['carrito'].append(item)

        flash('Producto agregado al carrito', 'success')
        total_carrito = calcular_total(session['carrito'])
        mensaje = 'Producto agregado al carrito'
    else:
        mensaje = 'Producto no disponible'
        total_carrito = calcular_total(session.get('carrito', []))

    return jsonify({'message': mensaje, 'total': total_carrito})

@app.route('/eliminar_del_carrito/<int:producto_id>', methods=['POST'])
def eliminar_del_carrito(producto_id):
    # Lógica para eliminar el producto del carrito
    for item in session['carrito']:
        if item['id'] == producto_id:
            session['carrito'].remove(item)
            break
    flash('Producto eliminado del carrito', 'success')
    return redirect(url_for('mostrar_carrito'))

@app.route('/vaciar_carrito', methods=['POST'])
def vaciar_carrito():
    # Lógica para vaciar el carrito
    return redirect(url_for('mostrar_carrito'))

@app.route('/mostrar_carrito')
def mostrar_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)

    return render_template('mostrar_carrito.html', carrito=carrito, total=total)


if __name__ == '__main__' :

    app.run(debug=True)