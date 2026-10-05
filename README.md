# ThermoLab

Aplicación de escritorio desarrollada en Python para la adquisición, visualización y gestión de datos experimentales relacionados con procesos térmicos.

## Descripción

ThermoLab permite realizar experimentos mediante la adquisición de datos provenientes de sensores y dispositivos DAQ, proporcionando una interfaz gráfica para visualizar y gestionar las mediciones obtenidas.

El proyecto está orientado a aplicaciones de instrumentación, adquisición de datos y análisis experimental.

## Características

* Interfaz gráfica desarrollada con PyQt6.
* Visualización de datos en tiempo real.
* Adquisición de datos mediante dispositivos MCC DAQ.
* Modo simulación para pruebas sin hardware.
* Gestión de experimentos.
* Visualización de señales y variables medidas.
* Exportación de datos.
* Arquitectura modular para facilitar el mantenimiento y ampliación del sistema.

## Tecnologías utilizadas

* Python
* PyQt6
* PyQtGraph
* NumPy
* Pandas
* OpenPyXL
* ULDAQ
* Packaging

## Estructura del proyecto

```text
ThermoLab/
│
├── app.py                 # Punto de entrada de la aplicación
├── requirements.txt       # Dependencias del proyecto
├── controllers/           # Controladores de la aplicación
├── core/                  # Configuración y utilidades principales
├── daq/                   # Gestión de adquisición de datos
├── gui/                   # Interfaz gráfica
├── models/                # Modelos de datos
├── data/                  # Datos generados por la aplicación
└── reports/               # Reportes
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/ThermoLab.git
cd ThermoLab
```

### 2. Crear un entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

En Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Ejecutar la aplicación

```bash
python app.py
```

## Adquisición de datos

ThermoLab incorpora soporte para sistemas de adquisición de datos MCC mediante ULDAQ.

También dispone de un modo de simulación que permite realizar pruebas de la aplicación sin disponer físicamente del dispositivo de adquisición.

## Estado del proyecto

Proyecto en desarrollo.

## Autor

Diego López
Carlos Betancur"# ThermoLab" 
