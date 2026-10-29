# AI Usage Log — ADA-08

## 1. Selección de la tarea para el experimento

**Etapa:** Task Selection  
**Fecha:** 26 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Le pedí a Antigravity determinar una actividad adecuada para utilizarla como tarea de prueba en `TASK_UNDER_TEST.md`. La actividad debía permitir comparar el comportamiento del agente antes y después de aplicar las mejoras Agent-Ready al repositorio.

**Propuesta de la IA:**  
Antigravity propuso la tarea CR-01, consistente en agregar un filtro por campo a la funcionalidad existente de búsqueda de clientes. La tarea permite modificar código existente, respetar la arquitectura del proyecto y verificar el comportamiento mediante pruebas automatizadas.

**Decisión del estudiante:**  
Revisé la actividad propuesta y la aprobé porque implicaba un cambio funcional concreto, suficientemente acotado y verificable. Además, permitía utilizar exactamente la misma tarea en las ejecuciones BEFORE y AFTER.

**Cambio en el producto/documentación:**  
Se estableció `TASK_UNDER_TEST.md` como documento de referencia para CR-01, identificando el objetivo del cambio, los requisitos relacionados, la evidencia de verificación y las restricciones de implementación.

**Verificación:**  
La tarea seleccionada debía ser lo suficientemente significativa para requerir comprensión del contexto del repositorio, cambios en el código y ejecución de pruebas, sin redefinir los requisitos existentes.

---

## 2. Auditoría inicial de la preparación del repositorio

**Etapa:** Repository Readiness Audit — BEFORE  
**Fecha:** 26 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Utilicé Antigravity para evaluar el estado inicial del repositorio y detectar las dificultades que podría enfrentar un agente al explorar el proyecto, implementar CR-01 y comprobar su funcionamiento.

**Acción de la IA:**  
Se realizó la inspección del repositorio y de su documentación para evaluar las ocho dimensiones de preparación establecidas en ADA-08: navegación, instrucciones del agente, ejecución y pruebas, límites arquitectónicos, trazabilidad, automatización, evidencia y seguridad.

**Decisión del estudiante:**  
La evaluación debía reflejar las condiciones reales del repositorio antes de aplicar las mejoras Agent-Ready. Se mantuvieron los mismos criterios y pesos establecidos para poder comparar posteriormente los resultados.

**Cambio en el producto/documentación:**  
Se utilizó `REPOSITORY_READINESS_AUDIT.md` para registrar las puntuaciones, la evidencia de cada dimensión, las principales brechas y los tres puntos de fricción más importantes.

**Verificación:**  
La auditoría debía incluir las ocho dimensiones con sus pesos originales y calcular `TOTAL BEFORE` sobre 100 puntos. Las puntuaciones debían justificarse mediante evidencia concreta y no solamente por la existencia de archivos.

---

## 3. Ejecución del agente en el estado BEFORE

**Etapa:** BEFORE Agent Run  
**Fecha:** 26 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Ejecuté CR-01 en el estado inicial del repositorio para observar cómo Antigravity exploraba el proyecto, identificaba los archivos relevantes, implementaba el cambio y ejecutaba las validaciones disponibles.

**Acción de la IA:**  
Antigravity implementó el filtro opcional por campo para la búsqueda de clientes. El reporte de ejecución documentó los archivos modificados, las pruebas y los resultados obtenidos.

**Decisión del estudiante:**  
Conservé la ejecución como evidencia BEFORE para compararla con la ejecución posterior. La implementación generada debía mantenerse separada y no reutilizarse como punto de partida para AFTER.

**Cambio en el producto:**  
Durante esta ejecución se incorporó la funcionalidad CR-01 y se agregó `tests/test_search_field_filter.py` para probar el comportamiento nuevo.

**Verificación:**  
El reporte histórico BEFORE indicó que el conjunto original tenía 73 pruebas y que, después de incorporar las nueve pruebas específicas de CR-01, se obtuvieron 82 pruebas aprobadas.

Estos resultados corresponden a la ejecución histórica y deben distinguirse del estado preparado posteriormente para la comparación controlada.

---

## 4. Identificación del conocimiento implícito

**Etapa:** Implicit Knowledge Analysis  
**Fecha:** 26 Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Después de la ejecución BEFORE, utilicé Antigravity para identificar información del proyecto que no estaba suficientemente explícita y que el agente tuvo que descubrir mediante la inspección del código, los archivos de configuración o los errores durante la ejecución.

**Acción de la IA:**  
Se documentaron dificultades relacionadas con las particularidades del entorno y la forma de modificar o ejecutar el proyecto. Entre los hallazgos registrados se encuentran los finales de línea CRLF, que provocaron un fallo al intentar modificar un archivo mediante coincidencia de texto, y el tratamiento de argumentos vacíos de PowerShell al ejecutar la CLI.

**Decisión del estudiante:**  
Decidí documentar el conocimiento implícito que afectaba la confiabilidad del trabajo del agente, distinguiendo entre información que debía explicitarse en las instrucciones y reglas que podían convertirse en verificaciones automáticas.

**Cambio en el producto/documentación:**  
Se utilizó `results/implicit-knowledge.md` para registrar los hallazgos, cómo fueron descubiertos, los riesgos asociados y las posibles medidas de remediación.

**Verificación:**  
Los hallazgos debían estar respaldados por evidencia, como errores observados, comandos ejecutados o inspección del código. No toda información implícita debía convertirse en documentación: cuando una regla podía comprobarse de manera determinista, se consideró preferible automatizarla.

---

## 5. Preparación de las instrucciones del repositorio

**Etapa:** Agent Instructions / Repository Navigation  
**Fecha:** 27 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Trabajé con Antigravity en las mejoras necesarias para que un agente pudiera comprender el repositorio y trabajar con menos dependencia de conocimiento previo o instrucciones manuales.

**Acción de la IA:**  
Se trabajó en la organización de las instrucciones del repositorio, las fuentes de verdad, los comandos de validación, los límites arquitectónicos y las condiciones necesarias para completar una tarea.

**Decisión del estudiante:**  
Se mantuvo la estructura spec-driven existente. Las instrucciones debían dirigir al agente hacia los documentos autoritativos, sin duplicar los requisitos ni convertir `AGENTS.md` en una fuente alternativa de comportamiento.

**Cambio en el producto/documentación:**  
Se trabajó con `AGENTS.md` y la documentación del proyecto para hacer explícitos el flujo de trabajo, los comandos, las restricciones de cambios y la Definition of Done. También se contempló `docs/REPO_MAP.md` para facilitar la localización de puntos de entrada, pruebas, límites arquitectónicos y rutas protegidas.

**Verificación:**  
Se debía comprobar que las rutas y comandos documentados existieran y que las instrucciones fueran coherentes con los requisitos, la especificación, la arquitectura y las tareas.

Las propuestas individuales aceptadas o rechazadas deben registrarse según el historial real de Antigravity, sin atribuir decisiones que no estén documentadas.

---

## 6. Automatización de reglas y verificación del repositorio

**Etapa:** Automation / Guardrails / CI  
**Fecha:** 27 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Utilicé Antigravity para trabajar en las verificaciones del repositorio y reducir la dependencia de instrucciones que el agente pudiera pasar por alto.

**Acción de la IA:**  
Se trabajó con el mecanismo de verificación integrado `scripts/verify_repo.ps1` y los controles del repositorio para ejecutar las validaciones de manera reproducible.

**Decisión del estudiante:**  
Se priorizó que las reglas importantes pudieran comprobarse automáticamente, especialmente las relacionadas con la integridad de las especificaciones y las pruebas. La intención era compartir verificaciones consistentes entre el desarrollador y el agente, además de las que estuvieran configuradas en CI.

**Cambio en el producto/documentación:**  
Se utilizó `scripts/verify_repo.ps1` como comando central de verificación y se conservaron las mejoras Agent-Ready destinadas a hacer más reproducible el proceso.

**Verificación:**  
El estado preparado antes de volver a ejecutar CR-01 reportó 89 pruebas aprobadas, 93.53 % de cobertura y `VERIFY_REPO: PASS`.

La existencia de un script local no demuestra por sí sola que las mismas verificaciones se ejecuten en CI; esto debe comprobarse mediante la configuración y los resultados del pipeline correspondiente.

---

## 7. Preparación del baseline para la comparación AFTER

**Etapa:** Baseline Preparation  
**Fecha:** 27 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Durante la preparación de AFTER se identificó que la rama con las mejoras Agent-Ready ya contenía la implementación de CR-01. Era necesario retirar esa funcionalidad para que el agente pudiera implementarla nuevamente durante la prueba.

**Acción de la IA:**  
Antigravity retiró los cambios de CR-01 de `search_service.py`, `search.py` y `__init__.py`. En una primera verificación, las pruebas fallaron porque permanecía `tests/test_search_field_filter.py`, que dependía de la funcionalidad retirada.

Posteriormente, se revisó el historial de Git para determinar el origen del archivo de pruebas.

**Decisión del estudiante:**  
Decidí conservar las mejoras Agent-Ready y retirar únicamente los elementos asociados a CR-01. Acepté eliminar el archivo de pruebas específico porque el historial indicaba que había sido introducido junto con la funcionalidad y no pertenecía a las ocho suites de pruebas originales.

**Cambio en el producto:**  
Se eliminó `tests/test_search_field_filter.py`, manteniendo `TASK_UNDER_TEST.md`, las pruebas originales y las mejoras Agent-Ready.

**Verificación:**  
El estado preparado se reportó con 89 pruebas aprobadas, 93.53 % de cobertura y `VERIFY_REPO: PASS`.

La preparación también requirió comprobar que la implementación anterior no se reutilizara en AFTER. La identidad del baseline funcional común debía verificarse mediante el historial de Git y los commits de ambas ramas.

---

## 8. Ejecución de CR-01 en el estado AFTER

**Etapa:** AFTER Agent Run  
**Fecha:** 28 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Ejecuté nuevamente CR-01 en el repositorio preparado con las mejoras Agent-Ready, utilizando una sesión nueva para evitar reutilizar la implementación de BEFORE.

**Acción de la IA:**  
Antigravity volvió a implementar el filtro opcional por campo para la búsqueda de clientes. Se admitieron `name`, `surname`, `full_name` y `email`; se agregó `VALID_SEARCH_FIELDS` y se incorporó validación para rechazar campos no admitidos mediante `ValueError`. La omisión del parámetro o el uso de `None` conservó la búsqueda en todos los campos.

**Decisión del estudiante:**  
Conservé el reporte AFTER como evidencia y revisé los resultados de las pruebas y de las herramientas de validación para evaluar si la implementación cumplía la tarea.

**Cambio en el producto:**  
Se modificaron:

- `src/customer_search/search_service.py`
- `src/customer_search/search.py`
- `src/customer_search/__init__.py`
- `tests/test_search_field_filter.py`

**Verificación:**  
El reporte AFTER registró:

- 98 pruebas aprobadas.
- 95.19 % de cobertura.
- `ruff check .`: aprobado.
- `ruff format --check .`: 39 archivos ya estaban formateados.
- `mypy src tests`: sin problemas en 21 archivos fuente.
- `scripts/verify_repo.ps1`: seis etapas aprobadas.
- Resultado final: `PASS`.

La ejecución aislada de `tests/test_search_field_filter.py` terminó con código de salida 1 por el umbral global de cobertura de pytest-cov, aunque las nueve pruebas de ese archivo pasaron. La suite completa superó el umbral global.

---

## 9. Comparación de los resultados BEFORE y AFTER

**Etapa:** Evaluation  
**Fecha:** 28 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Utilicé los reportes de ambas ejecuciones para comparar las pruebas aprobadas, la cobertura y las validaciones realizadas.

**Acción de la IA:**  
Los reportes registraron los archivos modificados, los comandos ejecutados, los resultados de las pruebas y el estado final de cada ejecución.

**Decisión del estudiante:**  
Decidí distinguir los resultados históricos de BEFORE de los resultados obtenidos al ejecutar la tarea sobre el repositorio preparado. También consideré necesario comprobar los commits y las condiciones experimentales antes de atribuir las diferencias exclusivamente a las mejoras Agent-Ready.

**Cambio en la documentación:**  
Se conservaron los reportes de ejecución para documentar las evidencias y realizar la comparación del experimento.

**Verificación:**

| Métrica | BEFORE histórico | AFTER |
|---|---:|---:|
| Pruebas aprobadas | 82 | 98 |
| Cobertura | No confirmada en el reporte histórico disponible | 95.19 % |
| Validación integrada | No documentada de forma equivalente | `PASS` reportado |

El estado preparado antes de AFTER registró 89 pruebas aprobadas y 93.53 % de cobertura. Por ello, los resultados 82 y 98 no deben utilizarse por sí solos como una comparación controlada: el estado preparado de ADA-08 debe compararse con el AFTER cuando se evalúe el efecto de la tarea sobre el mismo baseline.

**Resultado:**  
La ejecución AFTER terminó con las validaciones reportadas como aprobadas. La mejora de la preparación del repositorio debe evaluarse adicionalmente con las auditorías BEFORE y AFTER, utilizando las mismas ocho dimensiones y los mismos pesos.

---

## 10. Revisión final y limitaciones

**Etapa:** Final Review  
**Fecha:** 28 de Octubre de 2026  
**IA:** Antigravity

**Interacción con IA:**  
Revisé los reportes de ejecución y la evidencia disponible para determinar qué resultados podían considerarse comprobados y qué aspectos necesitaban una revisión adicional.

**Acción de la IA:**  
Antigravity documentó los resultados de la implementación AFTER y las validaciones realizadas. Los reportes permitieron identificar tanto las comprobaciones aprobadas como las limitaciones surgidas durante la ejecución.

**Decisión del estudiante:**  
Decidí conservar los resultados sin asumir que las pruebas aprobadas demostraban por sí solas que todas las mejoras Agent-Ready habían producido un efecto positivo.

**Cambio en la documentación:**  
Se utilizaron los reportes de ejecución, las auditorías de readiness y el historial de Git como evidencia para evaluar el resultado del experimento.

**Verificación:**  
La conclusión requiere comprobar que BEFORE y AFTER parten del mismo estado funcional, utilizan la misma tarea y el mismo prompt oficial, y no reutilizan la implementación generada durante BEFORE. También requiere completar las auditorías de preparación y calcular el delta con los pesos originales.

La intervención humana sigue siendo necesaria para resolver ambigüedades de requisitos, revisar decisiones arquitectónicas y confirmar que las conclusiones se apoyen en evidencia suficiente.

---