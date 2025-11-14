from playwright.sync_api import sync_playwright
import os
from pathlib import Path

def download_from_plex(username, password):
    # Crear directorio de descargas si no existe
    download_path = Path(__file__).parent / 'downloads'
    download_path.mkdir(exist_ok=True)
    
    with sync_playwright() as p:
        # Lanzar navegador en modo headless para Render
        browser = p.chromium.launch(
            headless=True,  # Siempre headless en producción
            args=['--no-sandbox', '--disable-setuid-sandbox']  # Necesario para Docker
        )
        
        context = browser.new_context(
            accept_downloads=True
        )
        
        page = context.new_page()
        
        try:
            print('Navegando a Plex Cloud...')
            page.goto('https://cloud.plex.com/')
            
            # Esperar a que la página cargue
            page.wait_for_load_state('networkidle')
            
            print('Haciendo clic en IAM Login...')
            # Hacer clic en el botón IAM Login
            page.click('#iamButton')
            page.wait_for_load_state('networkidle')
            
            print('Ingresando credenciales...')
            # Ingresar username
            page.fill('#inputUsername3', username)
            page.keyboard.press('Enter')
            
            # Esperar un momento para que procese el username
            page.wait_for_timeout(1000)
            
            # Ingresar password
            page.fill('#inputPassword3', password)
            page.keyboard.press('Enter')
            
            # Esperar a que inicie sesión
            print('Esperando autenticación...')
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            print('Sesión iniciada. Navegando a Workcenter Log...')
            # Navegar a la página de Workcenter Log
            page.goto('https://cloud.plex.com/ProductionTracking/WorkcenterLog')
            page.wait_for_load_state('networkidle')
            page.wait_for_timeout(2000)
            
            print('Abriendo calendario...')
            # Hacer clic en el icono del calendario
            page.click('#autoID43_Anchor')
            page.wait_for_timeout(1000)
            
            print('Seleccionando "Last 7 Days"...')
            # Seleccionar "Last 7 Days" en el dropdown
            page.select_option('#DateRangePickerRangeSelect', 'plex.dates.DateRange.LastSevenDays')
            page.wait_for_timeout(500)
            
            print('Confirmando selección de fecha...')
            # Hacer clic en el botón Ok
            page.click('button.plex-datetimepicker-button:has-text("Ok")')
            page.wait_for_timeout(1000)
            
            print('Realizando búsqueda...')
            # Hacer clic en el botón Search
            page.click('button:has-text("Search")')
            
            print('Esperando resultados (esto puede tomar 2-5 minutos)...')
            # Esperar a que aparezca la primera fila de resultados
            page.wait_for_selector('tr.plex-grid-row[data-index="0"]', timeout=300000)  # 5 minutos de timeout
            
            print('Resultados cargados exitosamente!')
            page.wait_for_timeout(2000)
            
            print('Haciendo clic en "Export As"...')
            # Hacer clic en el botón "Export As"
            page.click('a:has-text("Export As")')
            page.wait_for_timeout(1000)
            
            print('Seleccionando "Export to CSV"...')
            # Hacer clic en "Export to CSV"
            page.click('a#autoID59:has-text("Export to CSV")')
            
            print('Esperando descarga del archivo CSV (esto puede tomar hasta 5 minutos)...')
            # Esperar por la descarga con timeout de 5 minutos
            with page.expect_download(timeout=300000) as download_info:  # 5 minutos de timeout
                pass
            
            download = download_info.value
            
            print(f'Descargando: {download.suggested_filename}')
            
            # Guardar el archivo con el nombre personalizado
            file_path = download_path / 'workcenter-log.csv'
            download.save_as(file_path)
            
            print(f'Archivo descargado exitosamente en: {file_path}')
            
        except Exception as error:
            print(f'Error durante la descarga: {error}')
        
        finally:
            # Esperar un momento antes de cerrar
            page.wait_for_timeout(2000)
            browser.close()

if __name__ == '__main__':
    # Opción 1: Usar archivo de configuración
    try:
        from config import USERNAME, PASSWORD
    except ImportError:
        # Opción 2: Ingresar directamente aquí
        USERNAME = 'tu_usuario'  # Cambia esto por tu usuario
        PASSWORD = 'tu_password'  # Cambia esto por tu contraseña
    
    download_from_plex(USERNAME, PASSWORD)
