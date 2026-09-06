# Red Neuronal Evolutiva
Este proyecto tiene por objetivo demostrar las capacidades del machine learning y de las redes neuronales para automatizar tareas. Este programa está dirigido para un público que le cuesta visualizar el funcionamiento de las mismas y su utilidad.

El algoritmo en cuestión consta de dos partes:

La primera es un videojuego de tipo flappy bird totalmente funcional el cual puede ser jugado por el usuario mediante entradas básicas. Este videojuego puedes ejecutarlo en el siguiente archivo:

```bash mainGame.py ``` 

La segunda parte es el mismo videojuego, pero ahora controlado por una red neuronal evolutiva. Este lo puedes ejecutar en el siguiente archivo:

```bash mainNN.py ``` 

## Funcionamiento del Videojuego

El videojuego tipo flappy bird funciona a partir de la librería pygame, la cual nos permite crear videojuegos sencillos utilizando el lenguaje de programación python

El algoritmo más importante del videojuego puede ser descrito mediante este pseudocódigo:

**Entradas**
barraEspaciadoraPresionada, collisionDetectada, obstaculoSuperado
```
1. DEFINIR puntaje
2. SI barraEspaciadoraPresionada:
	- ACCION saltar
3. DE LO CONTRARIO:
	- ACCION caer
4. SI obstaculoSuperado:
	- SUMAR puntaje + 1
5. SI collisionDetectada:
	- ACCION destruirPajaro
```
**Salidas**
puntaje

## Funcionamiento de la red neuronal
Nuestra red neuronal funciona a partir de la librería tensor flow. Para poder entrenarlo utilizamos el proceso de evolución, en donde varios candidatos con pesos aleatorios son puestos a jugar para al final seleccionar al mejor, mutar sus pesos y repetir el proceso hasta encontrar al mejor modelo.

Nuestro proceso de redes neuronales puede describirse mediante dos pseudocódigos, el primero para describir el procesamiento y salidas de una sola red neuronal, y el segundo describe el proceso evolutivo de nuestros modelos.

**Red Neuronal:**

**Entradas**
posicionYDelPajaro, distanciaXObstaculo, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo
```
1. NORMALIZAR posicionYDelPajaro, distanciaXObstaculo, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo
2. DEFINIR prediccion
3. DEFINIR accion
4. preddiccion = PROCESAR prediccionRedNeuronal(posicionYDelPajaro, distanciaXObstaculo, distanciaYAperturaDeObastaculo, posicionXObstaculo, posicionYAperturaDeObastaculo)
6. SI prediccion == 1:
7. accion = saltar
8. DE LO CONTRARIO:
9. accion = caer
10. PROCESAR controlarPajaro(accion)
11.  LEER puntajeDePajaro
```
**Salidas**
accion, puntajeDePajaro

**Proceso Evolutivo**  
```
1. DEFINIR listaDeRedesNeuronales
2. DEFINIR puntajeMasAlto = 0
3. DEFINIR mejorRedNeuronal
4. REPETIR 50 VECES:
	- DEFINIR redNeuronalAleatorea
	- redNeuronalAleatorea = Nueva RedNeuronal
	- GUARDAR redNeuronal EN listaDeRedesNeuronales
5. MIENTRAS listaDeRedesNeuronales NO SEA IGUAL A 0:
	- REPETIR POR CADA redNeuronal EN listaDeRedesNeuronales:
		- PROCESAR redNeuronal.controlarPajaro()
		- SI redNueronal.viva NO ES IGUAL A verdadero:
			- ACCION destruirRedNeuronal
		- SI redNeuronal.puntaje > puntajeMasAlto
			- puntajeMasAlto = redNeuronal.puntaje
			- mejorRedNeuronal = redNeuronal
6. ACCION mutar(mejorRedNeuronal)
```
