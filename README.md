# WikiGPT-ES (Videojuegos)

Chatbot con IA entrenado desde cero usando únicamente artículos de Wikipedia en español pertenecientes a categorías de videojuegos. Incluye una arquitectura propia llamada **Arquitectura TRIADA-VG** (Triada de Recuperación, Inferencia y Anclaje para Dominios de Videojuegos), diseñada para ser eficiente, robusta y totalmente reproducible.

## Arquitectura TRIADA-VG
1. **Recuperación semántica ligera**: vectorización TF‑IDF sobre el contenido de artículos.
2. **Inferencia con reglas y abstracción**: se extraen pasajes relevantes y se sintetiza una respuesta con heurísticas controladas.
3. **Anclaje en fuentes**: cada respuesta mantiene referencias internas a los títulos de artículos que la sustentan.

## Requisitos
- Python 3.10+

Instala dependencias:

```bash
pip install -r requirements.txt
```

## Entrenamiento desde cero
El entrenamiento crea un índice a partir de la categoría `Categoría:Videojuegos` (y subcategorías). El modelo es pequeño y reproducible.

```bash
python -m wikigpt_es.train --max-pages 200 --output data
```

## Uso por consola

```bash
python -m wikigpt_es.cli --data data
```

## GUI

```bash
python -m wikigpt_es.gui --data data
```

## Nota sobre datos
Este proyecto usa exclusivamente artículos de Wikipedia en español dentro de categorías de videojuegos.
