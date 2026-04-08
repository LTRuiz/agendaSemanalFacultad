# 📚 Sistema de Estudio

Aplicación web personal para organizar el estudio universitario, construida con **Streamlit**. Permite visualizar el horario semanal, trackear bloques de estudio completados, gestionar tareas y hacer seguimiento de parciales.

---

## ✨ Funcionalidades

- **Hoy** — Vista del día actual con bloques de estudio, clases universitarias, advertencias de tareas pendientes y parciales próximos
- **Semana completa** — Vista expandible de los 6 días de estudio con progreso por día
- **Mis Clases** — Horario de cursada con detalle por materia, aula y carga horaria
- **Progreso** — Métricas semanales de horas completadas por materia
- **Tareas** — Gestión de tareas pendientes con fecha de entrega y cuenta regresiva
- **Parciales** — Seguimiento de fechas de parciales con días restantes y estado visual

---

## 🛠️ Tecnologías

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)

---

## 🚀 Instalación

1. Cloná el repositorio:

```bash
git clone https://github.com/LTRuiz/agendaSemanalFacultad.git
cd agendaSemanalFacultad
```

2. Instalá las dependencias:

```bash
pip install streamlit
```

3. Ejecutá la aplicación:

```bash
streamlit run app.py
```

---

## 📁 Estructura del proyecto

```
sistemaEstudios/
├── app.py              # Aplicación principal
├── styles.css          # Estilos CSS separados
├── study_data.json     # Datos persistentes (generado automáticamente)
└── README.md
```

> `study_data.json` se crea automáticamente al usar la app por primera vez. No hace falta crearlo manualmente.

---

## ⚙️ Personalización

Para adaptar la app a tu propia cursada, editá estas secciones en `app.py`:

**Materias** — Cambiá nombres, colores y claves en el diccionario `SUBJECTS`:
```python
SUBJECTS = {
    "asi": {"name": "Analisis de Sistemas", "color": "#1D9E75", ...},
    ...
}
```

**Clases universitarias** — Modificá días, horarios y aulas en la lista `CLASSES`:
```python
CLASSES = [
    {"day": 0, "start": "17:20", "end": "19:45", "aula": "Aula 229", "subj": "asi"},
    ...
]
```

**Horario de estudio** — Editá los bloques diarios en `STUDY_SCHEDULE` (días 0=Lunes a 5=Sábado).

**Parciales** — Actualizá las fechas en la lista `PARCIALES`:
```python
PARCIALES = [
    {"subj": "asi", "nombre": "Parcial Análisis de Sistemas", "fecha": date(2026, 5, 15)},
    ...
]
```

---

## 📌 Roadmap

- [ ] Integración con Google Calendar
- [ ] Notificaciones de recordatorio
- [ ] Modo claro/oscuro automático
- [ ] Exportar progreso semanal

---

## 📄 Licencia

Uso personal. Libre para adaptar a tu propia cursada.
