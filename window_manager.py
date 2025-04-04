from app import ConsoleApp

class WindowManager:
    _instance = None  # Singleton instance

    def __init__(self):
        if WindowManager._instance is not None:
            raise Exception("WindowManager já foi inicializado!")
        self.app = None
        WindowManager._instance = self

    @staticmethod
    def get_instance():
        if WindowManager._instance is None:
            WindowManager()
        return WindowManager._instance

    def initialize(self, tray_icon):
        # Inicializa a instância do ConsoleApp
        self.app = ConsoleApp(tray_icon)

    def show_window(self):
        if self.app:
            self.app.show_window()

    def hide_window(self):
        if self.app:
            self.app.hide_window()


# Funções globais para controle da janela
def show_window():
    WindowManager.get_instance().show_window()

def hide_window():
    WindowManager.get_instance().hide_window()
