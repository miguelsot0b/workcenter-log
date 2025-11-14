from download_plex import download_from_plex
from upload_to_drive import upload_to_google_drive
import os
import json
import base64

def main():
    """
    Script principal que descarga de Plex y sube a Google Drive
    """
    print('=== Iniciando proceso de descarga y subida ===\n')
    
    # Obtener credenciales de variables de entorno (para Render)
    USERNAME = os.environ.get('PLEX_USERNAME')
    PASSWORD = os.environ.get('PLEX_PASSWORD')
    GOOGLE_SERVICE_ACCOUNT_BASE64 = os.environ.get('GOOGLE_SERVICE_ACCOUNT_BASE64')
    
    # Si no están en variables de entorno, intentar usar config.py (para desarrollo local)
    if not USERNAME or not PASSWORD:
        try:
            from config import USERNAME, PASSWORD
            print('Usando credenciales de config.py (desarrollo local)')
        except ImportError:
            print('ERROR: No se encontraron credenciales')
            print('Define las variables de entorno: PLEX_USERNAME, PLEX_PASSWORD')
            return
    
    # Si hay JSON de cuenta de servicio en base64, decodificarlo y guardarlo
    if GOOGLE_SERVICE_ACCOUNT_BASE64:
        print('Decodificando cuenta de servicio desde base64...')
        try:
            json_content = base64.b64decode(GOOGLE_SERVICE_ACCOUNT_BASE64).decode('utf-8')
            with open('wlog-henniges-33bd4d15bfe8.json', 'w') as f:
                f.write(json_content)
            print('✓ Archivo de cuenta de servicio creado')
        except Exception as e:
            print(f'ERROR al decodificar base64: {e}')
            return
    
    # Paso 1: Descargar archivo de Plex
    print('Paso 1: Descargando archivo de Plex Cloud...')
    try:
        download_from_plex(USERNAME, PASSWORD)
        print('✓ Descarga completada\n')
    except Exception as e:
        print(f'✗ Error en la descarga: {e}')
        return
    
    # Paso 2: Subir archivo a Google Drive
    print('Paso 2: Subiendo archivo a Google Drive...')
    success = upload_to_google_drive()
    
    if success:
        print('\n=== Proceso completado exitosamente ===')
    else:
        print('\n=== Proceso completado con errores ===')

if __name__ == '__main__':
    main()
