# FinalTrade-flask-classic
Sitio web de intercambio de Euros y criptomonedas

## Para usar la app web

1. Clonar el repositorio
# con ssh
git clone ssh://.....

# con https
git clone https://.....

2. Crear un entorno virtual dentro de la raíz del repositorio

cd easytrade
python -m venv env

# windows
.\env\Scripts\activate

# linux / MacOs
source ./env/bin/activate

3. Instalar las dependencias

pip install -r requirements.txt

4. Configurar las variables de entorno

copiar el archivo .env_template dentro de la raiz del programa

asignarles el valor

FLASK_APP=run
FLASK_ENV=production
FLASK_SECRET_KEY=tu_token_secrto 
(El token secreto lo puedes asiganar con el valor que tu quieras)

5. Arrancar la App Web

flask run
```




```


