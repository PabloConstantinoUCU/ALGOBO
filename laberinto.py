import tkinter as tk
from tkinter import ttk
import heapq
import time

class GrafoConCostos:
    def __init__(self):
        # Diccionario para almacenar las listas de adyacencia con costos
        self.grafo = {}

    def agregar_nodo(self, nodo):
        # Agrega el nodo al grafo si no existe
        if nodo not in self.grafo:
            self.grafo[nodo] = {}

    def agregar_arista(self, nodo1, nodo2, costo):
        # Agrega una arista con costo entre nodo1 y nodo2
        if nodo1 in self.grafo and nodo2 in self.grafo:
            self.grafo[nodo1][nodo2] = costo
            self.grafo[nodo2][nodo1] = costo
        else:
            print(f"Uno o ambos nodos ({nodo1}, {nodo2}) no existen en el grafo.")

    def mostrar_grafo(self):
        # Muestra el grafo
        for nodo in self.grafo:
            for vecino, costo in self.grafo[nodo].items():
                print(f"Arista: ({nodo} - {vecino}), Costo: {costo}")
                
    def set_inicio(self, nodo):
        self.inicio = nodo

    def set_fin(self, nodo):
        self.fin = nodo
                
    def resolver_dijkstra(self, canvas, pixels):
        # Implementación del algoritmo de Dijkstra
        if self.inicio is None or self.fin is None:
            print("No se puede resolver: No se ha definido el inicio o el fin.")
            return None

        # Diccionario para almacenar las distancias más cortas
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[self.inicio] = 0

        # Diccionario para rastrear el camino
        camino = {}
        camino[self.inicio] = None

        # Cola de prioridad para el nodo más cercano
        cola_prioridad = [(0, self.inicio)]

        while cola_prioridad:
            distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
            if nodo_actual != self.inicio and nodo_actual != self.fin:
                x, y = nodo_actual
                canvas.itemconfig(pixels[y][x], fill="yellow")

            if nodo_actual == self.fin:
                break

            for vecino, costo in self.grafo[nodo_actual].items():
                distancia = distancia_actual + costo

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    camino[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (distancia, vecino))
            
            time.sleep(0.001)  # Espera 100 ms

        # Reconstruir el camino desde el fin al inicio
        nodo = self.fin
        ruta = []
        while nodo is not None:
            ruta.append(nodo)
            nodo = camino.get(nodo)
        ruta.reverse()

        return ruta if ruta[0] == self.inicio else None
    
    def resolver_a_star(self):
        # Implementación del algoritmo A*
        if self.inicio is None or self.fin is None:
            print("No se puede resolver: No se ha definido el inicio o el fin.")
            return None

        # Función heurística (distancia de Manhattan)
        def heuristica(nodo1, nodo2):
            x1, y1 = nodo1
            x2, y2 = nodo2
            return abs(x1 - x2) + abs(y1 - y2)

        # Diccionario para almacenar las distancias más cortas
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[self.inicio] = 0

        # Diccionario para rastrear el camino
        camino = {}
        camino[self.inicio] = None

        # Cola de prioridad para el nodo más cercano
        cola_prioridad = [(heuristica(self.inicio, self.fin), self.inicio)]

        # Diccionario para almacenar los costos estimados
        costos_estimados = {nodo: float('inf') for nodo in self.grafo}
        costos_estimados[self.inicio] = heuristica(self.inicio, self.fin)

        while cola_prioridad:
            _, nodo_actual = heapq.heappop(cola_prioridad)

            if nodo_actual == self.fin:
                break

            for vecino, costo in self.grafo[nodo_actual].items():
                distancia = distancias[nodo_actual] + costo

                if distancia < distancias[vecino]:
                    distancias[vecino] = distancia
                    camino[vecino] = nodo_actual
                    costo_estimado = distancia + heuristica(vecino, self.fin)
                    costos_estimados[vecino] = costo_estimado
                    heapq.heappush(cola_prioridad, (costo_estimado, vecino))

        # Reconstruir el camino desde el fin al inicio
        nodo = self.fin
        ruta = []
        while nodo is not None:
            ruta.append(nodo)
            nodo = camino.get(nodo)
        ruta.reverse()

        return ruta if ruta[0] == self.inicio else None

class Aplicacion:
    def __init__(self, root, grid_size=16, pixel_size=20):
        self.root = root
        self.grid_size = grid_size
        self.pixel_size = pixel_size
        self.selected_option = tk.StringVar(value="A")
        self.painted_pixels = set()
        self.paint_color = None
        self.setting_start = False
        self.setting_end = False
        self.start_point = None
        self.end_point = None

        # Frame principal
        self.frame = tk.Frame(root, bg="gray")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Frame superior para los botones de inicio y fin
        self.top_frame = tk.Frame(self.frame, bg="gray")
        self.top_frame.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Botón para definir el inicio
        self.start_button = tk.Button(self.top_frame, text="Set Inicio", command=self.set_start, bg="white", fg="black")
        self.start_button.pack(side=tk.LEFT, padx=10)

        # Botón para definir el fin
        self.end_button = tk.Button(self.top_frame, text="Set Fin", command=self.set_end, bg="white", fg="black")
        self.end_button.pack(side=tk.LEFT, padx=10)

        # Lienzo para dibujar el pixel art
        self.canvas = tk.Canvas(self.frame, width=grid_size*pixel_size, height=grid_size*pixel_size, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=10)

        # Crear la grilla de pixeles
        self.pixels = []
        for y in range(grid_size):
            row = []
            for x in range(grid_size):
                rect = self.canvas.create_rectangle(
                    x*pixel_size, y*pixel_size,
                    (x+1)*pixel_size, (y+1)*pixel_size,
                    fill="white", outline="gray"
                )
                row.append(rect)
            self.pixels.append(row)

        # Conectar la acción del mouse a los eventos de pintar y arrastrar
        self.canvas.bind("<Button-1>", self.start_paint)
        self.canvas.bind("<B1-Motion>", self.paint_pixel_drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_paint)

        # Botón GO!
        self.go_button = tk.Button(self.frame, text="GO!", command=self.go_button_action, bg="black", fg="white")
        self.go_button.grid(row=2, column=0, padx=20, pady=20)

        # Select con opciones "A" y "B"
        self.option_menu = ttk.Combobox(self.frame, textvariable=self.selected_option, values=["Dijkstra", "A*"], state="readonly")
        self.option_menu.grid(row=2, column=1, padx=20, pady=20)

    def set_start(self):
        self.setting_start = True
        self.setting_end = False
        self.start_button.config(bg="lightgreen")
        self.end_button.config(bg="white")

    def set_end(self):
        self.setting_end = True
        self.setting_start = False
        self.end_button.config(bg="lightcoral")
        self.start_button.config(bg="white")

    def start_paint(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            if self.setting_start:
                if self.canvas.itemcget(self.pixels[y][x], "fill") == "white":
                    if self.start_point:
                        self.canvas.itemconfig(self.pixels[self.start_point[1]][self.start_point[0]], fill="white")
                    self.canvas.itemconfig(self.pixels[y][x], fill="green")
                    self.start_point = (x, y)
                    self.setting_start = False
                    self.start_button.config(bg="white")
            elif self.setting_end:
                if self.canvas.itemcget(self.pixels[y][x], "fill") == "white":
                    if self.end_point:
                        self.canvas.itemconfig(self.pixels[self.end_point[1]][self.end_point[0]], fill="white")
                    self.canvas.itemconfig(self.pixels[y][x], fill="red")
                    self.end_point = (x, y)
                    self.setting_end = False
                    self.end_button.config(bg="white")
            else:
                self.painted_pixels.clear()
                self.paint_color = "black" if self.canvas.itemcget(self.pixels[y][x], "fill") == "white" else "white"
                self.paint_pixel(event)

    def paint_pixel(self, event):
        x, y = event.x // self.pixel_size, event.y // self.pixel_size
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            # Evitar pintar sobre el inicio o fin
            if (x, y) == self.start_point or (x, y) == self.end_point:
                return
            if (x, y) not in self.painted_pixels:
                current_color = self.canvas.itemcget(self.pixels[y][x], "fill")
                if current_color != self.paint_color:
                    self.canvas.itemconfig(self.pixels[y][x], fill=self.paint_color)
                    self.painted_pixels.add((x, y))

    def paint_pixel_drag(self, event):
        self.paint_pixel(event)

    def end_paint(self, event):
        self.painted_pixels.clear()

    def go_button_action(self):
        if not self.start_point or not self.end_point:
            print("No se puede correr sin setear inicio y fin")
        else:
            grafo = self.crear_grafo()
            print(grafo)
            print(grafo.resolver_dijkstra(self.canvas, self.pixels))
            print(grafo.resolver_a_star())
            print("Opción seleccionada:", self.selected_option.get())
            print("Punto de inicio:", self.start_point)
            print("Punto de fin:", self.end_point)
            
    def crear_grafo(self):
        # Crear una instancia de GrafoConCostos
        grafo = GrafoConCostos()

        # Añadir los nodos al grafo (solo píxeles no pintados)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.canvas.itemcget(self.pixels[y][x], "fill") != "black":
                    grafo.agregar_nodo((x, y))

        # Añadir las aristas entre nodos adyacentes
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.canvas.itemcget(self.pixels[y][x], "fill") != "black":
                    # Lista de vecinos adyacentes (arriba, abajo, izquierda, derecha)
                    vecinos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                    
                    for vecino in vecinos:
                        vx, vy = vecino
                        # Verificar si el vecino está dentro de los límites y es un nodo no pintado
                        if 0 <= vx < self.grid_size and 0 <= vy < self.grid_size:
                            if self.canvas.itemcget(self.pixels[vy][vx], "fill") != "black":
                                # Añadir la arista con peso 1
                                grafo.agregar_arista((x, y), (vx, vy), 1)

        # Establecer los vértices de inicio y fin en el grafo
        if self.start_point:
            grafo.set_inicio(self.start_point)
        if self.end_point:
            grafo.set_fin(self.end_point)

        # Mostrar el grafo creado en la consola
        grafo.mostrar_grafo()
        
        # Retornar el grafo creado (opcional)
        return grafo

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
