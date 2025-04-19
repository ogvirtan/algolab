from ui.user_interface import UI
from services.engine import Engine

def main():
    #kayttoliittyma = UI()
    e = Engine()
    e.main_loop()        

if __name__ == "__main__":
    main()