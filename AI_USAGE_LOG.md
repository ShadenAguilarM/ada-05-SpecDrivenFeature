# AI Usage Log — ADA-05

## 1. Revisión inicial de requisitos y definición del alcance

**Etapa:** Requirements  
**Fecha:** 20/09/2026
**IA:** ChatGPT

**Interacción con IA:**  
Le pedí a la IA revisar los requisitos iniciales de la feature Customer Search y detectar inconsistencias o ambigüedades antes de comenzar la implementación.

**Propuesta de la IA:**  
La IA identificó problemas relacionados con la definición de los campos de búsqueda, la paginación, la coincidencia exacta, la trazabilidad de los requisitos y algunas referencias incorrectas entre los documentos. También recomendó resolver estas cuestiones antes de implementar.

**Decisión del estudiante:**  
Decidí corregir primero los requisitos y mantener el flujo de trabajo spec-driven, evitando comenzar la implementación mientras existieran contradicciones.

**Cambio en el producto/documentación:**  
Se revisó `REQUIREMENTS.md` y se establecieron requisitos funcionales y no funcionales más concretos para Customer Search.

---

## 2. Definición del comportamiento de búsqueda

**Etapa:** Specification  
**Fecha:** 21/09/2026
**IA:** ChatGPT

**Interacción con IA:**  
Consulté a la IA sobre cómo debía definirse la búsqueda y si era conveniente utilizar varios campos de entrada.

**Propuesta de la IA:**  
La IA propuso utilizar un único campo de búsqueda capaz de buscar por nombre, apellido, nombre completo o correo electrónico. También propuso coincidencias parciales, búsqueda sin distinguir mayúsculas/minúsculas y mostrar primero las coincidencias exactas.

**Decisión del estudiante:**  
Decidí utilizar un solo campo de búsqueda porque simplifica la interacción y permite realizar todos los tipos de búsqueda desde el mismo lugar.

**Cambio en el producto/documentación:**  
`REQUIREMENTS.md` y posteriormente `SPEC.md` quedaron definidos alrededor de un único campo de búsqueda, con reglas específicas para coincidencias exactas y parciales.

---

## 3. Decisión sobre el almacenamiento de datos y límite de resultados

**Etapa:** Requirements / Specification  
**Fecha:** 21/09/2026
**IA:** ChatGPT

**Interacción con IA:**  
Le pedí a la IA definir una alternativa concreta para almacenar los clientes considerando que la solución no debía utilizar una base de datos.

**Propuesta de la IA:**  
La IA propuso utilizar un archivo JSON local como fuente de datos, manteniéndolo en modo de solo lectura para la funcionalidad de búsqueda. También se analizó la posibilidad de implementar paginación para los resultados.

**Decisión del estudiante:**  
Decidí utilizar JSON local y establecer un máximo de 10 resultados por búsqueda, sin implementar navegación entre páginas.

**Cambio en el producto/documentación:**  
Se agregó el supuesto `A-01` para el almacenamiento en JSON y se definió en `SPEC.md` que la búsqueda muestra como máximo 10 clientes y que la paginación queda fuera del alcance. 
---

## 4. Revisión de arquitectura y división de tareas

**Etapa:** Architecture / Tasks  
**Fecha:** 23/09/2026
**IA:** ChatGPT

**Interacción con IA:**  
Después de definir los requisitos y la especificación, pedí revisar cómo dividir la implementación y qué componentes serían necesarios.

**Propuesta de la IA:**  
La IA propuso una arquitectura pequeña basada en CLI, Search Service, Customer Data Loader, Customer Model y pruebas con pytest. También propuso dividir la implementación en tareas pequeñas y verificables.

**Decisión del estudiante:**  
Acepté mantener una arquitectura simple y seguir el orden de tareas definido en `TASKS.md`, evitando agregar componentes que no fueran necesarios para la feature.

**Cambio en el producto/documentación:**  
`ARCHITECTURE.md` quedó definido alrededor de esos componentes y `TASKS.md` dividió la implementación en tareas como configuración del proyecto, modelo Customer, carga de JSON, búsqueda, validación, CLI y pruebas. 
---

## 5. Implementación de T-01 

**Etapa:** Implementation  
**Fecha:** 23/09/2026
**IA:** Antigravity

**Interacción con IA:**  
Utilicé Antigravity para implementar la primera tarea después de revisar los documentos del proyecto.

**Propuesta/acción de la IA:**  
El agente creó la estructura básica del proyecto Python y configuró pytest para las pruebas automatizadas.

**Decisión del estudiante:**  
Revisé los archivos generados y el resultado de las pruebas antes de continuar con la siguiente tarea.

**Cambio en el producto:**  
Se crearon `pyproject.toml`, `src/customer_search/__init__.py`, `tests/__init__.py` y `tests/test_setup.py`.

**Verificación:**  
El proyecto utilizó Python 3.14.3 y pytest 9.1.1. La prueba inicial terminó con **1 prueba aprobada**.

---

## 6. Implementación y revisión de T-02

**Etapa:** Implementation / Tests  
**Fecha:** 23/09/2026
**IA:** Antigravity

**Interacción con IA:**  
Utilicé Antigravity para implementar el modelo de cliente definido en `TASKS.md`.

**Propuesta/acción de la IA:**  
El agente creó el modelo `Customer` con `name`, `surname` y `email`, además de una propiedad para obtener el nombre completo. También agregó igualdad e inmutabilidad al modelo.

**Decisión del estudiante:**  
Revisé los cambios y acepté provisionalmente la implementación, identificando que la igualdad e inmutabilidad no eran necesarias para los requisitos actuales y que deberían revisarse para evitar comportamiento no requerido.

**Cambio en el producto:**  
Se modificaron `customer.py`, `models.py`, `__init__.py` y `tests/test_customer.py`, incorporando el modelo y sus pruebas.

**Verificación:**  
Se ejecutó `py_compile` y `pytest -v`. El resultado fue de **7 pruebas aprobadas en 0.05 segundos**.

...