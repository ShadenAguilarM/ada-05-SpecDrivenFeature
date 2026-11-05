# AI Usage Log

## 1. Definición y refinamiento del Change Request

- **Fecha:** 03 de Noviembre de 2026 (Aprobación humana) / 04 de Noviembre de 2026, 09:47:05 -0600 (Registro en repositorio)
- **Etapa:** Change Request Definition & Scoping
- **Agente o herramienta utilizada:** Coder Agent / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Documentar formalmente el Change Request CR-01 para la funcionalidad de búsqueda de clientes con filtro de campo opcional y registrar las condiciones de ejecución en el repositorio.
- **Resultado obtenido:** Se generó `CHANGE_REQUEST.md` especificando objetivo, requisitos cubiertos (FR-01, FR-02, AC-01, AC-02, AC-03), restricciones arquitectónicas y criterios de verificación automatizados. Se documentó el estado inicial del entorno en `results/run-context.md`.
- **Evidencia asociada:**
  - Archivo `CHANGE_REQUEST.md` (líneas 1-38, commit `0bcabf21982dce26934ec71a25220059a612829d`).
  - Archivo `results/run-context.md` (líneas 1-51, commit `0bcabf21982dce26934ec71a25220059a612829d`).
- **Decisión tomada:** Aceptada (Aprobación humana por Ashley Aguilar el 03/11/2026).
- **Justificación:** El cambio delimita de forma precisa la extensión de la funcionalidad de búsqueda sin alterar el comportamiento por defecto de búsqueda en todos los atributos cuando el filtro se omite o es `None`.

---

## 2. Plan de implementación propuesto por el Coder Agent

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Implementation Planning
- **Agente o herramienta utilizada:** Coder Agent / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Analizar los documentos del repositorio (`CHANGE_REQUEST.md`, `AGENTS.md`, `SPEC.md`, `ARCHITECTURE.md`) y formular un plan de implementación estructurado antes de codificar.
- **Resultado obtenido:** Se formuló un plan de 6 pasos documentado en la sección `## Implementation Plan` de `results/coder-report.md`:
  1. Revisar especificaciones y restricciones de arquitectura.
  2. Implementar parámetro opcional `field` en operaciones de `SearchService` (`search`, `find_matches`, `execute_search`) y funciones de conveniencia.
  3. Restringir la búsqueda a campos válidos con `VALID_SEARCH_FIELDS` y lanzar `ValueError` en campos no soportados.
  4. Garantizar la paridad de exportación de símbolos en `search.py` y `__init__.py`.
  5. Agregar y actualizar pruebas unitarias en `tests/test_search_field_filter.py`.
  6. Ejecutar script de verificación y herramientas estáticas.
- **Evidencia asociada:**
  - Archivo `results/coder-report.md` (líneas 15-21, commit `b4134e6cb30f7214fad47bf4eff97aeabcbcb69b`).
- **Decisión tomada:** Aceptada (Ejecutado por el Coder Agent).
- **Justificación:** El plan descompuso el cambio respetando las reglas de export parity y la preservación de pruebas exigidas en `AGENTS.md`.

---

## 3. Sugerencia de diseño e implementación del filtro por campo

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Design & Implementation
- **Agente o herramienta utilizada:** Coder Agent / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Incorporar la lógica del filtro de atributos de cliente en `SearchService` manteniendo compatibilidad hacia atrás.
- **Resultado obtenido / Sugerencia:**
  - Definir la constante inmutable `VALID_SEARCH_FIELDS = frozenset({"name", "surname", "full_name", "email"})`.
  - Re-exportar `VALID_SEARCH_FIELDS` en `src/customer_search/search.py` y `src/customer_search/__init__.py`.
  - Validar pertenencia de `field` lanzando `ValueError("Unsupported search field: ...")` cuando el valor no sea `None` ni esté en el conjunto admitido.
  - Conservar el comportamiento predeterminado evaluando todos los atributos cuando `field` sea `None` o se omita.
  - Implementar 10 pruebas unitarias iniciales en `tests/test_search_field_filter.py`.
- **Evidencia asociada:**
  - `src/customer_search/search_service.py` (commit `b4134e6`).
  - `src/customer_search/search.py` y `src/customer_search/__init__.py` (commit `b4134e6`).
  - `tests/test_search_field_filter.py` (commit `b4134e6`).
- **Decisión tomada:** Aceptada.
- **Justificación:** La solución utiliza exclusivamente la biblioteca estándar de Python (evitando dependencias externas), mantiene la paridad de módulos alias y satisface los criterios de aceptación AC-01, AC-02 y AC-03.

---

## 4. Verificación de calidad inicial del repositorio (Verification Gate)

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Initial Verification Gate
- **Agente o herramienta utilizada:** Verification Gate / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Ejecutar de forma independiente las pruebas y herramientas de aseguramiento de calidad sobre el commit `b4134e6`.
- **Resultado obtenido:**
  - `pytest`: 99 pruebas pasadas en 1.06s; 95.19% de cobertura total (superando el umbral mínimo de 90%).
  - `ruff check .` y `ruff format --check .`: Aprobados (44 archivos formateados).
  - `mypy src tests`: 21 archivos validados sin inconsistencias de tipos.
  - `scripts/check_repo_contract.py`: `REPO_CONTRACT: PASS`.
  - Comprobaciones de seguridad: 0 secretos detectados; `data/customers.json` protegido en solo lectura.
  - Se generó el reporte inicial en `results/verification-report.md`.
- **Evidencia asociada:**
  - Archivo `results/verification-report.md` (líneas 1-24, commit `9732898748e779ef83cb3b6a546e07a30dd29ea7`).
- **Decisión tomada:** Aceptada (`Overall Gate: PASS`).
- **Justificación:** Se comprobó que el commit inicial no rompió la suite de pruebas preexistente y cumplió los umbrales de calidad configurados en `pyproject.toml`.

---

## 5. Revisión independiente y detección de hallazgos (Reviewer Agent)

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Independent Code Review
- **Agente o herramienta utilizada:** Independent Reviewer Agent (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Realizar una auditoría técnica en modo solo lectura del PR candidate (`ada09/cr-01`) respecto al commit base `c4dca4d`, verificando trazabilidad, contratos de API, cobertura de pruebas y límites de arquitectura.
- **Resultado obtenido:** Se generó `results/review-report.md` con 7 hallazgos categorizados:
  - **RF-01 (MUST FIX):** Discrepancia en el diff del PR; el reporte del Coder Agent afirmaba modificaciones en `src/`, pero el diff contra `c4dca4d` no contenía cambios en producción debido al historial de ramas anterior.
  - **RF-02 (SHOULD FIX):** Omisión de `field="full_name"` en `test_find_matches_with_field_filter` y ausencia de verificación explícita de `MatchType` en `surname`.
  - **RF-03 (SHOULD FIX):** Falta de pruebas unitarias directas para los métodos públicos `get_exact_matches()` y `get_partial_matches()` con el parámetro `field`.
  - **RF-04 (SHOULD FIX):** Asimetría en pruebas individuales de campo (pruebas exactas sin prueba parcial o viceversa).
  - **RF-05 (SHOULD FIX):** Comprobación redundante de `VALID_SEARCH_FIELDS` dentro del bucle O(N) por cada cliente y doble iteración sobre el dataset en `search()`.
  - **RF-06 (OPTIONAL):** Normalización manual con `.strip().lower()` repetida 8 veces en lugar de usar `normalize_text()`.
  - **RF-07 (OPTIONAL):** El parámetro `field` sombreaba el símbolo `dataclasses.field`.
- **Evidencia asociada:**
  - Archivo `results/review-report.md` (líneas 1-199).
  - Archivo `results/review-contract.md` (líneas 1-27).
- **Decisión tomada:** Pendiente de confirmación humana (Recomendación del revisor: `READY AFTER MUST FIX`).
- **Justificación:** Los hallazgos identificaron riesgos reales de trazabilidad en git, deficiencias de cobertura de pruebas y deuda técnica en el rendimiento de iteración de clientes.

---

## 6. Verificación de condiciones previas, decisión humana y compuerta de retorno

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Human Governance & Stop-Condition Enforcement
- **Agente o herramienta utilizada:** Human Reviewer (Ashley Aguilar) & Coder Agent (Antigravity)
- **Objetivo o instrucción:** Evaluar las recomendaciones del revisor independiente, registrar decisiones formales y gobernar el inicio del ciclo de corrección.
- **Resultado obtenido:**
  1. *Comprobación de condiciones previas (17:37 - 17:40):* El Coder Agent fue invocado para atender hallazgos, pero tras inspeccionar `results/human-review-decisions.md` constató que las decisiones humanas se encontraban en `PENDING CONFIRMATION` y la compuerta `Return to coder-agent` no estaba marcada. En estricto apego a la regla de paro (*"Si las decisiones siguen pendientes, no modifiques nada"*), el agente no realizó cambios y reportó el bloqueo esperando confirmación.
  2. *Decisión humana (17:41):* La persona responsable ratificó formalmente como `ACCEPTED` los 7 hallazgos (RF-01 a RF-07) y marcó la compuerta `[X] Return to coder-agent`.
- **Evidencia asociada:**
  - Archivo `results/human-review-decisions.md` (líneas 1-74).
  - Transcripción de la conversación y primer reporte de Precondition Check.
- **Decisión tomada:** Aceptada (Confirmación humana de RF-01 a RF-07 y apertura formal de la compuerta).
- **Justificación:** La persona responsable validó la necesidad de subsanar tanto la integridad del diff del PR como las brechas de cobertura y diseño técnico señaladas por el revisor.

---

## 7. Implementación del ciclo de correcciones (Fix Cycle)

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Remediation & Refactoring
- **Agente o herramienta utilizada:** Coder Agent / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Atender estrictamente los hallazgos aceptados (RF-01 a RF-07) en el código y pruebas, sin ampliar el alcance de CR-01 ni debilitar pruebas previas.
- **Resultado obtenido:**
  - `src/customer_search/search_service.py`:
    - Se resolvió el sombreado de identificador importando `from dataclasses import field as dc_field` (RF-07).
    - Se reutilizó `normalize_text()` en sustitución de llamadas inline a `.strip().lower()` (RF-06).
    - Se extrajo `_classify_match_normalized()` para ejecutar la normalización de la query y la comprobación de `VALID_SEARCH_FIELDS` una sola vez antes de la iteración de clientes, y se refactorizó `search()` para realizar una única pasada mediante `find_matches()`, particionando en memoria antes del ordenamiento (RF-05).
  - `tests/test_search_field_filter.py`:
    - Se agregaron casos simétricos exactos y parciales para `name`, `full_name` y `email` (RF-04).
    - Se incorporaron pruebas para `field="full_name"` y aserciones explícitas de `MatchType.EXACT` y `MatchType.PARTIAL` en `surname` (RF-02).
    - Se implementaron las pruebas dedicadas `test_get_exact_matches_with_field_filter` y `test_get_partial_matches_with_field_filter` (RF-03).
  - `results/pr.diff`: Se regeneró el parche completo contra base `c4dca4d`, incluyendo los cambios de producción y pruebas (RF-01).
  - `results/coder-report.md`: Se anexó la sección `## Fix Cycle` detallando hallazgos atendidos y autochequeo.
  - Commit generado: `a30266ea5e67934d98fe06980b07693700422b51` con mensaje `fix: address ADA-09 review findings`.
- **Evidencia asociada:**
  - Commit `a30266ea5e67934d98fe06980b07693700422b51`.
  - Archivos modificados: `src/customer_search/search_service.py`, `tests/test_search_field_filter.py`, `results/coder-report.md`, `results/pr.diff`.
- **Decisión tomada:** Aceptada.
- **Justificación:** Todas las acciones ejecutadas se ciñeron a las instrucciones autorizadas en `results/human-review-decisions.md` y mantuvieron limpia la suite de pruebas.

---

## 8. Verificación independiente del ciclo de corrección (Verification Gate)

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Post-Fix Verification Gate
- **Agente o herramienta utilizada:** Verification Gate / Antigravity (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Validar que las correcciones en el commit `a30266e` funcionen correctamente y no hayan introducido nuevas regresiones.
- **Resultado obtenido:**
  - `pytest -v`: 101 pruebas aprobadas en 1.17s (cobertura global 95.45%, 100% en `search_service.py`).
  - `ruff check .`: All checks passed!
  - `ruff format --check .`: 49 archivos verificados con formato correcto.
  - `mypy src tests`: 21 archivos fuente validados con 0 inconsistencias de tipado.
  - `scripts/check_repo_contract.py`: `REPO_CONTRACT: PASS` y comprobaciones de seguridad aprobadas.
  - `scripts/verify_repo.ps1`: 6 etapas de verificación aprobadas (`VERIFY_REPO: PASS`).
  - Se actualizó `results/verification-report.md` incorporando la sección vigente del ciclo de corrección y preservando el registro histórico inicial.
- **Evidencia asociada:**
  - Archivo `results/verification-report.md` (líneas 1-45).
- **Decisión tomada:** Aceptada (`Overall Gate: PASS`).
- **Justificación:** Las 101 pruebas pasaron exitosamente sin regresiones y se certificó el cumplimiento de todos los estándares del proyecto.

---

## 9. Segunda revisión independiente (Independent Re-Review)

- **Fecha:** 04 de Noviembre de 2026
- **Etapa:** Independent Re-Review
- **Agente o herramienta utilizada:** Independent Reviewer Agent (Gemini 3.8 Flash High)
- **Objetivo o instrucción:** Evaluar en modo de solo lectura el estado de resolución de cada uno de los hallazgos originales e identificar si surgieron hallazgos nuevos tras la corrección.
- **Resultado obtenido:**
  - Evaluación de hallazgos originales:
    - RF-01: **RESOLVED** (Evidencia de diff real y reporte alineado en `results/pr.diff` y `results/coder-report.md`).
    - RF-02: **RESOLVED** (Evidencia de aserciones de `match_type` y pruebas de `full_name` en `tests/test_search_field_filter.py:119-142`).
    - RF-03: **RESOLVED** (Evidencia de pruebas unitarias directas en `test_get_exact_matches_with_field_filter` y `test_get_partial_matches_with_field_filter`).
    - RF-04: **RESOLVED** (Evidencia de pruebas simétricas exactas/parciales en `tests/test_search_field_filter.py:42-101`).
    - RF-05: **RESOLVED** (Evidencia de particionado en una pasada en `search()` y extracción de `_classify_match_normalized()`).
    - RF-06: **RESOLVED** (Evidencia de unificación con `normalize_text()` en `search_service.py:124-156`).
    - RF-07: **RESOLVED** (Evidencia de importación `from dataclasses import field as dc_field` en `search_service.py:15`).
  - Hallazgos nuevos: Ninguno (**None**).
  - Recomendación final del revisor: `[X] READY FOR HUMAN REVIEW`.
  - Se generó el reporte formal en `results/re-review-report.md`.
- **Evidencia asociada:**
  - Archivo `results/re-review-report.md` (líneas 1-137).
- **Decisión tomada:** Aceptada (Recomendación formal de pase a revisión humana final).
- **Justificación:** La evidencia de código y ejecución de pruebas demostró la resolución completa de los 7 hallazgos originales sin generar nuevos defectos.
