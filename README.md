# Simulador-de-Portafolio-de-inversi-n
Este es un simulador de inversiones para que se muestren los movimientos de las inversiones realizadas.
Este archivo describe el proyecto. Explica qué hace la aplicación, cómo ejecutarla y cómo está organizada ademas de explicar cada una de las funciones del archivo.

**app.py**
Este archivo es la interfaz de usuario. Aquí es donde se usa Streamlit para crear la aplicación visual. Nos permite como usuario ingresar el capital inicial, seleccionar activos, comprar o vender y ver el estado del portafolio. No contiene lógica compleja, solo conecta lo que el usuario hace con las funciones del sistema.

**portfolio_model.py**
Este archivo define el portafolio como una clase. Guarda el dinero disponible, las acciones que se tienen y el historial del valor del portafolio. También contiene funciones simples para agregar o quitar acciones y actualizar el dinero. Es la base de datos en memoria del sistema.

**trading.py**
Este archivo contiene la lógica principal de compra y venta. Aquí se calcula cuántas acciones se compran, cuánto dinero se descuenta, cuánto se recibe al vender y se aplican comisiones. Usa el modelo del portafolio y los precios del mercado. Es el “cerebro” de las operaciones.

**market_data.py**
Este archivo se encarga de obtener los precios de las acciones desde internet usando yfinance. Su única responsabilidad es traer datos del mercado. Esto permite separar la lógica de negocio de la obtención de datos externos.

**settings.py**
Este archivo guarda configuraciones del sistema, como las comisiones de cada acción. Sirve para que estos valores no estén mezclados con la lógica del programa y se puedan cambiar fácilmente.

**formatters.py**
Este archivo es opcional y sirve para funciones auxiliares, como formatear números, dinero o textos. No es obligatorio, pero ayuda a mantener el código organizado si el proyecto crece.

**requirements.txt**
Este archivo lista todas las librerías que necesita el proyecto para funcionar. Nos sirve para que cualquier persona pueda instalar las dependencias fácilmente usando pip.

**Estructura general del proyecto**
El proyecto está dividido en partes para que sea más fácil de entender y mantener. La interfaz está separada de la lógica, la lógica está separada de los datos externos, y las configuraciones están en otro lugar. Esto hace que el sistema sea más claro, escalable y profesional.
