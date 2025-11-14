from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import os
from pathlib import Path

def upload_to_google_drive():
    """
    Sube el archivo workcenter-log.csv a Google Drive sobrescribiendo el archivo existente
    """
    # Configuración
    SERVICE_ACCOUNT_FILE = 'wlog-henniges-33bd4d15bfe8.json'
    FILE_ID = os.environ.get('GOOGLE_DRIVE_FILE_ID', '1axLJlFa9wIkQS-z_Q1aptfGRjeDPHLwu')
    CSV_FILE = Path(__file__).parent / 'downloads' / 'workcenter-log.csv'
    
    # Scopes necesarios para Google Drive (usar drive completo)
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    try:
        print('Autenticando con Google Drive...')
        # Autenticación con la cuenta de servicio
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        # Crear el servicio de Google Drive
        service = build('drive', 'v3', credentials=credentials)
        
        print(f'Subiendo archivo: {CSV_FILE}')
        
        # Verificar que el archivo existe
        if not CSV_FILE.exists():
            print(f'ERROR: El archivo {CSV_FILE} no existe')
            return False
        
        # Preparar el archivo para subir
        media = MediaFileUpload(
            str(CSV_FILE),
            mimetype='text/csv',
            resumable=True
        )
        
        # Intentar actualizar el archivo existente
        try:
            print(f'Intentando actualizar archivo existente con ID: {FILE_ID}')
            file = service.files().update(
                fileId=FILE_ID,
                media_body=media
            ).execute()
            
            print(f'Archivo actualizado exitosamente en Google Drive!')
            print(f'File ID: {file.get("id")}')
            print(f'Nombre: {file.get("name")}')
            
        except HttpError as e:
            if e.resp.status == 404:
                print(f'Archivo no encontrado. Verificando acceso...')
                
                # Listar archivos accesibles
                print('Listando archivos accesibles por la cuenta de servicio:')
                results = service.files().list(
                    pageSize=10,
                    fields="files(id, name, mimeType)"
                ).execute()
                files = results.get('files', [])
                
                if not files:
                    print('No se encontraron archivos accesibles.')
                    print('\nPara dar acceso a la cuenta de servicio:')
                    print('1. Abre el archivo en Google Drive')
                    print('2. Haz clic en "Compartir"')
                    print('3. Agrega este email y dale permisos de "Editor":')
                    
                    # Obtener el email de la cuenta de servicio
                    with open(SERVICE_ACCOUNT_FILE, 'r') as f:
                        import json
                        service_account_info = json.load(f)
                        print(f'   {service_account_info.get("client_email")}')
                else:
                    print('Archivos encontrados:')
                    for file in files:
                        print(f'  - {file.get("name")} (ID: {file.get("id")})')
                
                print('\nCreando nuevo archivo en Google Drive...')
                file_metadata = {'name': 'workcenter-log.csv'}
                file = service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id, name'
                ).execute()
                
                print(f'Nuevo archivo creado exitosamente!')
                print(f'File ID: {file.get("id")}')
                print(f'Nombre: {file.get("name")}')
                print(f'\nUSA ESTE ID EN EL SCRIPT: {file.get("id")}')
            else:
                raise
        
        return True
        
    except Exception as e:
        print(f'Error al subir archivo a Google Drive: {e}')
        return False

if __name__ == '__main__':
    upload_to_google_drive()
