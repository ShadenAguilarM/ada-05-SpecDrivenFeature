# AI Usage Log — ADA-09 / CR-01 Review Fix Cycle

## 1. Verificación previa y recepción de decisiones humanas

**Etapa:** Precondition & Governance Check  
**Fecha:** 04 de Noviembre de 2026  
**IA:** Antigravity (Gemini 3.8 Flash)

**Interacción con IA:**  
Se solicitó al Coder Agent revisar `results/human-review-decisions.md` y verificar que los hallazgos tuvieran decisiones humanas confirmadas como `ACCEPTED` o `MODIFIED` y que existiera autorización explícita para iniciar el ciclo de corrección antes de efectuar cualquier modificación.

**Acción de la IA:**  
1. Se inspeccionó inicialmente `results/human-review-decisions.md`, detectando que las decisiones se encontraban como `PENDING CONFIRMATION`, deteniendo cualquier modificación en cumplimiento estricto de la regla de paro y condiciones previas.
2. Tras la confirmación y ratificación humana en `results/human-review-decisions.md` (decisiones `ACCEPTED` para RF-01 hasta RF-07 y compuerta `Return to coder-agent` marcada), se inició formalmente el ciclo de corrección.

**Decisión del desarrollador / Coder Agent:**  
Atender únicamente los hallazgos formalmente aceptados (RF-01 a RF-07) sin extender el alcance de CR-01, sin debilitar pruebas y sin modificar las decisiones o severidades humanas.

---

## 2. Implementación de correcciones en SearchService y optimización

**Etapa:** Implementation & Refactoring  
**Fecha:** 04 de Noviembre de 2026  
**IA:** Antigravity (Gemini 3.8 Flash)

**Interacción con IA:**  
Instrucción de corregir los problemas técnicos señalados por el revisor independiente:
- RF-05: Reducción de validaciones redundantes en bucles O(N) y eliminación de la doble iteración sobre el dataset en `search()`.
- RF-06: Sustitución de llamadas repetidas a `.strip().lower()` por la función reutilizable `normalize_text()`.
- RF-07: Eliminación del enmascaramiento del identificador `field` de `dataclasses`.

**Acción de la IA:**  
- En `src/customer_search/search_service.py`:
  - Se importó `from dataclasses import field as dc_field` y se actualizó `SearchResult.customers = dc_field(default_factory=list)`, eliminando el sombreado de nombres con el parámetro `field`.
  - Se sustituyeron las manipulaciones inline de texto en `customer_sort_key` y en las ramas de coincidencia por llamadas a `normalize_text()`.
  - Se extrajo `_classify_match_normalized(customer, normalized_query, field)` para normalizar la query y validar el campo una sola vez al inicio de `find_matches()`, evitando validaciones redundantes en cada customer evaluado.
  - Se refactorizó `search()` para realizar una única pasada sobre el dataset mediante `find_matches()`, particionando los resultados exactos y parciales en memoria antes de ordenarlos alfabéticamente.

---

## 3. Ampliación de pruebas de regresión y cobertura del contrato de API

**Etapa:** Test & Verification  
**Fecha:** 04 de Noviembre de 2026  
**IA:** Antigravity (Gemini 3.8 Flash)

**Interacción con IA:**  
Instrucción de agregar pruebas de regresión para cubrir las brechas identificadas:
- RF-02: Cobertura de `field="full_name"` y aserciones explícitas de `MatchType` en `test_find_matches_with_field_filter`.
- RF-03: Pruebas unitarias directas para `get_exact_matches()` y `get_partial_matches()` con el parámetro `field`.
- RF-04: Cobertura simétrica (exacta y parcial) en todos los campos soportados (`name`, `surname`, `full_name`, `email`).

**Acción de la IA:**  
- En `tests/test_search_field_filter.py`:
  - Se agregaron casos de prueba exactos y parciales para `name`, `full_name` y `email`.
  - Se agregaron aserciones explícitas de `match_type` (`EXACT` y `PARTIAL`) para coincidencias en `surname` y `full_name`.
  - Se implementaron las funciones de prueba `test_get_exact_matches_with_field_filter` y `test_get_partial_matches_with_field_filter`.

---

## 4. Ejecución de suite de verificación y documentación del ciclo

**Etapa:** Quality Gate & Reporting  
**Fecha:** 04 de Noviembre de 2026  
**IA:** Antigravity (Gemini 3.8 Flash)

**Acción de la IA:**  
- Se ejecutaron las herramientas de calidad configuradas:
  - `pytest -v`: 101 pruebas aprobadas (100%), 95.45% de cobertura global (100% en `search_service.py`).
  - `ruff check .`: sin advertencias ni errores de linting.
  - `ruff format --check .`: 48 archivos formateados correctamente.
  - `mypy src tests`: 21 archivos validados sin inconsistencias de tipos.
  - `scripts/verify_repo.ps1`: 6 etapas aprobadas (`VERIFY_REPO: PASS`).
- Se actualizó `results/coder-report.md` agregando la sección `## Fix Cycle` con el detalle de hallazgos atendidos, archivos modificados, pruebas agregadas, comandos y self-check.

**Verificación:**  
El árbol de trabajo contiene únicamente los archivos autorizados y todos los controles de calidad pasan satisfactoriamente.
