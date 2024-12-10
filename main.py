import tkinter as tk
from cliente.vista_base import FrameBase
from cliente.vista_principal import FramePrincipal


def main():
    
    ventana = tk.Tk()
    ventana.title('Veterinaria')
    ventana.iconbitmap('img/veterinario.ico')
    ventana.resizable(False, False)

    FrameBase.barritaMenu(ventana)
    FramePrincipal(ventana)
    
    ventana.mainloop()
    
if __name__ == '__main__':
    main()
