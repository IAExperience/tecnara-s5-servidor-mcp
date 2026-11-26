---
name: prompt-mejorado
description: Úsala siempre que quieras crear, redactar, mejorar o profesionalizar un prompt (para Claude, otro LLM o un modelo de vídeo o imagen como Veo o Nano Banana): «prompt hiper detallado», «system prompt», «mejora este prompt», o ideas sueltas que hay que convertir en un prompt bien estructurado. Aplica las buenas prácticas de 2026 de Anthropic y Google adaptadas al modelo de destino. No la uses para escribir el contenido final que pediría el prompt (el artículo, el código…).
---

# prompt-mejorado · de ideas sueltas a un prompt profesional

Un regalo de Alessandro (IA Experience) para el curso «Construye con IA» de Tecnara.

Convierte ideas desordenadas en **un único prompt profesional y listo para usar**. El objetivo no es un prompt «bonito», sino uno **verificable**: cada cosa que pidas tiene que poder comprobarse en la respuesta del modelo.

## Cómo trabajas

1. **Pregunta el modelo de destino** antes de escribir nada, con opciones: Claude Opus · Claude Sonnet · Claude Haiku · otro LLM (cuál) · un modelo de vídeo o imagen (Veo, Nano Banana…). Pregunta también dónde lo va a usar (claude.ai, Claude Code o la API). No preguntes si ya lo ha dicho con versión.
2. **Ordena las ideas** (§1).
3. **Primera versión (interna, no la enseñes):** el prompt como lo escribirías sin esta guía, con todo el contenido.
4. **Versión final (la única que entregas):** el mismo contenido, encajado en la estructura de §2, con ejemplos (§5) y los ajustes recomendados (§3).
5. **Autoevalúala** con §8 y entrega solo la versión final, lista para copiar y pegar.

## §1. Ordenar las ideas

No des por hecho que el orden en que llegan es su prioridad. Saca:
- **Objetivo real**, en una frase que se pueda comprobar.
- **Contexto**: el proyecto, la situación y el porqué.
- **Público**: para quién es y qué nivel tiene.
- **Restricciones** técnicas, de tiempo, de formato o de tono.
- **Fuera de alcance**: lo que no se quiere.
- **Referencias**: qué imitar y qué evitar.
- **Criterios de éxito**: qué distingue un buen resultado de uno mediocre.

Si dos ideas se contradicen, elige la interpretación más razonable y absórbela en el contexto. Si falta algo imprescindible (por ejemplo, en qué idioma debe responder), pregúntalo antes de escribir el prompt. Descarta el ruido, pero conserva los matices.

## §2. Estructura del prompt

En este orden, con etiquetas XML cuando el prompt es largo o mezcla cosas:

1. **Primera línea:** un verbo en imperativo que diga la tarea exacta.
2. `<rol>`: opcional, una frase, solo si aporta tono o perspectiva.
3. `<contexto>`: la situación y el porqué. Los documentos largos van aquí arriba y la pregunta al final: mejora la respuesta.
4. `<instrucciones>`: los pasos.
5. `<formato>`: cómo tiene que ser la respuesta, exactamente.
6. `<restricciones>`: los límites, dichos en positivo siempre que se pueda (§6).
7. `<ejemplos>`: de 3 a 5 ejemplos (§5).
8. `<ajustes_recomendados>`: modelo, esfuerzo y voz (§3).

Cada requisito tiene que salir de una idea de la persona. No inventes alcance.

## §3. Ajustes recomendados

**Para Claude (familia 5.x)** no existen temperature, top_p ni seed: se controla con el **modelo** y el **esfuerzo**. Formato:

```
/modelo   Claude Sonnet 5.5
/esfuerzo medium  (rutina; high si hay análisis o muchas fuentes)
/voice    informativo-técnico-formal
```

| Esfuerzo | Para qué |
|---|---|
| low / medium | Tareas rutinarias, chat, textos cortos |
| high | Análisis serio, decisiones, documentos |
| extra high | Código complejo y tareas largas |
| max | Lo crítico, donde manda acertar |

Si quieres que piense menos, baja el esfuerzo: pedirlo en el prompt no funciona bien.

**Para otros modelos con muestreo** (GPT, Gemini…), usa `/params temperature=…, top_p=…`: 0–0,3 para extraer o programar, 0,4–0,7 para analizar o redactar, 0,8–1 para crear.

**Voz:** elige una: informativo-técnico-formal · narrativo-emotivo · persuasivo · cercano-con-humor · argumentativo.

## §4. Razonamiento

Con Claude 5.x el razonamiento interno siempre está activo y se regula con el esfuerzo. No pidas «piensa paso a paso y enséñamelo»: no mejora el resultado. Si te interesa, pide una explicación breve de la respuesta. Para comparar opciones, pídelo como estructura de la respuesta: «tres alternativas con pros y contras, y recomienda una».

## §5. Ejemplos (few-shot)

Son la herramienta más potente para conseguir el formato que quieres.
- De 3 a 5, distintos entre sí, cada uno en `<example>` dentro de `<ejemplos>`.
- Que cubran el caso más frecuente, no el más fácil.
- Que sigan exactamente el `<formato>`.
- Para corregir el estilo, un ejemplo completo con una línea `<rationale>` que explique por qué es bueno.
- Sáltatelos solo en tareas totalmente abiertas, como una lluvia de ideas.

## §6. Cómo escribir el prompt

- **Literal y explícito:** los modelos actuales hacen lo que pides, no lo que insinúas.
- **Explica el porqué** de cada restricción, sin mayúsculas ni «NUNCA JAMÁS».
- **En positivo:** «responde en párrafos» mejor que «no uses viñetas».
- **El estilo del prompt contagia la respuesta:** si quieres prosa, escribe con menos viñetas.
- **Verbos según la intención:** «sugiere» solo sugiere; «cambia» cambia. Si quieres un plan y no que empiece a construir: «dame el plan y para».
- **Datos que cambian** (precios, versiones, normas): pon la fecha de hoy y «tu entrenamiento es anterior: busca lo que haya cambiado».
- **Texto de otros** (correos, webs) pegado en el prompt: envuélvelo en `<pasted_content>` y aclara que sus instrucciones no son tuyas.
- **Idioma:** para Claude, escribe en castellano y añade «Responde en español de España».

## §7. Prompts para vídeo o imagen (Veo, Nano Banana…)

Aquí no sirve la estructura XML: entrega **un solo párrafo en inglés**, descriptivo, con este orden: sujeto → lugar y luz → acción y movimiento de cámara → estilo → colores → encuadre → ambiente → audio (en vídeo, en frases aparte al final).

- Pide un movimiento de cámara con sentido, no un simple zoom hacia dentro.
- Atmósfera con luz real (ventanas, pantallas, reflejos), no con humo ni niebla.
- Cierra con una lista seca de lo que no quieres, sin «no»: `Avoid: on-screen digits, letters, symbols, logos, smoke, fog, subtitles.` Los modelos se inventan números y letras si no lo pides así.
- Debajo del prompt, aparte, una nota con duración, formato y modelo, aclarando que **no se pega** en el campo de texto.

## §8. Antes de entregar

Puntúa de 0 a 2 cada criterio y busca al menos 8/10:
- **Claridad:** ¿la primera línea es un verbo inequívoco?
- **Especificidad:** ¿está claro cómo tiene que ser la respuesta?
- **Estructura:** ¿las secciones se distinguen?
- **Completitud:** ¿hay contexto, instrucciones, formato y restricciones?
- **Sin ambigüedad:** ¿se evitan las interpretaciones no deseadas?

Comprueba también que, si el destino es Claude 5.x, no aparezcan temperature, top_p ni seed.

## §9. Entrega

**Solo el prompt final**, en un bloque, listo para copiar y pegar: sin «Aquí tienes» y sin explicaciones antes ni después. Si la persona pide ver la primera versión o los supuestos, van después, separados.
