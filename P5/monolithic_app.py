import time

def fA(dataA):
    print("[fA] Recibiendo:", dataA)
    time.sleep(5)  # Simula un proceso pesado
    return dataA + "A"

def fB(dataB):
    print("[fB] Recibiendo:", dataB)
    time.sleep(3)  # Simula un proceso pesado
    return dataB + "B"

def fC(dataC):
    print("[fC] Recibiendo:", dataC)
    time.sleep(4)  # Simula un proceso pesado
    return dataC + "C"

def monolithic_app():
    w = "Inicio:"
    print("Comienzo de la ejecución monolítica con w =", w)
    
    x = fA(w)
    y = fB(x)
    z = fC(y)
    
    print("Resultado final del flujo monolítico:", z)

if __name__ == "__main__":
    monolithic_app()
