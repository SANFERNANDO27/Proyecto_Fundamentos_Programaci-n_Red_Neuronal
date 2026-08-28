# Red Neuronal Evolutiva
Este proyecto tiene por objetivo demostrar las capacidades del machine learning y de las redes neuronales para automatizar tareas. Este programa está dirigido para un público que le cuesta visualizar el funcionamiento de las mismas y su utilidad.

El algoritmo en cuestión consta de dos partes:

La primera es un videojuego de tipo flappy bird totalmente funcional el cual puede ser jugado por el usuario mediante entradas básicas. Este videojuego puedes ejecutarlo en el siguiente archivo:

```bash mainGame.py ``` 

La segunda parte es el mismo videojuego, pero ahora controlado por una red neuronal evolutiva. Este lo puedes ejecutar en el siguiente archivo:

```bash mainNN.py ``` 

## Funcionamiento del Videojuego

El videojuego tipo flappy bird funciona a partir de la librería pygame, la cual nos permite crear videojuegos sencillos utilizando el lenguaje de programación python

## Funcionamiento de la red neuronal
Nuestra red neuronal funciona a partir de la librería tensor flow. Para poder entrenarlo utilizamos el proceso de evolución, en donde varios candidatos con pesos aleatorios son puestos a jugar para al final seleccionar al mejor, mutar sus pesos y repetir el proceso hasta encontrar al mejor modelo.
