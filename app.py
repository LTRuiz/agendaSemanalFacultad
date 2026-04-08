import streamlit as st
import json
from datetime import date, timedelta
from pathlib import Path

st.set_page_config(page_title="Sistema de Estudio", page_icon="📚", layout="wide")

# ── Persistencia ───────────────────────────────────────────────────────────────
DATA_FILE = Path("study_data.json")

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {"done_blocks": {}, "tasks": []}

def save_data(d):
    with open(DATA_FILE, "w") as f:
        json.dump(d, f, indent=2, default=str)

if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ── Materias ───────────────────────────────────────────────────────────────────
SUBJECTS = {
    "asi": {"name": "Analisis de Sistemas",   "short": "Analisis Sist.", "color": "#1D9E75", "bg": "#E1F5EE"},
    "fis": {"name": "Fisica II",               "short": "Fisica II",      "color": "#378ADD", "bg": "#E6F1FB"},
    "com": {"name": "Comunicacion de Datos",   "short": "Com. Datos",     "color": "#D4537E", "bg": "#FBEAF0"},
    "mat": {"name": "Analisis Matematico II",  "short": "Anal. Mat. II",  "color": "#7F77DD", "bg": "#EEEDFE"},
    "py":  {"name": "Python (fundamentos)",    "short": "Python",         "color": "#EF9F27", "bg": "#FAEEDA"},
}

# ── Clases universitarias ──────────────────────────────────────────────────────
CLASSES = [
    {"day": 0, "start": "17:20", "end": "19:45", "aula": "Aula 229", "subj": "asi"},
    {"day": 1, "start": "17:20", "end": "19:45", "aula": "Aula 229", "subj": "fis"},
    {"day": 2, "start": "17:20", "end": "19:00", "aula": "Aula 610", "subj": "com"},
    {"day": 2, "start": "19:00", "end": "20:40", "aula": "Aula 226", "subj": "fis"},
    {"day": 3, "start": "18:15", "end": "20:40", "aula": "Aula 223", "subj": "mat"},
    {"day": 3, "start": "20:40", "end": "23:05", "aula": "Aula 702", "subj": "asi"},
    {"day": 4, "start": "21:35", "end": "23:05", "aula": "Aula 411", "subj": "com"},
    {"day": 5, "start": "15:00", "end": "17:25", "aula": "Aula 227", "subj": "mat"},
]

PARCIALES = [
    # {"subj": "asi", "nombre": "Parcial Análisis de Sistemas", "fecha": date(2026, 5, 15)},
    # {"subj": "fis", "nombre": "Parcial Física II",             "fecha": date(2026, 5, 20)},
    # {"subj": "com", "nombre": "Parcial Comunicación de Datos", "fecha": date(2026, 5, 22)},
    # {"subj": "mat", "nombre": "Parcial Análisis Matemático II","fecha": date(2026, 6, 3)},
]

# ── Horario de estudio: 25hs semana, Lun-Sab, desde 9:00 ──────────────────────
#
# Lunes    4.5hs  |  Martes   4.0hs  |  Miercoles 4.0hs
# Jueves   4.25hs |  Viernes  4.0hs  |  Sabado    4.25hs  => 25hs
#
# Regla: cada materia se estudia el dia ANTES de su clase.
# Descanso 15min entre bloques. Almuerzo 13:00-14:00 (Lun-Vie).
#
# (inicio, fin, titulo, descripcion, subj)
STUDY_SCHEDULE = {
    0: [
        ("09:00", "10:30", "Fisica II",            "Teoria y ejercicios (clase mañana martes)",  "fis"),
        ("10:45", "12:15", "Analisis de Sistemas",  "Repaso antes de clase esta noche",           "asi"),
        ("13:00", "14:00", "Almuerzo",              "",                                            "lunch"),
        ("14:00", "15:30", "Python",               "Variables, condicionales y bucles",           "py"),
    ],
    1: [
        ("09:00", "10:30", "Comunicacion de Datos", "Protocolos y modelos de red (clase mañana)", "com"),
        ("10:45", "12:00", "Fisica II",             "Repaso antes de clase esta noche",           "fis"),
        ("13:00", "14:00", "Almuerzo",              "",                                            "lunch"),
        ("14:00", "15:15", "Analisis Mat. II",      "Practica de ejercicios",                     "mat"),
    ],
    2: [
        ("09:00", "10:30", "Analisis Mat. II",      "Ejercicios (clase mañana jueves)",           "mat"),
        ("10:45", "12:00", "Comunicacion de Datos", "Repaso antes de clase esta noche",           "com"),
        ("13:00", "14:00", "Almuerzo",              "",                                            "lunch"),
        ("14:00", "15:15", "Analisis de Sistemas",  "Modelado y diagramas UML",                   "asi"),
    ],
    3: [
        ("09:00", "10:30", "Analisis Mat. II",      "Repaso antes de clase esta noche",           "mat"),
        ("10:45", "12:00", "Analisis de Sistemas",  "Repaso antes de clase esta noche",           "asi"),
        ("13:00", "14:00", "Almuerzo",              "",                                            "lunch"),
        ("14:00", "15:45", "Python",               "Funciones, listas y diccionarios",            "py"),
    ],
    4: [
        ("09:00", "10:30", "Comunicacion de Datos", "Repaso antes de clase esta noche",           "com"),
        ("10:45", "12:15", "Fisica II",             "Ejercicios y cierre de semana",              "fis"),
        ("13:00", "14:00", "Almuerzo",              "",                                            "lunch"),
        ("14:00", "15:15", "Analisis de Sistemas",  "Practica integradora",                       "asi"),
    ],
    5: [
        ("09:00", "10:30", "Python",               "POO: clases y objetos",                      "py"),
        ("10:45", "12:00", "Fisica II",             "Resolucion de ejercicios de la semana",      "fis"),
        ("12:15", "13:30", "Analisis Mat. II",      "Repaso antes de clase a las 15hs",           "mat"),
    ],
}

# ── Helpers ────────────────────────────────────────────────────────────────────
DAY_NAMES = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]

def get_week_dates(ref):
    monday = ref - timedelta(days=ref.weekday())
    return [monday + timedelta(days=i) for i in range(7)]

def block_id(d, idx):
    return str(d.isoformat()) + "_" + str(idx)

def toggle_block(bid):
    data["done_blocks"][bid] = not data["done_blocks"].get(bid, False)
    save_data(data)

def add_task(text, subj, due):
    data["tasks"].append({"text": text, "subj": subj, "due": str(due) if due else "", "done": False})
    save_data(data)

def toggle_task(i):
    data["tasks"][i]["done"] = not data["tasks"][i]["done"]
    save_data(data)

def get_all_parciales():
    extras = [
        {
            "subj": p["subj"],
            "nombre": p["nombre"],
            "fecha": date.fromisoformat(p["fecha"])
        }
        for p in data.get("parciales_extra", [])
    ]
    return PARCIALES + extras

def delete_task(i):
    data["tasks"].pop(i)
    save_data(data)

def get_blocks(weekday):
    raw = STUDY_SCHEDULE.get(weekday, [])
    return [{"start": r[0], "end": r[1], "title": r[2], "sub": r[3], "subj": r[4]} for r in raw]

def minutes_between(start, end):
    sh, sm = int(start[:2]), int(start[3:])
    eh, em = int(end[:2]),   int(end[3:])
    return (eh * 60 + em) - (sh * 60 + sm)

def fmt_dur(minutes):
    h, m = divmod(minutes, 60)
    if m == 0:
        return str(h) + "h"
    return str(h) + "h " + str(m) + "min"

total_study_min = sum(
    minutes_between(r[0], r[1])
    for day_raw in STUDY_SCHEDULE.values()
    for r in day_raw
    if r[4] != "lunch"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
def load_css(path: str):
    with open(path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ── Cabecera ───────────────────────────────────────────────────────────────────
today      = date.today()
week_dates = get_week_dates(today)

c1, c2, c3 = st.columns([3, 2, 1])
with c1:
    st.title("Sistema de Estudio")
with c2:
    st.markdown("**Semana** " + week_dates[0].strftime("%d/%m") + " - " + week_dates[5].strftime("%d/%m/%Y"))
with c3:
    st.markdown("**" + str(round(total_study_min / 60, 1)) + " hs / semana**")

tab_hoy, tab_semana, tab_parciales, tab_cursada, tab_progreso, tab_tareas = st.tabs(
    ["Hoy", "Semana completa", "Parciales", "Mis Clases", "Progreso", "Tareas"]
)

# ═══════════════════════════════════════════════════════════════════════════════
# HOY
# ═══════════════════════════════════════════════════════════════════════════════
with tab_hoy:
    wd = today.weekday()
    st.subheader(DAY_NAMES[wd] + "  " + today.strftime("%d/%m/%Y"))
    
    pending_tasks = [t for t in data["tasks"] if not t["done"]]
    if pending_tasks:
        lines = ""
        for t in pending_tasks:
            s = SUBJECTS.get(t.get("subj"), SUBJECTS["py"])
            if t.get("due"):
                due_date = date.fromisoformat(t["due"])
                days_left = (due_date - today).days
                if days_left < 0:
                    due_str = " — <span style='color:#ff6b6b;'>vencida hace " + str(abs(days_left)) + " día(s)</span>"
                elif days_left == 0:
                    due_str = " — <span style='color:#ff6b6b;'>vence HOY</span>"
                elif days_left == 1:
                    due_str = " — <span style='color:#f0a500;'>vence mañana</span>"
                else:
                    due_str = " — <span style='color:#aaa;'>quedan " + str(days_left) + " días</span>"
            else:
                due_str = ""
            lines += "• <b>" + t["text"] + "</b> <small>(" + s["short"] + due_str + ")</small><br>"
        st.markdown(
            '<div style="background:#3d3000;border-left:4px solid #f0a500;border-radius:8px;padding:12px 16px;">'
            '⚠️ Tenés <b>' + str(len(pending_tasks)) + '</b> tarea(s) pendiente(s):<br><br>'
            + lines +
            '</div>',
            unsafe_allow_html=True
        )

    proximos = sorted([p for p in get_all_parciales() if (p["fecha"] - today).days >= 0], key=lambda p: p["fecha"])
    if proximos:
        lines_p = ""
        for p in proximos:
            s = SUBJECTS[p["subj"]]
            days_left = (p["fecha"] - today).days
            if days_left == 0:
                color = "#ff6b6b"; texto = "¡ES HOY!"
            elif days_left <= 7:
                color = "#ff6b6b"; texto = "faltan <b>" + str(days_left) + "</b> días"
            elif days_left <= 14:
                color = "#f0a500"; texto = "faltan <b>" + str(days_left) + "</b> días"
            else:
                color = "#aaa";    texto = "faltan <b>" + str(days_left) + "</b> días"
            lines_p += (
                "• <b>" + p["nombre"] + "</b>"
                " <small>(" + p["fecha"].strftime("%d/%m/%Y") + " — "
                "<span style='color:" + color + ";'>" + texto + "</span>)</small><br>"
            )
        st.markdown(
            '<div style="background:#4a1010;border-left:4px solid #ff4b4b;border-radius:8px;padding:12px 16px;margin-top:8px;">'
            '📅 Parciales próximos:<br><br>' + lines_p +
            '</div>',
            unsafe_allow_html=True
        )
    
    if wd == 6:
        st.info("Domingo libre. Descansa y preparate para la semana!")
    else:
        hoy_classes = [c for c in CLASSES if c["day"] == wd]
        if hoy_classes:
            st.markdown("**Clases de hoy:**")
            badge_html = ""
            for c in hoy_classes:
                s = SUBJECTS[c["subj"]]
                badge_html += (
                    '<span class="class-badge" style="background:' + s["bg"] + ';border:1.5px solid ' + s["color"] + ';">'
                    + "Clase " + s["short"] + " &nbsp;·&nbsp; " + c["start"] + "-" + c["end"] + " &nbsp;·&nbsp; " + c["aula"]
                    + "</span> "
                )
            st.markdown(badge_html, unsafe_allow_html=True)
            st.markdown("")

        blocks      = get_blocks(wd)
        study_b     = [b for b in blocks if b["subj"] != "lunch"]
        total_m_day = sum(minutes_between(b["start"], b["end"]) for b in study_b)
        done_count  = sum(
            1 for i, b in enumerate(blocks)
            if b["subj"] != "lunch" and data["done_blocks"].get(block_id(today, i), False)
        )

        st.markdown("**Bloques de estudio — " + fmt_dur(total_m_day) + " totales:**")

        for i, b in enumerate(blocks):
            bid     = block_id(today, i)
            is_done = data["done_blocks"].get(bid, False)
            s       = SUBJECTS.get(b["subj"], SUBJECTS["py"])
            dur_min = minutes_between(b["start"], b["end"])

            if b["subj"] == "lunch":
                st.markdown(
                    '<div class="block-card lunch-card" style="background:#f5f5f0;border-left-color:#aaa;">'
                    '<span class="block-time">  ' + b["start"] + " - " + b["end"] + "</span> "
                    '<span class="block-title">' + b["title"] + "</span></div>",
                    unsafe_allow_html=True
                )
            else:
                done_cls = "done-block" if is_done else ""
                col_b, col_btn = st.columns([6, 1])
                with col_b:
                    st.markdown(
                        '<div class="block-card ' + done_cls + '" style="background:' + s["bg"] + ';border-left-color:' + s["color"] + ';">'
                        '<span class="block-dur">' + fmt_dur(dur_min) + "</span>"
                        '<div class="block-time">' + b["start"] + " - " + b["end"] + "</div>"
                        '<div class="block-title">' + b["title"] + "</div>"
                        '<div class="block-sub">' + b["sub"] + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                with col_btn:
                    lbl = "OK" if is_done else "---"
                    if st.button(lbl, key="hoy_" + bid):
                        toggle_block(bid)
                        st.rerun()

        st.markdown("---")
        pct = done_count / len(study_b) if study_b else 0
        st.progress(pct, text="Progreso: " + str(done_count) + "/" + str(len(study_b)) + " bloques completados")
    

# ═══════════════════════════════════════════════════════════════════════════════
# SEMANA
# ═══════════════════════════════════════════════════════════════════════════════
with tab_semana:
    leg = ""
    for s in SUBJECTS.values():
        leg += '<span class="legend-dot" style="background:' + s["color"] + '"></span>'
        leg += '<small style="margin-right:14px;color:#555">' + s["short"] + "</small>"
    st.markdown(leg, unsafe_allow_html=True)
    st.markdown("")

    for d in week_dates[:6]:
        wd2      = d.weekday()
        is_today = d == today
        blocks   = get_blocks(wd2)
        study_b2 = [b for b in blocks if b["subj"] != "lunch"]
        total_m2 = sum(minutes_between(b["start"], b["end"]) for b in study_b2)
        done_d   = sum(
            1 for i, b in enumerate(blocks)
            if b["subj"] != "lunch" and data["done_blocks"].get(block_id(d, i), False)
        )

        prefix   = "HOY  " if is_today else ""
        label    = prefix + DAY_NAMES[wd2] + " " + d.strftime("%d/%m") + "  —  " + fmt_dur(total_m2) + "  ·  " + str(done_d) + "/" + str(len(study_b2)) + " bloques"

        with st.expander(label, expanded=is_today):
            day_cls = [c for c in CLASSES if c["day"] == wd2]
            if day_cls:
                badge_html = ""
                for c in day_cls:
                    s = SUBJECTS[c["subj"]]
                    badge_html += (
                        '<span class="class-badge" style="background:' + s["bg"] + ';border:1.5px solid ' + s["color"] + ';">'
                        + "Clase " + s["short"] + " · " + c["start"] + "-" + c["end"] + " · " + c["aula"]
                        + "</span> "
                    )
                st.markdown(badge_html, unsafe_allow_html=True)
                st.markdown("")

            for i, b in enumerate(blocks):
                bid2    = block_id(d, i)
                is_done = data["done_blocks"].get(bid2, False)
                s       = SUBJECTS.get(b["subj"], SUBJECTS["py"])
                dur_min = minutes_between(b["start"], b["end"])

                if b["subj"] == "lunch":
                    st.markdown(
                        '<div class="block-card lunch-card" style="background:#f5f5f0;border-left-color:#aaa;">'
                        '<span class="block-time">' + b["start"] + " - " + b["end"] + "</span> "
                        '<span class="block-title">' + b["title"] + "</span></div>",
                        unsafe_allow_html=True
                    )
                else:
                    done_cls = "done-block" if is_done else ""
                    cb, cbtn = st.columns([6, 1])
                    with cb:
                        st.markdown(
                            '<div class="block-card ' + done_cls + '" style="background:' + s["bg"] + ';border-left-color:' + s["color"] + ';">'
                            '<span class="block-dur">' + fmt_dur(dur_min) + "</span>"
                            '<div class="block-time">' + b["start"] + " - " + b["end"] + "</div>"
                            '<div class="block-title">' + b["title"] + "</div>"
                            '<div class="block-sub">' + b["sub"] + "</div>"
                            "</div>",
                            unsafe_allow_html=True
                        )
                    with cbtn:
                        lbl2 = "OK" if is_done else "---"
                        if st.button(lbl2, key="sem_" + d.isoformat() + "_" + str(i)):
                            toggle_block(bid2)
                            st.rerun()

            pct_d = done_d / len(study_b2) if study_b2 else 0
            st.progress(pct_d, text=str(done_d) + "/" + str(len(study_b2)) + " bloques")

# ═══════════════════════════════════════════════════════════════════════════════
# PARCIALES
# ═══════════════════════════════════════════════════════════════════════════════

with tab_parciales:
    st.subheader("Parciales")

    extras = data.get("parciales_extra", [])

    for p in sorted(get_all_parciales(), key=lambda x: x["fecha"]):
        s = SUBJECTS[p["subj"]]
        days_left = (p["fecha"] - today).days

        if days_left < 0:
            estado = "Finalizado"; color_estado = "#aaa"
        elif days_left == 0:
            estado = "¡Hoy!"; color_estado = "#ff6b6b"
        elif days_left <= 7:
            estado = "¡Muy pronto!"; color_estado = "#ff6b6b"
        elif days_left <= 14:
            estado = "Próximo"; color_estado = "#f0a500"
        else:
            estado = "Pendiente"; color_estado = "#4caf50"

        extra_idx = next(
            (i for i, e in enumerate(extras) if e["nombre"] == p["nombre"] and e["fecha"] == str(p["fecha"])),
            None
        )

        cols = st.columns([6, 1]) if extra_idx is not None else [st.container(), None]

        with cols[0]:
            st.markdown(
                '<div style="background:' + s["bg"] + ';border-left:5px solid ' + s["color"] + ';'
                'border-radius:10px;padding:14px 18px;margin-bottom:12px;color:#1a1a1a;">'
                '<div style="display:flex;justify-content:space-between;align-items:center;">'
                '<div>'
                '<div style="font-size:16px;font-weight:700;color:' + s["color"] + ';">' + p["nombre"] + '</div>'
                '<div style="font-size:13px;margin-top:4px;color:#1a1a1a;">' + p["fecha"].strftime("%A %d/%m/%Y") + '</div>'
                '</div>'
                '<div style="text-align:right;">'
                '<div style="font-size:22px;font-weight:800;color:' + color_estado + ';">' + str(max(days_left, 0)) + ' días</div>'
                '<div style="font-size:12px;color:' + color_estado + ';">' + estado + '</div>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )

        if extra_idx is not None:
            with cols[1]:
                st.markdown(
                    '<div style="display:flex;align-items:center;justify-content:center;height:100%;padding-top:18px;">'
                    '<span></span></div>',
                    unsafe_allow_html=True
                )
                if st.button("🗑️", key="del_parcial_" + str(extra_idx)):
                    data["parciales_extra"].pop(extra_idx)
                    save_data(data)
                    st.rerun()

    st.markdown("---")
    st.markdown("**Agregar parcial:**")
    with st.form("add_parcial_form", clear_on_submit=True):
        cp1, cp2, cp3 = st.columns([3, 2, 2])
        with cp1:
            p_nombre = st.text_input("Nombre", placeholder="Ej: Segundo parcial Física")
        with cp2:
            p_subj = st.selectbox("Materia", options=list(SUBJECTS.keys()), format_func=lambda k: SUBJECTS[k]["short"])
        with cp3:
            p_fecha = st.date_input("Fecha", value=None)
        if st.form_submit_button("Agregar") and p_nombre.strip() and p_fecha:
            data.setdefault("parciales_extra", []).append({
                "subj": p_subj,
                "nombre": p_nombre.strip(),
                "fecha": str(p_fecha)
            })
            save_data(data)
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# MIS CLASES
# ═══════════════════════════════════════════════════════════════════════════════
with tab_cursada:
    st.subheader("Mis clases de cursada")
    st.caption("Horario semanal de clases universitarias")

    # Tabla visual por materia
    st.markdown("---")

    # Agrupar clases por materia
    clases_por_materia = {}
    for c in CLASSES:
        k = c["subj"]
        if k not in clases_por_materia:
            clases_por_materia[k] = []
        clases_por_materia[k].append(c)

    for subj_key, clases in clases_por_materia.items():
        s = SUBJECTS[subj_key]
        total_clase_min = sum(minutes_between(c["start"], c["end"]) for c in clases)

        rows_html = ""
        for c in clases:
            dia = DAY_NAMES[c["day"]]
            dur = minutes_between(c["start"], c["end"])
            rows_html += (
                '<div style="display:flex;align-items:center;gap:12px;padding:5px 0;'
                'border-top:1px solid rgba(128,128,128,0.3);">'
                '<span style="min-width:90px;font-weight:600;font-size:13px;">' + dia + '</span>'
                '<span style="min-width:120px;font-size:13px;">' + c["start"] + " - " + c["end"] + '</span>'
                '<span style="min-width:80px;font-size:12px;opacity:.7;">' + fmt_dur(dur) + '</span>'
                '<span style="font-size:12px;opacity:.7;">' + c["aula"] + '</span>'
                '</div>'
            )

        st.markdown(
            '<div style="background:' + s["bg"] + ';border-left:5px solid ' + s["color"] + ';'
            'border-radius:10px;padding:14px 18px;margin-bottom:12px;color:#1a1a1a;">'
            '<div style="font-size:16px;font-weight:700;margin-bottom:8px;color:' + s["color"] + ';">'
            + s["name"] +
            '</div>'
            + rows_html +
            '</div>',
            unsafe_allow_html=True
        )

    # Resumen semanal de horas de clase
    st.markdown("---")
    st.markdown("**Resumen de carga horaria:**")

    total_cls_min = sum(minutes_between(c["start"], c["end"]) for c in CLASSES)
    col_r1, col_r2, col_r3 = st.columns(3)
    col_r1.metric("Horas de clase / semana", fmt_dur(total_cls_min))
    col_r2.metric("Horas de estudio / semana", fmt_dur(total_study_min))
    col_r3.metric("Total carga semanal", fmt_dur(total_cls_min + total_study_min))

    # Tabla resumen por dia
    st.markdown("---")
    st.markdown("**Vista por dia:**")

    dias_con_clase = sorted(set(c["day"] for c in CLASSES))
    for wd_c in dias_con_clase:
        clases_dia = [c for c in CLASSES if c["day"] == wd_c]
        mins_dia   = sum(minutes_between(c["start"], c["end"]) for c in clases_dia)
        badge_html = (
            '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;flex-wrap:wrap;">'
            '<span style="font-weight:700;font-size:14px;min-width:90px;color:inherit;">'
            + DAY_NAMES[wd_c] + '</span>'
        )
        for c in clases_dia:
            s = SUBJECTS[c["subj"]]
            badge_html += (
                '<span style="background:' + s["bg"] + ';border:1.5px solid ' + s["color"] + ';'
                'padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;color:#1a1a1a;">'
                + s["short"] + " " + c["start"] + "-" + c["end"] +
                '</span>'
            )
        badge_html += (
            '<span style="font-size:12px;opacity:.6;color:inherit;">' + fmt_dur(mins_dia) + '</span>'
            '</div>'
        )
        st.markdown(badge_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESO
# ═══════════════════════════════════════════════════════════════════════════════
with tab_progreso:
    st.subheader("Progreso semanal")

    totals_min = {k: 0 for k in SUBJECTS}
    dones_min  = {k: 0 for k in SUBJECTS}
    totals_blk = {k: 0 for k in SUBJECTS}
    dones_blk  = {k: 0 for k in SUBJECTS}

    for d in week_dates[:6]:
        blocks = get_blocks(d.weekday())
        for i, b in enumerate(blocks):
            if b["subj"] not in SUBJECTS:
                continue
            m = minutes_between(b["start"], b["end"])
            totals_min[b["subj"]] += m
            totals_blk[b["subj"]] += 1
            if data["done_blocks"].get(block_id(d, i), False):
                dones_min[b["subj"]] += m
                dones_blk[b["subj"]] += 1

    t_min_all = sum(totals_min.values())
    d_min_all = sum(dones_min.values())
    pct_all   = int(d_min_all / t_min_all * 100) if t_min_all else 0

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Horas planificadas", str(round(t_min_all / 60, 1)) + " hs")
    m2.metric("Horas completadas",  str(round(d_min_all / 60, 1)) + " hs")
    m3.metric("Progreso",           str(pct_all) + "%")
    m4.metric("Dias de estudio",    "6  (Lun-Sab)")

    st.markdown("---")
    st.markdown("**Por materia:**")

    for key, s in SUBJECTS.items():
        t_m = totals_min[key]
        d_m = dones_min[key]
        t_b = totals_blk[key]
        d_b = dones_blk[key]
        pct = int(d_m / t_m * 100) if t_m else 0

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(
                '<span class="legend-dot" style="background:' + s["color"] + '"></span>**' + s["short"] + "**",
                unsafe_allow_html=True
            )
            st.progress(
                pct / 100,
                text=str(round(d_m/60,1)) + "/" + str(round(t_m/60,1)) + " hs  ·  " + str(d_b) + "/" + str(t_b) + " bloques  (" + str(pct) + "%)"
            )
        with col2:
            st.metric("", str(pct) + "%", label_visibility="hidden")

    st.markdown("---")
    if st.button("Resetear semana"):
        for d in week_dates[:6]:
            for i in range(len(get_blocks(d.weekday()))):
                bid = block_id(d, i)
                if bid in data["done_blocks"]:
                    del data["done_blocks"][bid]
        save_data(data)
        st.success("Semana reseteada.")
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# TAREAS
# ═══════════════════════════════════════════════════════════════════════════════
with tab_tareas:
    st.subheader("Tareas y pendientes")

    with st.form("add_task_form", clear_on_submit=True):
        ct, cs, cd = st.columns([3, 2, 2])
        with ct:
            task_text = st.text_input("Descripcion", placeholder="Ej: Resolver guia TP3")
        with cs:
            task_subj = st.selectbox(
                "Materia", options=list(SUBJECTS.keys()),
                format_func=lambda k: SUBJECTS[k]["short"]
            )
        with cd:
            task_due = st.date_input("Fecha de entrega", value=None)
        if st.form_submit_button("Agregar") and task_text.strip():
            add_task(task_text.strip(), task_subj, task_due)
            st.rerun()

    st.markdown("---")

    if not data["tasks"]:
        st.info("No hay tareas cargadas. Agrega una arriba.")
    else:
        pending   = [(i, t) for i, t in enumerate(data["tasks"]) if not t["done"]]
        completed = [(i, t) for i, t in enumerate(data["tasks"]) if t["done"]]

        if pending:
            st.markdown("**Pendientes — " + str(len(pending)) + " tarea(s):**")
            for i, t in pending:
                s       = SUBJECTS.get(t["subj"], SUBJECTS["py"])
                due_str = "  ·  " + t["due"] if t.get("due") else ""
                cc, cb, cd2 = st.columns([5, 1, 1])
                with cc:
                    st.markdown(
                        '<div class="block-card" style="background:' + s["bg"] + ';border-left-color:' + s["color"] + ';">'
                        '<div class="block-title">' + t["text"] + "</div>"
                        '<div class="block-sub">' + s["short"] + due_str + "</div>"
                        "</div>",
                        unsafe_allow_html=True
                    )
                with cb:
                    if st.button("Hecho", key="tc_" + str(i)):
                        toggle_task(i); st.rerun()
                with cd2:
                    if st.button("Borrar", key="td_" + str(i)):
                        delete_task(i); st.rerun()

        if completed:
            with st.expander("Completadas (" + str(len(completed)) + ")"):
                for i, t in completed:
                    s = SUBJECTS.get(t["subj"], SUBJECTS["py"])
                    cc2, cb2, cd3 = st.columns([5, 1, 1])
                    with cc2:
                        st.markdown(
                            '<div class="block-card done-block" style="background:' + s["bg"] + ';border-left-color:' + s["color"] + ';">'
                            '<div class="block-title">' + t["text"] + "</div>"
                            '<div class="block-sub">' + s["short"] + "</div>"
                            "</div>",
                            unsafe_allow_html=True
                        )
                    with cb2:
                        if st.button("Deshacer", key="tu_" + str(i)):
                            toggle_task(i); st.rerun()
                    with cd3:
                        if st.button("Borrar", key="td2_" + str(i)):
                            delete_task(i); st.rerun()