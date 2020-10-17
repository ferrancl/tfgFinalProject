from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import PhotoImage
from tkinter import Canvas
from tkinter import NW
from tkinter import Menu
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
from math import sqrt
import tkinter as tk

mode = 'inicio'
lista_puntos_escala = []
lista_puntos_particula=[]
lista_dibujos = []
lista_dibujos_contorno = []
pixels_barra = 1
unidad_escala = 'μm'
medida_escala = 1
n=0
particulas = ''
centro_x = None
centro_y = None
particulas = ''

def guardar_archivo_texto():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:
        return
    f.write(particulas)
    f.close()


def dibujar_escala():
    global mode, medida_escala, unidad_escala
    mode = 'escala'
    messagebox.showinfo('Mensaje', 'Dibuje 2 puntos para determinar la escala')


def dibujar_contornos():
    global mode, pixels_barra
    if pixels_barra == 1:
        messagebox.showerror('Error', 'Error: Primero determine una escala')
    if pixels_barra > 1:
        mode = 'contorno'
        messagebox.showinfo('Mensaje', 'Dibuje 3 puntos para determinar el contorno de una partícula')

def dibujar(event):
    global mode, lista_puntos_escala, lista_puntos_particula, pixels_barra, n, lista_diametro_particulas, centro_x, centro_y, particulas, medida_escala, unidad_escala, lista_dibujos, particulas, lista_dibujos_contorno, etiqueta_particula
    pt = (event.x, event.y)
    if mode == 'escala':
        if len(lista_puntos_escala)<2:
            dibujo_punto = canvas.create_oval(event.x - 1, event.y - 1, event.x + 1, event.y + 1, outline = 'blue', fill = 'blue')
            lista_puntos_escala.append(pt)
            lista_dibujos.append(dibujo_punto)
            if len(lista_puntos_escala) == 2:
                #print('Dibujar escala')
                dibujo_escala = canvas.create_line(lista_puntos_escala[0][0], lista_puntos_escala[0][1], event.x, lista_puntos_escala[0][1], fill='blue')
                lista_dibujos.append(dibujo_escala)
                pixels_barra = abs(lista_puntos_escala[0][0] - event.x)
                messagebox.showinfo('Escala', 'Escala fijada correctamente')

    if mode == 'contorno':
        if pixels_barra > 1:
            Helvfont = font.Font(family="Helvetica", size=7, weight="bold")
            dibujo_punto_contorno = canvas.create_oval(event.x - 2, event.y - 2, event.x + 2, event.y + 2, outline ='red' ,fill = 'red')
            lista_dibujos_contorno.append(dibujo_punto_contorno)
            lista_puntos_particula.append(pt)
            if len(lista_puntos_particula) == 3:
                n=n+1
                x1=lista_puntos_particula[0][0]
                y1=lista_puntos_particula[0][1]
                x2=lista_puntos_particula[1][0]
                y2=lista_puntos_particula[1][1]
                x3=lista_puntos_particula[2][0]
                y3=lista_puntos_particula[2][1]
                #Ponemos esta condición para asegurarnos que ma y mb tienen un valor definido
                if x2-x1 == 0 or x3-x2 == 0 or y2-y1 == 0 or y3-y2 == 0:
                    lista_puntos_particula = []
                    for punto in lista_dibujos_contorno:
                        canvas.delete(punto)
                    lista_dibujos_contorno = []
                    n=n-1
                    messagebox.showerror('Mensaje', 'La coordenada x o la coordenada y de 2 puntos no puede ser la misma. Vuelva a marcar 3 puntos distintos.')
                else:
                    ma=(y2-y1)/(x2-x1)
                    mb=(y3-y2)/(x3-x2)
                    centro_x = (ma*mb*(y1-y3)+mb*(x1+x2)-ma*(x2+x3))/(2*(mb-ma))
                    centro_y = (-1/ma)*(centro_x-(x1+x2)/2)+(y1+y2)/2
                    centro = (int(round(centro_x, 0)), int(round(centro_y,0)))
                    rad = sqrt(pow(x1 - centro_x, 2) + pow(y1 - centro_y, 2))
                    dibujo_contorno = canvas.create_oval(centro[0] - int(round(rad,0)),centro[1] - int(round(rad,0)), centro[0]+ int(round(rad,0)), centro[1] + int(round(rad,0)), outline='red' , width = 2)
                    lista_dibujos_contorno.append(dibujo_contorno)
                    #lista_diametro_particulas.append(2*rad)
                    etiqueta_particula = Label(ventana, text= str(n), font=Helvfont)
                    etiqueta_particula.place(x = centro[0] - 1 ,y = centro[1] - 1, height=6, width=6)
                    particulas=particulas + 'Particula' + str(n) + ' ' + str(2*rad*medida_escala/(pixels_barra)) + ' ' + unidad_escala + '\n'
            if len(lista_puntos_particula) > 3:
                lista_puntos_particula = lista_puntos_particula[len(lista_puntos_particula)-1:]
                lista_dibujos_contorno = lista_dibujos_contorno[len(lista_dibujos_contorno)-1:]
        if pixels_barra == 1:
            messagebox.showerror('Error', 'Error: Primero determine una escala')

def deshacer():
    global lista_dibujos, lista_puntos_escala, mode, lista_dibujos_contorno, lista_puntos_particula, pixels_barra, n, etiqueta_particula, particulas
    if mode == 'escala':
        if len(lista_puntos_escala) == 0:
            messagebox.showinfo('Mensaje', 'No hay elementos de la escala que deshacer')
        if len(lista_puntos_escala) == 1:
            canvas.delete(lista_dibujos[len(lista_dibujos)-1])
            lista_dibujos = []
            lista_puntos_escala = []
        if len(lista_puntos_escala) == 2:
            lista_puntos_escala = lista_puntos_escala[:len(lista_puntos_escala)-1]
            canvas.delete(lista_dibujos[len(lista_dibujos)-1])
            canvas.delete(lista_dibujos[len(lista_dibujos)-2])
            lista_dibujos = lista_dibujos[:1]
            pixels_barra = 1

    if mode == 'contorno':
        if len(lista_puntos_particula) == 0:
            messagebox.showerror('Mensaje', 'No hay elementos del contorno de la partícula que deshacer')
        if 0 < len(lista_puntos_particula) < 3:
            lista_puntos_particula = lista_puntos_particula[:len(lista_puntos_particula)-1]
            canvas.delete(lista_dibujos_contorno[len(lista_dibujos_contorno)-1])
            lista_dibujos_contorno = lista_dibujos_contorno[:len(lista_dibujos_contorno)-1]
        if len(lista_puntos_particula) == 3:
            lista_puntos_particula = lista_puntos_particula[:len(lista_puntos_particula)-1]
            canvas.delete(lista_dibujos_contorno[len(lista_dibujos_contorno)-1])
            canvas.delete(lista_dibujos_contorno[len(lista_dibujos_contorno)-2])
            lista_dibujos_contorno = lista_dibujos_contorno[:len(lista_dibujos_contorno)-2]
            n=n-1
            etiqueta_particula.destroy()
            variable = particulas.splitlines()
            variable = variable[:len(variable)-1]
            p = ''
            for linia in variable:
                p = p + linia + '\n'
            particulas = p

def redimensionar(imagen_original):
    o_size = imagen_original.size   #Tamaño original de la imagen
    f_size = (800, 800)
    factor = min(float(f_size[1])/o_size[1], float(f_size[0])/o_size[0])
    width = int(o_size[0] * factor)
    height = int(o_size[1] * factor)
    return (imagen_original.resize((width, height), Image.ANTIALIAS))

def salir_programa():
    if messagebox.askyesno(title='Confirmación', message = '¿Seguro que desea salir del programa?') == True:
        ventana.destroy()
    else:
        pass

def abrir():
    global imagenL
    ventana.filename=filedialog.askopenfilename()
    ruta=ventana.filename
    imagen = Image.open(ruta)
    imagenL = ImageTk.PhotoImage(redimensionar(imagen))
    canvas.create_image(0,0,anchor=NW,image=imagenL)
    Titulo.destroy()
    esfera_foto.destroy()
    ordenador_foto.destroy()


def menu_ayuda():
    messagebox.showinfo('Intrucciones', '1.Abrir la imagen que contiene las partículas que se quieren medir.\n2.Determinar la escala dibujándola sobre la imagen.\n3.Medir cada una de las partículas a partir de 3 puntos de su contorno (cada punto se marca con un clic izquierdo de ratón).\n4.Una vez medidas todas las partículas, generar el fichero de datos (extensión .txt) que contiene el diámetro de las partículas medidas.\nNOTA: el programa permite la acción de deshacer de la partícula que se está midiendo en ese preciso instante, es decir, en el momento en el que se empiece a medir una nueva partícula (marcando uno de los puntos del contorno), no se podrá deshacer la medición de la partícula anterior.')


ventana =tk.Tk()
ventana.geometry("800x800+0+0")
ventana.title("Sphereasy")

#Creas tu canvas y lo posicionas en tu ventana
canvas = Canvas (ventana, height=800, width=800)
canvas.pack()

courierfont = font.Font(family="Courier", size=80, weight="bold")
Titulo = Label(ventana, text = 'SPHEREASY', font=courierfont )
Titulo.place(x=150, y=130, height= 70, width = 500)
esfera = PhotoImage(file = 'Sphere_rotating.gif')
esfera_foto = Label(ventana, image = esfera)
esfera_foto.place(x=135, y=280)
ordenador = PhotoImage(file = 'ordenador.gif')
ordenador_foto = Label(ventana, image = ordenador)
ordenador_foto.place(x=380, y=265)

# Variable global que va a contener la imagen
imagenL = None
barraMenu=Menu(ventana)

#crear los menús ..............................................................
mnuArchivo=Menu(barraMenu)
mnuEdicion=Menu(barraMenu)
mnuEscala=Menu(barraMenu)
mnuDibujar=Menu(barraMenu)
mnuDatos=Menu(barraMenu)
mnuAyuda=Menu(barraMenu)

#crear los comandos de los menús................................................
mnuArchivo.add_command(label="Abrir",command = abrir)
mnuArchivo.add_separator()
mnuArchivo.add_command(label="Salir",command= salir_programa)

mnuEdicion.add_command(label = "Deshacer", command = deshacer)

mnuEscala.add_command(label = "Dibujar escala", command = dibujar_escala)

mnuDibujar.add_command(label = "Contorno partícula a partir de 3 puntos", command= dibujar_contornos)

mnuDatos.add_command(label = 'Generar fichero de datos', command = guardar_archivo_texto)

mnuAyuda.add_command(label = 'Instrucciones de uso del programa', command = menu_ayuda)

barraMenu.add_cascade(label="Archivo",menu=mnuArchivo)
barraMenu.add_cascade(label="Edición",menu=mnuEdicion)
barraMenu.add_cascade(label="Escala",menu=mnuEscala)
barraMenu.add_cascade(label="Dibujar",menu=mnuDibujar)
barraMenu.add_cascade(label="Datos",menu=mnuDatos)
barraMenu.add_cascade(label="Ayuda", menu = mnuAyuda)
ventana.config(menu=barraMenu)


def obtener():
    global valor, medida_escala, unidad_escala
    medida_escala = valor.get()
    unidad_escala = unidad.get()
    messagebox.showinfo('Escala', 'Escala fijada a' + ' ' + str(valor.get()) + ' ' + unidad.get())
valor=IntVar(value=1)
unidad=StringVar(value = 'mm')
titulo1= Label(ventana, text='Longitud').place(x=20, y=658)
spin1= Spinbox(ventana, from_=1, to = 1000, textvariable = valor, width = 4).place(x=87, y=655)
titulo2= Label(ventana, text='Unidad').place (x=200, y=658)
spin2= Spinbox(ventana, values=('mm', 'μm', 'nm', 'pm'), textvariable = unidad, width = 4).place(x=260, y=655)
boton= Button(ventana, text= 'Aceptar', command= obtener).place(x=380, y=655)

canvas.bind("<Button-1>", dibujar)

ventana.mainloop()
