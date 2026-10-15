# Professional Skill Study — ADA-07

## Source
Repository: https://github.com/addyosmani/agent-skills  
Skill: `code-review-and-quality`  
Version / commit: `1401c8b8030e023baeebb31781a6653fe8e93026` (branch `main`, 2026-10-03)  
Installed path: `.agents/skills/code-review-and-quality/` (`.agents/skills/code-review-and-quality/SKILL.md`)  
Lockfile registration: `skills-lock.json` (SHA-256: `0667c7af98996c0bec4fb0eb444680bdbf1da1d6a3cfdf5dbe8cbd350d9d2752`)

---

## Why this skill was selected
La skill `code-review-and-quality` fue seleccionada para este estudio por cuatro razones estratégicas:

1. **Alineación con el ciclo de vida de desarrollo:** Opera como un *Quality Gate* exhaustivo antes de integrar cualquier cambio a la rama principal (`main`), encajando exactamente en la fase de revisión de PRs tras la implementación de funcionalidades.
2. **Evaluación multidimensional holística (Los 5 Ejes):** A diferencia de revisiones convencionales que solo comprueban si la suite de pruebas pasa, esta skill evalúa simultáneamente Correctness, Readability, Architecture, Security y Performance.
3. **Prestigio técnico y adopción comunitaria:** Desarrollada y mantenida por Addy Osmani (líder de ingeniería en Google Chrome / Web Ecosystem), representa un estándar de referencia en la industria para el diseño de agentes evaluadores de código.
4. **Catálogo de Remedios Estructurales Nombrados:** Proporciona un marco prescriptivo que exige proponer soluciones estructuradas y patrones de diseño reconocibles (*Named Restructurings*) en lugar de críticas vagas o abstractas.
5. **Valor comparativo frente a nuestra skill nativa:** Permite contrastar una skill especializada en gobernanza formal y desarrollo guiado por especificaciones (`reviewing-pull-requests`) contra un estándar industrial universal enfocado en la calidad intrínseca del software.

---

## Anatomy observations
El análisis de la anatomía de `code-review-and-quality` (documentado en profundidad en `docs/professional_skill_anatomy.md`) revela decisiones de diseño clave:

- **Estructura física monolítica:** A diferencia de arquitecturas modulares con carpetas separadas para scripts, plantillas y casos de prueba, esta skill se implementa como un único archivo de instrucciones `SKILL.md` (399 líneas, ~21 KB).
- **Routing flexible y universal:** El frontmatter YAML define un contrato de activación agnóstico al canal. No requiere necesariamente la existencia de un PR formal en GitHub; acepta diffs locales de git e incluso fragmentos de diff pegados en texto (*"even when the diff is pasted inline"*).
- **Workflow de 5 pasos con Quality Gates:**
  1. *Understand the Context:* Comprender el objetivo y el requerimiento antes de mirar el código.
  2. *Review the Tests First:* Evalúa las pruebas antes que la implementación, introduciendo la técnica empírica de **Mutation Testing** (invertir condiciones lógicas para verificar que las pruebas fallen activamente).
  3. *Review the Implementation:* Aplica los 5 ejes de revisión y reglas de dimensionamiento de cambios (~100 líneas por cambio; alertas para archivos que superen ~1,000 líneas totales).
  4. *Categorize Findings:* Aplica el principio de apalancamiento *"Lead with what matters"* (seguridad y arquitectura primero, nits al final) y exige prefijos de severidad explícitos (`Critical:`, `Required:`, `Optional:`, `Nit:`, `FYI`).
  5. *Verify the Verification:* Exige comprobar el relato de verificación (tests verdes, build exitoso, changelog e inspección de diffs del lockfile).
- **Composición y Separación de Responsabilidades:** Aplica el principio de responsabilidad única (*Single Responsibility Principle*), delegando análisis profundos a skills complementarias (`security-and-hardening`, `performance-optimization` y `constraint-driven-development`).
- **Postura ética y límites operativos:** Prohíbe terminantemente la complacencia (*Anti-Sycophancy*, vetando el "LGTM" sin evidencia), prohíbe eliminar código muerto sin consultar al usuario (*Dead Code Hygiene*) y exige respetar el juicio del autor en decisiones de dominio (*"Accept override gracefully"*).

---

## Execution
- **PR / diff reviewed:** PR #42 (`fix/customer-search-whitespace-normalization` → `main`, commit `756f1abd0b5e7a2c5f853bad9c3443d838aad32c`).
  - *Archivos evaluados:* `src/customer_search/search_service.py` (+12 líneas), `tests/test_search_matching.py` (+110 líneas) y 2 archivos binarios compilados `.pyc` en `__pycache__`.
- **Prompt used:**
  ```text
  Use the code-review-and-quality skill to review the same PR / change used in Part I. 
   
  Context: - Read repository requirements/specification when available. - Review the complete diff. - Inspect relevant tests and verification evidence. 
   
  Do not modify code yet. 
  Do not comment, approve, or merge on GitHub. 
   
  Produce the review locally in: 
  results/professional-skill-review.md 
   
  For every finding include: - severity - file / evidence - engineering rationale - recommended action 
   
  Si la Skill recomienda otras Skills como security-and-hardening o performance-optimization, documenta esa composición. 
  No es obligatorio ejecutarlas.
  ```
- **Artifacts produced:**
  1. `results/professional-skill-review.md`: Reporte completo de revisión multi-eje, categorización de hallazgos por severidad, verificación de pruebas con mutación y documentación formal de composición de skills.
  2. `results/skill-comparison.md`: Matriz comparativa de 12 dimensiones entre ambas skills y análisis de accionabilidad.

---

## Findings unique to the professional skill
1. **Cuantificación algorítmica y asignaciones en el Hot Path (Eje Performance + Remedio Estructural "Single-Pass Partitioning"):**
   - *Evidencia / Detalle:* `SearchService.search()` invocaba tanto `get_exact_matches()` como `get_partial_matches()`, y ambos llamaban a `find_matches()`. Mientras que nuestra skill lo vio como una simple mejora opcional menor porque la prueba cumplía NFR-01 (< 2.0s), la skill profesional calculó matemáticamente el desperdicio computacional: para un dataset de 10,000 registros (NFR-02), la doble evaluación ejecuta `classify_match` 20,000 veces y `normalize_text` 80,000 veces. Con el colapso de espacios mediante `.split()` y `" ".join()`, esto generaba 80,000 asignaciones redundantes de cadenas en memoria por búsqueda. Nombró el remedio estructural *"Single-pass partitioning"* y entregó la función reescrita lista para reemplazar.
2. **Auditoría de fronteras de entrada y falta de límite superior en consultas (Eje Security + Principio de Datos No Confiables):**
   - *Evidencia / Detalle:* En `search_service.py:75-93`, la función `validate_search_term()` valida que el texto no esté vacío ni compuesto sólo por espacios, pero no establece un límite máximo de caracteres. La skill profesional identificó este riesgo arquitectónico (Finding 6: FYI): si el servicio se expone posteriormente a un API o servicio en red, una entrada masiva no acotada puede provocar denegación de servicio o agotamiento de memoria en `text.split()`.

---

## Findings unique to my skill
1. **Detección de Requisito Inventado y Spec Drift contra el baseline normativo:**
   - *Evidencia / Detalle:* `reviewing-pull-requests` auditó el colapso de espacios no solo como una alteración de lógica, sino como una violación directa de las reglas del proyecto (`AGENTS.md`: *"Do not invent or add business requirements"*). Contrastó línea por línea contra `REQUIREMENTS.md` (FR-03) y `SPEC.md` (SR-04), demostrando que la especificación solo exigía comparación insensible a mayúsculas y minúsculas. Catalogó la omisión formal como un impedimento de gobernanza que no puede integrarse sin consentimiento explícito del Product Owner.
2. **Delimitación de gobernanza mediante Preguntas Abiertas (`## Open Questions`) y `Human decision required: YES`:**
   - *Evidencia / Detalle:* Mientras que la skill profesional emitió un veredicto unilateral de ingeniería (`REQUEST CHANGES`), nuestra skill reconoció la frontera de autoridad del agente frente al humano. Planteó dos preguntas abiertas concretas para el responsable del proyecto (adopción formal del colapso de espacios como nuevo requisito y adopción de la política de `.gitignore`) y levantó la bandera explícita `Human decision required: YES`, garantizando que la IA apoye la toma de decisiones sin usurpar el rol del stakeholder.

---

## Security / dependency audit

Para evaluar la skill profesional como una dependencia externa de software, se aplicó la matriz de control de higiene de cadena de suministro (*Supply Chain Hygiene*):

| Control | Evidencia |
| :--- | :--- |
| **Source** | Autor y repositorio oficial claramente identificados: Addy Osmani (@addyosmani), repositorio público `https://github.com/addyosmani/agent-skills`. |
| **Pinning** | Commit fijado de forma inmutable a `1401c8b8030e023baeebb31781a6653fe8e93026` (branch `main`, fecha 2026-10-03). Registrado en `skills-lock.json` con hash criptográfico SHA-256: `0667c7af98996c0bec4fb0eb444680bdbf1da1d6a3cfdf5dbe8cbd350d9d2752`. |
| **Audit** | `SKILL.md` inspeccionado exhaustivamente (399 líneas). Es un archivo de instrucciones puramente declarativo en Markdown. No contiene ejecutables binarios, código ofuscado, macros ni scripts en segundo plano. Se identificó la presencia de referencias rotas fuera de paquete (`../../references/`) y acoplamiento semántico al ecosistema Node.js. |
| **Secrets** | No contiene, expone ni solicita llaves de API, contraseñas, tokens de acceso ni credenciales embebidas. No intenta acceder a variables de entorno sensibles ni archivos de configuración locales (`.env`). |
| **Commands** | No contiene scripts ejecutables propios en carpetas auxiliares. Los comandos sugeridos (`pytest`, `git diff`, `npm audit`) fueron inspeccionados previamente. Se vetó operativamente la instrucción del Paso 2 de alterar código en disco para pruebas de mutación, neutralizando el riesgo de corrupción de archivos. |
| **Permissions** | Cumple estrictamente con el principio de mínimo privilegio: sólo requirió permisos de lectura sobre el árbol del proyecto para inspeccionar el diff y ejecución en consola para correr la suite de pruebas `pytest`. No requirió acceso a la red ni privilegios de escritura en GitHub. |
| **Change control** | La skill reside congelada en `.agents/skills/code-review-and-quality/` y está vinculada al archivo de bloqueo `skills-lock.json`. No se realizaron actualizaciones dinámicas ni descargas silenciosas en caliente durante el ciclo de evaluación. |

### Hallazgos de la auditoría de dependencias:
1. **Riesgo Operacional por Mutación en Caliente:** La directriz de alterar código en disco para probar la reacción de los tests entra en conflicto con las políticas estrictas de revisión de solo lectura. Debe confinarse a análisis conceptual estático.
2. **Dependencias Relativas Rotas:** Las rutas `../../references/security-checklist.md` y `performance-checklist.md` asumen una estructura de monorepositorio que queda rota al instalar la skill de forma aislada.

---

## What I would adopt in v2 of my skill
Para la versión 2.0 de `reviewing-pull-requests`, se adoptarán las mejores prácticas de la skill profesional:

1. **Estructura basada en los 5 Ejes Formales de Calidad:**  
   Reorganizar la lista de verificación en Correctness, Readability, Architecture, Security y Performance, asegurando que seguridad y rendimiento sean evaluados sistemáticamente y no dependan de la intuición del evaluador.
2. **Catálogo de Remedios Estructurales Nombrados (*Named Restructurings*):**  
   Exigir que todo hallazgo arquitectónico o de refactorización identifique formalmente el patrón de solución (ej. *"Reuse canonical helper"*, *"Collapse duplicate branches"*, *"Single-pass partitioning"*) y proporcione el bloque de código listo para sustituir.
3. **Análisis de Mutación Conceptual en la Revisión de Pruebas:**  
   Incorporar en el paso de verificación de pruebas un análisis de mutabilidad lógica (razonar si mutar las condiciones introducidas rompe los tests) para detectar aserciones triviales o complacientes.
4. **Taxonomía de Severidad Estandarizada por Prefijos:**  
   Adoptar los prefijos `Critical:`, `Required:`, `Optional:`, `Nit:` y `FYI`, manteniendo el conteo cuantitativo requerido por el validador determinista.
5. **Cuantificación de Rendimiento en Rutas Críticas:**  
   Exigir que las observaciones de rendimiento calculen el orden de magnitud de operaciones y memoria en el peor caso especificado (ej. 10,000 registros), en lugar de limitarse a constatar si el tiempo global cumple con un umbral básico.

---

## Human conclusion
El ejercicio de auditar, ejecutar y comparar una skill comunitaria profesional contra una skill diseñada internamente deja tres aprendizajes fundamentales para la ingeniería de agentes de software:

1. **La complementariedad entre rigor de proceso y madurez técnica:**  
   Nuestra skill nativa destaca en gobernanza, preservación de requisitos y aseguramiento determinista de la salida (gracias a scripts de validación con pruebas unitarias). En contraparte, la skill profesional aporta un lenguaje de ingeniería maduro, principios de diseño universales y una capacidad notable para cuantificar el impacto algorítmico y estructural del código.
2. **La necesidad crítica de higiene en la cadena de suministro de skills:**  
   Las skills de agentes no son simples documentos de texto pasivo; son especificaciones ejecutables que guían las acciones de modelos de lenguaje con acceso a terminal y herramientas del sistema. Importar skills de terceros sin auditar su frontmatter, comandos recomendados, referencias relativas y supuestos de entorno puede inducir comportamientos destructivos (como la modificación inadvertida de código en flujos que deben ser de solo lectura). El uso de archivos de bloqueo criptográfico (`skills-lock.json`) y auditorías previas a la instalación es una práctica indispensable.
3. **Hacia un modelo de diseño híbrido:**  
   La arquitectura óptima para agentes revisores no radica en elegir entre una u otra, sino en crear un modelo híbrido: conservar la trazabilidad de especificaciones, las fronteras éticas de decisión humana y la validación determinista de nuestra skill, potenciándola con los 5 ejes, la cuantificación de rendimiento y los remedios estructurales de la skill profesional.
