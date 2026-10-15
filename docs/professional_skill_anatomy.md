# Anatomía y Análisis de Diseño: Skill `code-review-and-quality`

**Skill analizada:** `code-review-and-quality` ([SKILL.md](file:///C:/Users/ashle/Documents/ADA%2005%20IA/ada-05-SpecDrivenFeature/.agents/skills/code-review-and-quality/SKILL.md))  
**Origen:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)  
**Propósito del documento:** Desglosar la arquitectura interna, decisiones de ingeniería y patrones de interacción que caracterizan el diseño de una skill profesional de revisión de código orientada a agentes.

---

## 1. Routing (Enrutamiento y Disparo)

### Mecanismo de Activación en `description`
El frontmatter YAML define un contrato de activación preciso pero flexible:
* **Identificación del rol funcional:** Define explícitamente su propósito central (*"Conducts multi-axis code review"*).
* **Fases del ciclo de desarrollo:** Establece puntos temporales claros de invocación:
  - Pre-integración obligatoria (*"Use before merging any change"* / *"before it enters the main branch"*).
  - Post-autoría (*"Use when reviewing code written by yourself, another agent, or a human"*).
* **Flexibilidad de entradas (Input Modalities):** Reconoce solicitudes tanto formales (*"review a pull request"*) como informales o locales (*"review a diff"*, e incluso *"even when the diff is pasted inline"*). Esto previene que el agente descarte revisiones cuando el usuario no proporciona un PR formal en GitHub y solo pega un fragmento de código o un diff de Git.
* **Criterios de exclusión implícitos:** Al centrarse exclusivamente en la evaluación multi-eje pre-merge, evita colisionar con agentes constructores de features o solucionadores de tareas directas.

---

## 2. Workflow (Flujo de Trabajo y Quality Gates)

La skill organiza la revisión en 5 pasos secuenciales estructurados para evitar la complacencia (*rubber-stamping*) y garantizar que el evaluador entienda el contexto antes de juzgar la implementación:

```
[Paso 1: Understand the Context]
             │
             ▼
[Paso 2: Review the Tests First] ─── (Quality Gate: Mutation Test empírico)
             │
             ▼
[Paso 3: Review the Implementation] ─ (Quality Gate: 5 Ejes + Reglas de Tamaño)
             │
             ▼
[Paso 4: Categorize Findings] ────── (Quality Gate: Priorización por Severidad)
             │
             ▼
[Paso 5: Verify the Verification] ── (Quality Gate: Build, Tests y Evidencias)
             │
             ▼
        [ Verdict ] ─── (Approve vs Request Changes)
```

### Quality Gates antes de emitir el veredicto:
1. **Gate de Intención y Trazabilidad (Paso 1):** Prohíbe inspeccionar el código sin clarificar qué requerimiento o especificación intenta satisfacer el cambio.
2. **Gate de Prueba Activa / Mutación (Paso 2):** Exige verificar la efectividad de las pruebas no sólo leyendo el código de test, sino mediante un experimento empírico (invertir una condición o operador booleano en el código y verificar que la suite falle; si la suite pasa en verde con la mutación, se cataloga como fallo crítico de cobertura).
3. **Gate de Dimensionamiento y Complejidad (Paso 3):** Aplica umbrales explícitos de cambio:
   - `~100 líneas`: Óptimo.
   - `~300 líneas`: Aceptable para un único cambio lógico.
   - `~1000 líneas` o archivos que superan 1000 líneas totales: Bloqueo presuntivo; exige descomponer antes de añadir código.
4. **Gate de Bloqueadores Presuntivos (*Presumptive Blockers*):** Reubicaciones de complejidad sin simplificación, lógica de feature en módulos compartidos o degradación estructural impiden la aprobación directa.

---

## 3. Review Axes (Los Cinco Ejes de Revisión)

La revisión evalúa el cambio de manera holística a través de cinco dimensiones ortogonales:

| Eje de Revisión | Pregunta Conductora | Criterios de Evaluación y Reglas Clave |
| :--- | :--- | :--- |
| **1. Correctness** | *¿El código hace lo que dice hacer?* | • Coincidencia exacta con la especificación o tarea.<br>• Manejo exhaustivo de casos nulos, vacíos y valores de frontera.<br>• Manejo de rutas de error (no solo el camino feliz).<br>• Ausencia de errores off-by-one, condiciones de carrera o inconsistencias de estado. |
| **2. Readability & Simplicity** | *¿Otro ingeniero o agente puede entender este código sin explicaciones?* | • Nomenclatura descriptiva alineada con las convenciones del proyecto.<br>• Flujo de control directo (evitar ternarios anidados y callbacks profundos).<br>• Regla de abstracción: no generalizar hasta el tercer caso de uso.<br>• Detección de "diseños parchados" (condicionales añadidos sobre flujos ajenos). |
| **3. Architecture** | *¿El cambio encaja en el diseño del sistema?* | • Preservación de límites modulares limpios y dirección unidireccional de dependencias.<br>• Reducción vs. Reubicación: Si una refactorización no disminuye los conceptos mentales requeridos, solo está moviendo deuda.<br>• Prevención de fugas: Ninguna lógica de feature específica debe contaminar módulos genéricos o compartidos.<br>• Límites de tipos explícitos (evitar `any` o conversiones silenciosas). |
| **4. Security** | *¿El cambio introduce vulnerabilidades?* | • Validación y saneamiento estricto de entradas en los bordes del sistema.<br>• Ausencia total de secretos en código, trazas o control de versiones.<br>• Verificación de autorización/autenticación en rutas y recursos sensibles.<br>• Parámetros en consultas de bases de datos y protección contra XSS e inyecciones.<br>• Tratamiento de datos de APIs o configs externas como no confiables. |
| **5. Performance** | *¿El cambio genera cuellos de botella?* | • Detección de consultas N+1 en bases de datos o servicios.<br>• Ausencia de bucles no acotados o consultas sin límite/paginación.<br>• Operaciones pesadas en hilos de ejecución principales (exigencia de asincronía).<br>• Prevención de re-renders innecesarios en UI y asignación masiva de objetos en rutas críticas. |

---

## 4. Severity (Clasificación de Severidad y Priorización)

Para evitar que el autor diluya su atención en detalles menores, la skill establece una taxonomía estricta de prefijos obligatorios y una política de apalancamiento:

### Tabla de Prefijos
* **`Critical:` (Bloquea el merge):** Vulnerabilidades de seguridad, riesgo de pérdida de datos o funcionalidad sustancial rota.
* **`(Sin prefijo)` / Required (Obligatorio):** Deficiencias funcionales, inconsistencias con la especificación o fallos estructurales que deben corregirse antes de integrar.
* **`Optional:` / `Consider:` (Sugerencia):** Propuestas de diseño o optimizaciones recomendables pero que no condicionan la integración.
* **`Nit:` (Menor / Opcional):** Preferencias cosméticas, convenciones estilísticas menores o formato. El autor es libre de descartarlas.
* **`FYI:` (Informativo):** Contexto o notas educativas para el futuro que no requieren acción.

### Principio "Lead with what matters"
* Las observaciones se ordenan por impacto: primero Correctness y Security, luego degradaciones arquitectónicas, y al final detalles cosméticos.
* Si existe un problema estructural mayor y diez detalles cosméticos, la directriz instruye enfocarse en el problema estructural para no saturar al autor con ruido irrelevante.

---

## 5. Verification (Evidencia Exigida para Cerrar la Revisión)

La skill exige una lista de control empírica antes de validar el cierre de la revisión:
* **Resolución de hallazgos obligatorios:**
  - 100% de los elementos `Critical:` solucionados.
  - 100% de los elementos obligatorios sin prefijo resueltos o explícitamente aplazados con justificación formal documentada en un bug.
* **Estado de la suite y build:**
  - Suite de pruebas completa en verde (`Tests pass`).
  - Proceso de construcción/empaquetado exitoso sin advertencias bloqueantes (`Build succeeds`).
* **Documentación del relato de verificación (*Verification Story*):**
  - Registro explícito de qué cambió y exactamente cómo se probó (pruebas automatizadas, pruebas exploratorias manuales o capturas de pantalla para componentes visuales).
* **Disciplina de dependencias:**
  - En actualizaciones de librerías: revisión obligatoria del changelog oficial, aislamiento a un paquete por cambio, pruebas en verde e inspección línea por línea del diff del archivo de bloqueo (`lockfile`).

---

## 6. Composition (Composición y Relación con Otras Skills)

La arquitectura de la skill sigue el principio de responsabilidad única (*Single Responsibility Principle*), delegando análisis profundos a otras skills especializadas del ecosistema:

* **Especialistas Complementarios:**
  - `security-and-hardening`: Invocada cuando se detectan riesgos en cadenas de suministro, vulnerabilidades complejas de red o para el triaje de `npm audit`.
  - `performance-optimization`: Invocada cuando se requieren perfiles de consumo, análisis de flamegraphs o reestructuración profunda de algoritmos.
  - `constraint-driven-development`: Referenciada para análisis de mutación a gran escala y pruebas de invariantes en todo el repositorio.
* **Referencias Compartidas de Repositorio:**
  - `../../references/security-checklist.md`: Lista de verificación granular de seguridad.
  - `../../references/performance-checklist.md`: Matriz de controles de rendimiento.
* **Patrón Multi-Modelo (*Multi-Model Review Pattern*):**
  - Propone orquestar agentes en cadena: un modelo genera el código, un segundo modelo independiente revisa con esta skill para mitigar puntos ciegos, el primer modelo aplica las correcciones y el humano toma la decisión final.

---

## 7. Boundaries (Fronteras de Seguridad y Juicio Humano)

La skill delimita estrictamente el rol del agente auditor para prevenir acciones destructivas o asunciones silenciosas:

### Decisiones delegadas exclusivamente al humano
* **Decisión final de aprobación (*Verdict & Merge*):** El agente emite una recomendación técnica (`Approve` / `Request changes`), pero la decisión final de incorporar el código a producción permanece en el revisor humano.
* **Resolución de discrepancias técnicas:** Si el autor del cambio cuenta con el contexto del dominio y difiere de una sugerencia de diseño, el agente debe aceptar el juicio del autor con respeto (*"Accept override gracefully"*).
* **Postergación de limpiezas técnicas:** El agente no puede aceptar promesas informales de "lo arreglaremos después"; solo un humano puede autorizar diferir una corrección si existe una emergencia real documentada.

### Acciones que NO ejecuta silenciosamente
* **Higiene de código muerto (*Dead Code Hygiene*):** Aunque identifica funciones, constantes o componentes huérfanos generados tras una refactorización, **tiene prohibido eliminarlos por iniciativa propia**. Debe listarlos explícitamente y preguntar al usuario: *"¿Debo eliminar estos elementos en desuso?"*.
* **Cero complacencia (*Anti-Sycophancy*):** Tiene prohibido emitir aprobaciones automáticas ("LGTM") o suavizar la gravedad de defectos reales para agradar al autor.
* **Manipulación de dependencias:** Prohíbe modificar o editar a mano los archivos lockfile (`package-lock.json`), garantizando la integridad reproducible del entorno.
