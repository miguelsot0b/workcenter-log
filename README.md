# Workcenter Log - Plex to Google Drive

Descarga automática de Workcenter Log desde Plex Cloud y subida a Google Drive. Corre cada 10 minutos en Render.

## 🚀 Deploy en Render

1. **Crea el cronjob desde GitHub:**
   - Ve a https://render.com → Blueprints → New Blueprint Instance
   - Conecta: `https://github.com/miguelsot0b/workcenter-log`
   - Render detecta automáticamente `render.yaml`

2. **Configura la variable de entorno:**
   
   Solo necesitas configurar:
   ```
   GOOGLE_SERVICE_ACCOUNT_BASE64 = [base64 del JSON]
   ```
   
   Para generar el base64:
   ```bash
   # Windows PowerShell
   [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("wlog-henniges-33bd4d15bfe8.json"))
   
   # Linux/Mac
   base64 -w 0 wlog-henniges-33bd4d15bfe8.json
   ```

3. **Click Apply** - ¡Listo!

## Variables Configuradas

Estas ya están en `render.yaml`:
- `PLEX_USERNAME`: miguel.soto.ha
- `PLEX_PASSWORD`: Welcome0028
- `GOOGLE_DRIVE_FILE_ID`: 1axLJlFa9wIkQS-z_Q1aptfGRjeDPHLwu

## � Desarrollo Local

```bash
pip install -r requirements.txt
playwright install chromium
python main.py
```

Crea `config.py`:
```python
USERNAME = 'tu_usuario'
PASSWORD = 'tu_password'
```




