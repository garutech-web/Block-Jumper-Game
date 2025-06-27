name: "🚀 Pull Request"
description: "Propuesta de cambios para Block Jumper"
body:
  - type: markdown
    attributes:
      value: |
        ¡Gracias por tu contribución! Por favor, completa la siguiente información:
  - type: textarea
    id: descripcion
    attributes:
      label: "Descripción"
      description: "¿Qué cambios introduces?"
      placeholder: "Agrega una breve descripción de tu PR."
    validations:
      required: true
  - type: textarea
    id: pruebas
    attributes:
      label: "¿Cómo lo probaste?"
      description: "Explica cómo verificaste que tu cambio funciona."
      placeholder: "Ejemplo: ejecuté el juego y pasé el nivel 1."
    validations:
      required: true
  - type: checkboxes
    id: checklist
    attributes:
      label: "Checklist"
      options:
        - label: "He leído las [reglas de contribución](../CONTRIBUTING.md)"
          required: true
        - label: "He probado mi código antes de enviar el PR"
          required: true
        - label: "Mi código sigue el estilo del proyecto"
          required: true
