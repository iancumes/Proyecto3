
# Simulador de Máquina de Turing (una cinta)

Este proyecto implementa un **simulador de Máquinas de Turing de una cinta** configuradas mediante
archivos YAML, tal y como se describe en tu enunciado.

## Estructura del proyecto

```
tm_simulator/
├── main.py                  # Punto de entrada (CLI)
├── requirements.txt         # Dependencias (PyYAML)
├── tmsim/
│   ├── __init__.py
│   ├── turing_machine.py    # Lógica de la MT (cinta, transiciones, simulación)
│   └── parser_yaml.py       # Parsing del archivo YAML a objetos de Python
└── machines/
    └── mt1_reconocedora.yaml   # Ejemplo de configuración de una MT
    └── mt2_reconocedora.yaml
```

## Instalación (entorno local)

1. Crear y entrar al directorio del proyecto (ya existe si estás leyendo este archivo).
2. (Opcional pero recomendado) Crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar una máquina

Ejemplo utilizando la MT de `machines/example_mt_1.yaml`:

```bash
python main.py machines/mt1_reconocedora.yaml
```

El programa:

- Lee el archivo YAML.
- Construye la Máquina de Turing (estados, alfabetos, delta, etc.).
- Simula **todas** las cadenas configuradas en `simulation_strings`.
- Imprime en consola todas las **descripciones instantáneas (IDs)**:
  - Número de paso.
  - Estado actual.
  - Valor de la memoria (`mem_cache_value`).
  - Contenido de la cinta, marcando la posición del cabezal con `[]`.
- Al final muestra:
  - Estado final.
  - Contenido final de la cinta.
  - Si la cadena fue **aceptada** o **rechazada** (si el estado final está en el conjunto de estados finales).

También puedes simular una cadena manualmente (ignorando `simulation_strings`):

```bash
python main.py machines/example_mt_1.yaml --string aab#aab
```

Y limitar los pasos de simulación:

```bash
python main.py machines/example_mt_1.yaml --max-steps 5000
```

## Cómo definir tus propias MT

1. Copia `machines/example_mt_1.yaml` a un nuevo archivo, por ejemplo:

```bash
cp machines/example_mt_1.yaml machines/mt_reconocedora.yaml
```

2. Edita:

- La lista de estados (`q_states.q_list`, `initial`, `final`).
- Los alfabetos `alphabet` y `tape_alphabet`.
- Las transiciones en `delta`:
  - Cada transición tiene:
    - `params.initial_state`
    - `params.mem_cache_value` (puede estar vacío = `None`)
    - `params.tape_input` (símbolo leído de la cinta, puede ser vacío = blank)
    - `output.final_state`
    - `output.mem_cache_value` (nuevo valor en memoria; puede ser vacío)
    - `output.tape_output` (símbolo a escribir; puede ser vacío = blank)
    - `output.tape_displacement` (`L`, `R` o `S`)
- Las cadenas en `simulation_strings`.

3. Ejecuta:

```bash
python main.py machines/mt_reconocedora.yaml
```
