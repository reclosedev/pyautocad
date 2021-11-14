from pyautocad import Autocad

# Conéctese automáticamente a cad, siempre que cad esté abierto, se cr
# Si no se ha abierto cad en este momento, se creará un nuevo archivo 
acad = Autocad(create_if_not_exists=True)
# acad.prompt () se usa para imprimir texto en la consola cad 
acad.prompt("Hello, Autocad from Python")
# acad.doc.Name almacena el nombre del cad abierto recientemente
print (acad.doc.Name)


# Importar la clase APoint es muy necesario. El dibujo se realiza por 
# Donde 10 representa la coordenada x del punto y 30 representa la coo
from pyautocad import APoint
import math

p1=(0,0)
p2=(10,0)
# Dibuja una línea recta, p1 es el primer punto de la línea, p2 es el 
acad.model.AddLine(p1,p2)

# Agregue texto, el primer parámetro es la cadena de texto agregada, e
text = acad.model.AddText("{0}".format(text), p, 15)
# Texto movido de p1 a p2
text.move(p1, p2)

# Dibuje un círculo. El primer parámetro p es el punto envuelto por la
acad.model.AddCircle(p, 10)

# Dibuje un arco. El primer parámetro es el punto en el que se dibuja 
acad.model.AddArc(p, radius, math.radians(90), math.radians(270))

# Guarde el mapa cad en la ubicación especificada, ¡el primer parámetr
# Algunos pueden generar dibujos, todos son formatos de tipo de archiv
acad.doc.SaveAs("{0}".format(save_path), 64)
