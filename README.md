# Red Neuronal Evolutiva
Este proyecto tiene por objetivo demostrar las capacidades del machine learning y de las redes neuronales para automatizar tareas. Este programa está dirigido para un público que le cuesta visualizar el funcionamiento de las mismas y su utilidad.

El algoritmo en cuestión consta de dos partes:

La primera es un videojuego de tipo flappy bird totalmente funcional el cual puede ser jugado por el usuario mediante entradas básicas. Este videojuego puedes ejecutarlo en el siguiente archivo:

```bash main.py ``` 

La segunda parte es el mismo videojuego, pero ahora controlado por una red neuronal evolutiva. Este lo puedes ejecutar en el siguiente archivo:

```bash main_nn.py ``` 

## Librerías y dependencias
Para ejecutar el proyecto necesitas Python y las siguientes librerías. Las instrucciones de instalación se ejecutan desde una terminal, preferentemente con el entorno virtual del proyecto activado.

### Librerías que debes instalar

- **Pygame:** gestión del videojuego y sus físicas.
  ```bash
  python -m pip install pygame
  ```
  Documentación: https://www.pygame.org/docs/

- **NumPy:** operaciones con matrices y arreglos numéricos.
  ```bash
  python -m pip install numpy
  ```
  Documentación: https://numpy.org/doc/stable/

- **TensorFlow:** desarrollo y ejecución de la red neuronal.
  ```bash
  python -m pip install --upgrade pip
  python -m pip install tensorflow
  ```
  Documentación: https://www.tensorflow.org/learn
  Guía de instalación: https://www.tensorflow.org/install

  **Nota:** TensorFlow no es compatible con todas las versiones de Python. Antes de instalarlo, consulta los requisitos de la versión actual en la guía oficial. La guía de instalación con pip indica compatibilidad con Python 3.10 a 3.13 para la versión documentada actualmente.

### Módulos incluidos en Python

Los siguientes módulos forman parte de la biblioteca estándar de Python. **No necesitas instalarlos con pip**; basta con importarlos en el código.

- **math:** funciones y constantes matemáticas. No requiere instalación.
  Documentación: https://docs.python.org/3/library/math.html

- **random:** generación de números y selecciones pseudoaleatorias. No requiere instalación.
  Documentación: https://docs.python.org/3/library/random.html

- **copy:** creación de copias superficiales y profundas de objetos. No requiere instalación.
  Documentación: https://docs.python.org/3/library/copy.html

- **os:** interacción con el sistema operativo y manejo de rutas y archivos. No requiere instalación.
  Documentación: https://docs.python.org/3/library/os.html

### Instalación rápida

Si ya tienes una versión compatible de Python y `pip` configurado, puedes instalar las tres dependencias externas ejecutando:

```bash
python -m pip install pygame numpy tensorflow
```


## Funcionamiento del Videojuego

El videojuego tipo flappy bird funciona a partir de la librería pygame, la cual nos permite crear videojuegos sencillos utilizando el lenguaje de programación python

El algoritmo más importante del videojuego puede ser descrito mediante este pseudocódigo:

**Entradas**
clickPresionado, collisionDetectada, obstaculoSuperado (Todas son de tipo Boleano)
```
1. DEFINIR puntaje
2. SI clickPresionado:
	2.1 ACCION saltar
3. DE LO CONTRARIO:
	3.1 ACCION caer
4. SI obstaculoSuperado:
	4.1 SUMAR puntaje + 1
5. SI collisionDetectada:
	5.1 ACCION destruirPajaro
```
**Salidas**
puntaje -> entero

## Funcionamiento de la red neuronal
Nuestra red neuronal funciona a partir de la librería tensorflow. Para poder entrenarlo utilizamos el proceso de evolución, en donde varios candidatos con pesos aleatorios son puestos a jugar para al final seleccionar al mejor, mutar sus pesos y repetir el proceso hasta encontrar al mejor modelo.

Nuestro proceso de redes neuronales puede describirse mediante dos pseudocódigos, el primero para describir el procesamiento y salidas de una sola red neuronal, y el segundo describe el proceso evolutivo de nuestros modelos.

**Red Neuronal:**

**Entradas**
posicionYDelPajaro, velocidadYDelPajaro, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo (Todas de tipo float) 
```
1. NORMALIZAR posicionYDelPajaro, distanciaXObstaculo, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo
2. DEFINIR prediccion
3. DEFINIR accion
4. preddiccion = PROCESAR prediccionRedNeuronal(posicionYDelPajaro, distanciaXObstaculo, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo)
5. SI prediccion == 1:
    5.1 accion = saltar
6. DE LO CONTRARIO:
    6.1 accion = caer
7. PROCESAR controlarPajaro(accion)
8. LEER puntajeDePajaro
```
**Salidas**
accion -> dígito, puntajeDePajaro -> entero

**Proceso Evolutivo**  
```
1. DEFINIR listaDeRedesNeuronales
2. DEFINIR puntajeMasAlto = 0
3. DEFINIR mejorRedNeuronal
4. REPETIR 50 VECES:
	4.1 DEFINIR redNeuronalAleatorea
	4.2 redNeuronalAleatorea = Nueva RedNeuronal
	4.3 GUARDAR redNeuronal EN listaDeRedesNeuronales
5. MIENTRAS listaDeRedesNeuronales NO SEA IGUAL A 0:
	5.1 REPETIR POR CADA redNeuronal EN listaDeRedesNeuronales:
		5.1.1 PROCESAR redNeuronal.controlarPajaro()
		5.1.2 SI redNueronal.viva ES IGUAL A falso:
			5.1.2.1 ACCION destruirRedNeuronal
		5.1.3 SI redNeuronal.puntaje > puntajeMasAlto
			5.1.3.1 puntajeMasAlto = redNeuronal.puntaje
			5.1.3.2 mejorRedNeuronal = redNeuronal
6. ACCION mutar(mejorRedNeuronal)
```
