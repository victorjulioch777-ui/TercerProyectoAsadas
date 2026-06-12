# Este archivo es el punto de entrada del sistema.
# Se encarga de mostrar el menu principal y de llamar a las funciones correspondientes.
from ui.menu_local import mostrar_menu_local
from server.server import iniciar_servidor
from client.cliente import iniciar_cliente

def main():
    """
    Se encarga de mostrar el menu principal y de llamar a las funciones correspondientes.
    """
    while True:
        print("\n==== SISTEMA DISTRIBUIDO DE ASADAS ===")
        print("1. Sistema local")
        print("2. Iniciar servidor")
        print("3. Iniciar cliente")
        print("4. Salir")
        
        opcion = input("Seleccione una opcion: ").strip()
        
        if opcion == "1":
            mostrar_menu_local()
        elif opcion == "2":
            iniciar_servidor()
        elif opcion == "3":
            iniciar_cliente()
        elif opcion == "4":
            print("Saliendo del sistema...")
            break
        else:
            print("Opcion invalida.")
            
if __name__ == "__main__":
    main()