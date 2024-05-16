import matplotlib.pyplot as plt 
import numpy as np

t = np.linspace(0, 5, 10)
r = t**2
e = np.linspace(2, 6, 9)
w = e**2
p = np.linspace(2, 6, 9)
o = e**2

x = ['Positivo', 'Neutro', 'Negativo']
y = [6, 3, 1]
colors = ['green', 'yellow', 'red']


"""
plt.subplot(2,2,1)
plt.bar(x,y, color=colors)
plt.subplot(2,2,2)
plt.plot(t,r)
plt.subplot(2,2,3)
plt.plot(e, w, 'r')
plt.subplot(2,2,4)
plt.plot(p, o, 'g')
plt.show()
"""

"""
fig = plt.figure()   # Creamos una figura (canvas vacío) 
axes = fig.add_axes([0.1,0.1,0.5,0.9])   #  Añadimos los ejes
axes.bar(x,y, color=colors)     # 'b' hace referencia al color azul (blue)
plt.show()
"""
fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
axes.bar(x,y, color=colors)
axes.set_xlabel('Tipo de comentario')
axes.set_ylabel('Cantidad de comentarios')

#axes[1].plot(t,r, 'b')
plt.show()
