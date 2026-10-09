# Third-Party Skill Pre-Install Audit

Repository: https://github.com/addyosmani/agent-skills
Author / Maintainer: Addy Osmani (GitHub: @addyosmani)
Selected skill: code-review-and-quality
Version / commit inspected: `1401c8b8030e023baeebb31781a6653fe8e93026` (branch: `main`, date: 2026-10-03)

## Purpose
Establecer un proceso sistemático de revisión de código multidimensional antes de realizar el merge de cualquier cambio a la rama principal (`main`). Su objetivo es actuar como una puerta de calidad (*quality gate*) que evalúe si un cambio mejora objetivamente la salud general de la base de código sobre 5 ejes:
1. **Correctness** (corrección funcional, manejo de casos borde y rutas de error).
2. **Readability & Simplicity** (claridad de nomenclatura, flujo directo y reducción de complejidad innecesaria).
3. **Architecture** (respeto a fronteras modulares, consistencia de diseño y prevención de acoplamiento).
4. **Security** (validación en fronteras, saneamiento de entradas y ausencia de vulnerabilidades).
5. **Performance** (prevención de consultas N+1, bucles desmedidos y operaciones sincrónicas costosas).

## Trigger / Description
- **Nombre:** `code-review-and-quality`
- **Descripción en `SKILL.md`:**
  > "Conducts multi-axis code review. Use before merging any change. Use when reviewing code written by yourself, another agent, or a human. Use when you need to assess code quality across multiple dimensions before it enters the main branch. Use when asked to review a diff or a pull request, even when the diff is pasted inline."

### Tareas que disparan la Skill (In-Scope / Triggers)
- Antes de integrar o fusionar (*merge*) cualquier Pull Request o cambio de código.
- Inmediatamente después de completar la implementación de una nueva funcionalidad.
- Al evaluar o auditar código generado por otro agente o modelo de lenguaje.
- Durante tareas de refactorización de código existente.
- Después de resolver un defecto (*bug fix*), revisando tanto la corrección como las pruebas de regresión asociadas.
- Solicitudes directas de revisión de un diff o PR (incluso si el diff se proporciona en línea dentro del prompt).

### Tareas que quedan fuera (Out-of-Scope)
- Implementación de nuevas funcionalidades desde cero.
- Análisis forense especializado de seguridad o endurecimiento profundo de infraestructura (delega a la skill `security-and-hardening`).
- Perfilado detallado y optimización de rendimiento a bajo nivel (delega a la skill `performance-optimization`).
- Cálculo de métricas globales de mutación a escala de repositorio (delega a `constraint-driven-development`).
- Corrección automática o triaje de vulnerabilidades detectadas por auditorías de paquetes (delega a `security-and-hardening`).
- Mezclar refactorizaciones y cambios de comportamiento dentro de una misma revisión sin separarlos.

## Supporting References
- **Archivos locales en el subdirectorio de la skill (`skills/code-review-and-quality/`):**
  - Contiene únicamente el archivo `SKILL.md` (398 líneas, 20.8 KB). No incluye scripts ejecutables en `scripts/`, ni plantillas en `assets/`, ni casos en `evals/`.
- **Referencias externas al directorio (en la raíz del repositorio de origen):**
  - `../../references/security-checklist.md` (lista de verificación de seguridad).
  - `../../references/performance-checklist.md` (lista de verificación de rendimiento).
- **Skills complementarias o dependencias de ecosistema referenciadas:**
  - `security-and-hardening`
  - `performance-optimization`
  - `constraint-driven-development`

## Tools / Commands / Permissions
### Comandos / Scripts que puede ejecutar
- **Ejecución de pruebas:** Comandos del ejecutor de pruebas del proyecto (`pytest`, `npm test`, etc.) para verificar la cobertura y estado de la suite.
- **Compilación / Build:** Comandos del proceso de construcción (`npm run build`, chequeos de tipos de TypeScript o linters).
- **Auditoría de dependencias:** Comandos de seguridad de paquetes como `npm audit`.
- **Herramientas de control de versiones:** Inspección de diffs (`git diff`), historial de cambios (`git log`), y diferencias en el lockfile (`package-lock.json`, etc.).
- **Técnica experimental de Mutation Testing (Paso 2):** Instruye invertir temporalmente una condición en el código de producción, ejecutar las pruebas para verificar si detectan la falla, y luego restaurar el archivo original desde una copia.

### Permisos o herramientas requeridos
- **Lectura de archivos:** Herramientas para leer código, diffs, historiales, changelogs y documentos normativos del proyecto.
- **Ejecución de comandos en terminal:** Permiso para correr pruebas, builds y comandos de inspección en el entorno local.
- **Escritura y restauración de archivos de código:** Requerido si el agente aplica la técnica de prueba de mutaciones de manera activa.
- *Nota de fronteras:* No requiere herramientas de interacción remota con GitHub (no aprueba, no comenta por API ni ejecuta merges remotos).

## Potential Risks
1. **Riesgo de modificación inadvertida de código en revisiones (Violación de Read-Only):** La instrucción del Paso 2 de alterar código para pruebas de mutación (*"Invert one condition the change adds... run the suite, then restore the file from a copy"*) introduce un riesgo significativo de corrupción o cambios colaterales si el agente no restaura con éxito el archivo modificado. Esto choca con la política estricta de revisión *read-only* de nuestro repositorio.
2. **Dependencias relativas rotas:** Referencia rutas relativas a nivel de monorepositorio (`../../references/security-checklist.md` y `../../references/performance-checklist.md`), las cuales quedarán inaccesibles si la skill se instala de forma aislada.
3. **Fuerte acoplamiento con Node.js / JavaScript:** Contiene referencias explícitas a `npm audit`, `package.json`, React y TypeScript, por lo que requiere adaptación para proyectos basados en Python.
4. **Ausencia de validación determinista y evaluadores automatizados:** No posee scripts de validación de salida (`scripts/validate_review_report.py`) ni suites de prueba de disparo o ejecución (`evals/execution_cases.json`, `evals/trigger_cases.json`).
5. **Solapamiento funcional:** El repositorio ya cuenta con la skill nativa `reviewing-pull-requests`, adaptada y probada para la arquitectura, normativas y suites de este proyecto.

## Decision
[x] Install  
[ ] Do not install  

Reason:
Se aprueba la instalación con fines de análisis académico y experimentación comparativa dentro de la práctica. Dado que el repositorio de origen advierte que una instalación individual puede omitir referencias compartidas a nivel de repositorio (`references/`), se procede a instalar la colección completa para observar la skill en su contexto estructural íntegro. Durante la práctica se invocará explícitamente solo `code-review-and-quality`, respetando las precauciones operativas documentadas en esta auditoría.
