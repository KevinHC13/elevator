# Este programa representa el funcionamiento de un elevador en un edificio de dos pisos. Para esto se utiliza un automata de cuatro estados.
# Creado por:
# - Kevin Alejandro Hernández Campillo
# - Yanel Azucena Mireles Sena
# Github: https://github.com/KevinHC13

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QMouseEvent
from PyQt5.QtCore import Qt, QTimer, QRectF

# Esta clase contiene el objeto elevador, pero no lo dibuja
class Elevator(QWidget):
    def __init__(self):
        super().__init__()
        self.floor = 0  # Inicializar piso en 0
        self.doors_open = False  # Inicializar las puertas como cerradas

    # Función para subir un piso
    def go_up(self):
        if not self.doors_open:
            self.floor += 3
            self.update()
    
    # Función para bajar un piso
    def go_down(self):
        if not self.doors_open and self.floor > 0:
            self.floor -= 3
            self.update()

    # Función para abrir las puertas
    def open_doors(self):
        self.doors_open = True
        self.update()

    # Función para cerrar las puertas
    def close_doors(self):
        self.doors_open = False
        self.update()


# Esta clase representa a un estado del automata
class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.is_start = False
        self.is_final = False
        self.color = Qt.red             # Por defecto todos nodos son rojos
        self.edges = []                 # Contiene los enlaces que conforman el automata

    def __str__(self):
        return "Node" + str(self.name)

# Esta clase representa los enlaces o transiciones de un automata
class Edge:
    def __init__(self, start, end, symbol):
        self.start = start
        self.end = end
        self.symbol = symbol
        self.dibujado = False       # Variable usada para dibujar solamente una vez la transicion

    def __str__(self):
        return "Edge" + str(self.symbol)

# Esta clase representa al automata
class Automata:
    def __init__(self):
        self.nodes = []                 # Lista con nos nodos que conforman el automata
        self.edges = []                 # Lista con las transiciones que conforman el automata
        self.current_node = None        # Esta variable va cambiando de valor para almacenar al nodo actual en cada paso de la animacion

    # Añade un nodo o estado al automata. Para esto resive:
    # name: Nombre del nodo (String)
    # x, y: Posicion del nodo (Int)
    def add_node(self, name, x, y):
        node = Node(name, x, y)
        self.nodes.append(node)
        return node

    # Añade una transicion al automata. Para esto resive:
    # start: Nodo de inicio (Node)
    # end: Nodo final (Node)
    # symbol: simbolo para la transicion (String)
    def add_edge(self, start, end, symbol):
        edge = Edge(start, end, symbol)
        start.edges.append(edge)
        self.edges.append(edge)

# Clase principal que genera el graficado de los elementos y la interfaz
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Elevador')
        self.setGeometry(100, 100, 700, 700)
        self.setFixedSize(700, 700)
        color_hex = "#BBDEFB"
        color = QColor(color_hex)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), color)
        self.setPalette(p)        

        self.automata = Automata()
        self.create_automata()
        self.elevador = Elevator()

        # Timer utilizado para lanzar cada paso de la animacion
        self.timer = QTimer(self)
        self.tiempo = 0
        self.timer.timeout.connect(self.draw_transition)
        
    # Este metodo configura las propiedades del automata
    def create_automata(self):
        # Se insertan los estados necesarios
        d = self.automata.add_node('D', 100, 550)
        c = self.automata.add_node('C', 100, 400)
        b = self.automata.add_node('B', 100, 250)
        a = self.automata.add_node('A', 100, 100)

        # Se establecen los estados finales y el inicial
        c.is_start = True
        self.automata.current_node = c
        c.color = Qt.green
        c.is_final = True
        b.is_final = True

        # Se agregan las transiciones necesarias
        self.automata.add_edge(a, b, '1')
        self.automata.add_edge(b, a, '0')

        self.automata.add_edge(b, c, '1')
        self.automata.add_edge(c, b, '0')

        self.automata.add_edge(c, d, '1')
        self.automata.add_edge(d, c, '0')

    # Detectar el click del mouse
    def mousePressEvent(self, event: QMouseEvent):
        # Solo ejecutar si la animacion ya termino
        if self.tiempo == 0:
            # Detecta el click en el boton del piso 1
            if event.x() >= 485 and event.x() <= 515 and event.y() >= 485 and event.y() <= 515:
                # Dependiendo de donde este el elevador actualmente establece como lista de transiciones una secuenica de pasos a seguir
                if self.automata.current_node == self.automata.nodes[1]:
                    self.transitions = [1,0,0,0,1]
                if self.automata.current_node == self.automata.nodes[2]:
                    self.transitions = [1,1,0,0,0,1]
                self.timer.start(1000)
            # Detecta el click en el boton del piso 2
            # Dependiendo de donde este el elevador actualmente establece como lista de transiciones una secuenica de pasos a seguir
            if event.x() >= 485 and event.x() <= 515 and event.y() >= 185 and event.y() <= 215:
                if self.automata.current_node == self.automata.nodes[1]:
                    self.transitions = [0,0,1,1,1,0]
                if self.automata.current_node == self.automata.nodes[2]:
                    self.transitions = [0,1,1,1,0]
                # Inicia el timer que lanza la animacion
                self.timer.start(1000)
        else:
            print("Aun no termina la animacion")
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)      # Suaviza los trazos generados

        pen = QPen(Qt.black)
        pen.setWidth(2)
        painter.setPen(pen)

        # Dibujar linea que representa el piso
        painter.drawLine(200,300,600,300)
        painter.drawLine(200,600,600,600)
        painter.drawText(210,320 , "Piso 1")
        painter.drawText(210,50 , "Piso 2")

        # Dibujar botones para los pisos
        brush = QBrush(Qt.yellow)
        painter.setBrush(brush)
        painter.drawEllipse(500,500, 15, 15)
        painter.drawEllipse(500,200, 15, 15)


        # Dibujar elevador
        # Pintar las puertas dependiendo de su estado (abierto o cerrado)
        y = 550 - (100 * self.elevador.floor)

        if self.elevador.doors_open:
            painter.setBrush(QBrush(QColor(180, 180, 180)))
            painter.drawRect(QRectF(275, y - 150, 90, 190))
            painter.drawRect(QRectF(385, y - 150, 90, 190))
        else:
            painter.setBrush(QBrush(QColor(80, 80, 80)))
            painter.drawRect(QRectF(275, y - 150, 200, 190))

        
        # Dibuja los estados del automata
        for node in self.automata.nodes:
            brush = QBrush(node.color)
            painter.setBrush(brush)
            
            # Si el nodo esta marcado como final se dibujan dos circulos para representarlo
            if node.is_final:
                painter.drawEllipse(node.x - 20, node.y - 20, 40, 40)
                painter.drawEllipse(node.x - 15, node.y - 15, 30, 30)
            # De lo contrario solo se dibuja un circulo
            else:
                painter.drawEllipse(node.x - 20, node.y - 20, 40, 40)

            # Si el estado esta marcado como inicial se dibuja un indicador al lado del nodo
            if node.is_start:
                brush = QBrush(Qt.green)
                painter.setBrush(brush)
                painter.drawRect(node.x - 60, node.y-6,30,12)
                painter.drawText(node.x - 60, node.y+5, "Start")
            brush = QBrush(Qt.white)
            painter.setBrush(brush)

            # Dibuja el nombre de cada nodo
            painter.drawText(node.x-5, node.y+5, node.name)

        pen = QPen(Qt.black)
        pen.setWidth(1)
        painter.setPen(pen)

        # Dibuja los enlcaes de cada nodo
        for edge in self.automata.edges:
            # Se verifica que el nodo no tenga dobles enlaces
            for i in edge.end.edges:
                # Si se encuentran dobles enlaces se dibujan ambos y se marcan como dibujados
                if edge.start == i.end and not edge.dibujado and not i.dibujado:
                    # Se dibuja el primer enlace
                    edge.dibujado = True
                    x1 = edge.start.x + 5
                    y1 = edge.start.y
                    x2 = edge.end.x  + 5
                    y2 = edge.end.y
                    painter.drawLine(x1, y1+20, x2, y2-20)
                    painter.drawLine(x2, y2-20,x2-5,y2-25)
                    painter.drawLine(x2, y2-20,x2+5,y2-25)
                    x = int((x1 + x2) / 2)
                    y = int((y1 + y2) / 2)
                    painter.drawText(x + 7, y, edge.symbol)
                    
                    # Se dibuja el segundo enlace
                    i.dibujado = True
                    x1 = i.start.x - 5
                    y1 = i.start.y
                    x2 = i.end.x  - 5
                    y2 = i.end.y
                    painter.drawLine(x1, y1-20, x2, y2+20)
                    painter.drawLine(x2, y2+20,x2-5,y2+25)
                    painter.drawLine(x2, y2+20,x2+5,y2+25)
                    x = int((x1 + x2) / 2)
                    y = int((y1 + y2) / 2)
                    painter.drawText(x - 10, y, i.symbol)

            # Si el nodo no tiene dobles enlaces y el enlace no ha sido dibujado se dibuja
            if edge.dibujado == False:
                x1 = edge.start.x
                y1 = edge.start.y
                x2 = edge.end.x
                y2 = edge.end.y
                painter.drawLine(x1, y1+20, x2, y2-20)
                painter.drawLine(x2, y2-20,x2-5,y2-25)
                painter.drawLine(x2, y2-20,x2+5,y2-25)
                x = int((x1 + x2) / 4)
                y = int((y1 + y2) / 4)
                painter.drawText(x - 5, y, edge.symbol)
        
        # Al final se marcan todos los enlaces como no dibujados para dibujarlos de nuevo en la siguiente actualizacion
        for edge in self.automata.edges:
            edge.dibujado = False

        # Se reinicia el color de todos los nodos a rojo para borrar el color del anterior nodo verde
        for node in self.automata.nodes:
            node.color = Qt.red
            
    # Metodo utilizado para generar la animacion
    def draw_transition(self):
        # Solamente se ejecuta mientras aun no se hallan dibujado todos los elementos en la lista de transiciones
        if len(self.transitions) > self.tiempo:
            # Se verifica que el simbolo pasado exista en el nodo actual
            for edge in self.automata.current_node.edges:
                if int(edge.symbol) == self.transitions[self.tiempo] and edge.start == self.automata.current_node:
                    # Si existe el enlace entonces se ejecuta el metodo para modificar el estado del elevador al estado que corresponda segun el simbolo que resiva
                    # Para esto se verifica cada nodo y cada enlace que este contenga
                    if self.automata.current_node == self.automata.nodes[0]:
                        if int(edge.symbol) == 0:
                            self.elevador.close_doors()
                    elif self.automata.current_node == self.automata.nodes[1]:
                        if int(edge.symbol) == 1:
                            self.elevador.open_doors()
                        if int(edge.symbol) == 0:
                            self.elevador.go_up()
                    elif self.automata.current_node == self.automata.nodes[2]:
                        if int(edge.symbol) == 1:
                            self.elevador.go_down()
                        if int(edge.symbol) == 0:
                            self.elevador.open_doors()
                    elif self.automata.current_node == self.automata.nodes[3]:
                        if int(edge.symbol) == 1:
                            self.elevador.close_doors()

                    # Se establece como nodo actual el nodo final de la transicion
                    self.automata.current_node = edge.end
                    # Se pinta este nodo como verde
                    edge.end.color = Qt.green
                    # Se actualiza el lienzo
                    self.update()           
            # Se incrementa en 1 el tiempo para avanzar en la animacion            
            self.tiempo += 1
        else:
            # Cuando terminen de recorrerse todas las transiciones pasadas entonces se para el timer y se reinicia la variable tiempo
            self.timer.stop()
            self.tiempo = 0

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
