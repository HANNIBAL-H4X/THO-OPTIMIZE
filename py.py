import flet as ft
import os
import subprocess
from pathlib import Path
import webbrowser
from datetime import datetime
import psutil
import shutil
import sys
import ctypes
import time
import traceback

try:
    import win32security
    import win32api
    import win32con
    HAVE_WIN32 = True
except ImportError:
    HAVE_WIN32 = False
    print("Advertencia: Módulos win32 no encontrados. Instalando dependencias...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pywin32"], check=True)
    print("Por favor, reinicie la aplicación.")
    sys.exit(1)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def main(page: ft.Page):

    page.title = "PANEL OPTIMIZACION TODO HACK OFFICIAL BY : HANNIBAL THO"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.window_width = 1280
    page.window_height = 890
    page.window_resizable = False
    page.bgcolor = "#000000"  
    page.window_opacity = 0.95
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_maximizable = False
    page.window_minimizable = True
    page.scroll = "auto"
    
    page.window_icon = "assets/icon.ico"
    
    VERDE_LIMA = "#32CD32"
    NEGRO = "#000000"

    def get_text_style(size=18):
        return ft.TextStyle(
            size=size,
            weight=ft.FontWeight.W_500,
            color=VERDE_LIMA,
            font_family="Consolas"
        )

    console = ft.TextField(
        multiline=True,
        read_only=True,
        value="=== CONSOLA ===\n",
        text_size=14,
        height=400,  
        bgcolor="#200000",
        border_color=NEGRO,
        text_style=ft.TextStyle(
            color=VERDE_LIMA,
            font_family="Consolas"
        )
    )

    def log_to_console(message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        console.value = f"{console.value}[{timestamp}] {message}\n"
        console.scroll_to = len(console.value)
        page.update()

    def execute_reg(file_path):
        try:
            subprocess.run(["regedit", "/s", file_path], check=True)
            log_to_console(f"✅ Registro aplicado correctamente")
            show_snackbar("Operación exitosa")
        except Exception as e:
            log_to_console(f"❌ Error al aplicar registro")
            show_snackbar("Error en la operación", is_error=True)

    def execute_bat(file_path):
        try:
            subprocess.run([file_path], shell=True, check=True)
            log_to_console(f"✅ Script ejecutado correctamente")
            show_snackbar("Operación exitosa")
        except Exception as e:
            log_to_console(f"❌ Error al ejecutar script")
            show_snackbar("Error en la operación", is_error=True)

    def open_discord(_):
        webbrowser.open("https://discord.gg/4svwzsy3UP")
        log_to_console("🔗 Abriendo enlace de Discord")

    def show_snackbar(message, is_error=False):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=ft.Colors.RED_400 if is_error else ft.Colors.GREEN_400  
        )
        page.snack_bar.open = True
        page.update()

    def take_ownership(path):
        try:

            username = win32api.GetUserName()
            user_sid = win32security.LookupAccountName(None, username)[0]
            
            sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
            
            sd.SetSecurityDescriptorOwner(user_sid, True)
            win32security.SetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION, sd)
            
            dacl = win32security.ACL()
            dacl.AddAccessAllowedAce(win32security.ACL_REVISION, win32con.GENERIC_ALL, user_sid)
            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION, sd)
            
            return True
        except:
            return False

    def kill_blocking_processes():
        try:

            blocking_processes = [
                "SearchUI.exe", "SearchIndexer.exe", "RuntimeBroker.exe",
                "backgroundTaskHost.exe", "smartscreen.exe", "dllhost.exe",
                "compattelrunner.exe", "sihost.exe", "ctfmon.exe"
            ]
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] in blocking_processes:
                        proc.kill()
                except:
                    continue
            
            return True
        except:
            return False

    def clean_temp_files():
        try:

            kill_blocking_processes()
            
            services_to_stop = [
                'wuauserv', 'bits', 'dosvc', 'DiagTrack', 'Windows Search',
                'superfetch', 'sysmain'
            ]
            
            for service in services_to_stop:
                try:
                    subprocess.run(f'net stop "{service}" /y', shell=True, capture_output=True)
                except:
                    pass

            temp_paths = [
                os.environ.get('TEMP'),
                os.environ.get('TMP'),
                os.path.join(os.environ.get('WINDIR'), 'Temp'),
                os.path.join(os.environ.get('WINDIR'), 'Prefetch'),
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft\\Windows\\Explorer\\IconCacheToDelete'),
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft\\Windows\\INetCache'),
                os.path.join(os.environ.get('LOCALAPPDATA'), 'Microsoft\\Windows\\WebCache')
            ]

            total_cleaned = 0
            files_cleaned = 0
            
            for path in temp_paths:
                if path and os.path.exists(path):
                    try:

                        take_ownership(path)
                        
                        before_size = sum(
                            os.path.getsize(os.path.join(path, f)) 
                            for f in os.listdir(path) 
                            if os.path.isfile(os.path.join(path, f))
                        )
                    except:
                        before_size = 0

                    log_to_console(f"📁 Limpiando: {path}")
                    
                    for filename in os.listdir(path):
                        file_path = os.path.join(path, filename)
                        try:
                            if os.path.exists(file_path):

                                take_ownership(file_path)
                                
                                if os.path.isfile(file_path):
                                    try:

                                        os.chmod(file_path, 0o777)
                                        os.unlink(file_path)
                                    except:
                                        try:
                                            win32api.DeleteFile(file_path)
                                        except:
                                            pass
                                elif os.path.isdir(file_path):
                                    shutil.rmtree(file_path, ignore_errors=True)
                                
                                files_cleaned += 1
                        except Exception as e:
                            if "being used by another process" not in str(e):
                                log_to_console(f"⚠️ No se pudo eliminar: {filename}")

                    try:
                        after_size = sum(
                            os.path.getsize(os.path.join(path, f)) 
                            for f in os.listdir(path) 
                            if os.path.isfile(os.path.join(path, f))
                        )
                        cleaned = (before_size - after_size) / (1024 * 1024) 
                        total_cleaned += cleaned
                    except:
                        pass

            try:
                subprocess.run('ipconfig /flushdns', shell=True, capture_output=True)
                log_to_console("🌐 Cache DNS limpiado")
            except:
                pass

            for service in services_to_stop:
                try:
                    subprocess.run(f'net start "{service}"', shell=True, capture_output=True)
                except:
                    pass

            log_to_console(f"✨ Limpieza completada!")
            log_to_console(f"📊 Archivos procesados: {files_cleaned}")
            log_to_console(f"💾 Espacio liberado: {total_cleaned:.2f} MB")
            show_snackbar("Limpieza completada exitosamente")
        except Exception as e:
            log_to_console(f"❌ Error: {str(e)}")
            log_to_console(f"📝 Detalles: {traceback.format_exc()}")

    def get_button_style():
        return ft.ButtonStyle(
            color=VERDE_LIMA,
            bgcolor=NEGRO,
            padding=15,
            animation_duration=300,
            overlay_color=ft.Colors.RED_900,  
            shadow_color=VERDE_LIMA
        )

    def create_section(title, buttons):
        return ft.Column(
            controls=[
                ft.Text(title, style=get_text_style(20)),  
                ft.Row(
                    [ft.ElevatedButton(
                        text,
                        style=get_button_style(),
                        on_click=callback,
                        width=180,  
                    ) for text, callback in buttons],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,  
                    wrap=True,  
                )
            ],
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    content = ft.Column(
        controls=[

            ft.Container(
                content=ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.COMPUTER, color=VERDE_LIMA, size=40),  
                                ft.Text(
                                    "PANEL OPTIMIZACION TODO HACK OFFICIAL BY: HANNIBAL THO",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=VERDE_LIMA,
                                    font_family="Consolas"
                                ),
                            ]
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DISCORD,  
                            icon_color=VERDE_LIMA,
                            icon_size=32,
                            tooltip="Unirse al Discord",
                            on_click=open_discord
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                border=ft.border.all(2, VERDE_LIMA),
                border_radius=10,
                padding=10,
            ),

            ft.Row(
                [

                    ft.Container(
                        content=ft.Column(
                            [
                            
                                create_section("🚀 Optimización CPU", [
                                    ("Prioridad Juegos", lambda _: execute_reg(r"Recursos\cpu\a.reg")),
                                    ("Prioridad Windows", lambda _: execute_reg(r"Recursos\cpu\b.reg")),
                                    ("Revertir Cambios", lambda _: execute_reg(r"Recursos\cpu\c.reg")),
                                    ("Power Mode", lambda _: execute_bat(r"Recursos\pde_cpu\a.bat")),
                                ]),
                                create_section("🔧 Servicios", [
                                    ("Optimizar Servicios", lambda _: execute_reg(r"Recursos\svco\a.reg")),
                                    ("Revertir Cambios", lambda _: execute_reg(r"Recursos\svco\b.reg")),
                                ]),
                                create_section("📊 Telemetría", [
                                    ("Deshabilitar Telemetría", lambda _: execute_reg(r"Recursos\telemetria\a.reg")),
                                    ("Revertir Cambios", lambda _: execute_reg(r"Recursos\telemetria\b.reg")),
                                ]),
                                create_section("🎮 Modo Gaming", [
                                    ("Activar Modo Gaming", lambda _: execute_reg(r"Recursos\gaming\a.reg")),
                                ]),
                                create_section("🖥️ Optimización GPU", [
                                    ("Optimizar GPU", lambda _: execute_reg(r"Recursos\gpu\a.reg")),
                                ]),
                                create_section("💾 Optimización RAM", [
                                    ("Deshabilitar Compresión", lambda _: execute_bat(r"Recursos\ram\a.cmd")),
                                    ("Revertir Cambios", lambda _: execute_bat(r"Recursos\ram\b.bat")),
                                ]),
                                create_section("💿 Optimización SSD", [
                                    ("Optimizar SSD", lambda _: execute_reg(r"Recursos\ssd\a.reg")),
                                    ("Revertir Cambios", lambda _: execute_reg(r"Recursos\ssd\b.reg")),
                                ]),
                                create_section("📡 Optimización Red", [
                                    ("Optimizar Red", lambda _: execute_bat(r"Recursos\network\a.bat")),
                                    ("Limpiar Cache DNS", lambda _: execute_bat(r"Recursos\network\b.bat")),
                                ]),
                                create_section("🗑️ Limpieza", [
                                    ("Limpiar Archivos Temporales", lambda _: clean_temp_files()),
                                ]),
                            ],
                            scroll=ft.ScrollMode.AUTO,
                            spacing=12,  
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        width=600, 
                        height=700,  
                        border=ft.border.all(2, VERDE_LIMA),
                        border_radius=10,
                        padding=ft.padding.all(20), 
                        margin=ft.margin.all(5),  
                    ),

                    ft.Container(
                        content=console,
                        expand=True,
                        border=ft.border.all(2, VERDE_LIMA),
                        border_radius=10,
                        padding=20,
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.START,
            ),
        ],
        spacing=20,
    )

    page.add(content)
    page.update()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
