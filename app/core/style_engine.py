# app/core/style_engine.py
from app.core.tokens import tokens

def get_stylesheet(is_dark=False):
    t = tokens.DARK if is_dark else tokens.LIGHT
    
    return f"""
    /* Estilos Globales */
    QMainWindow {{
        background-color: {t['sidebar']};
    }}

    /* SIDEBAR: Minimalista y sin bordes */
    #sidebar {{
        background-color: {t['sidebar']};
        border: none;
    }}

    #sidebar QPushButton {{
        background-color: transparent;
        color: {t['muted_fg']};
        text-align: left;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 500;
        border: none;
    }}

    #sidebar QPushButton:hover {{
        background-color: {t['accent']};
        color: {t['primary']};
    }}

    /* EL CONTENEDOR INSET: El "truco" de Shadcn */
    #content_wrapper {{
        background-color: {t['background']};
        border: 1px solid {t['border']};
        border-top-left-radius: 16px; /* Radio grande para el look moderno */
        border-bottom-left-radius: 16px;
        /* Si quieres que sea redondeado por los 4 lados, quita el 'left' */
    }}

    /* Botón de Toggle */
    #toggle_btn {{
        background-color: transparent;
        border: none;
        margin-bottom: 20px;
    }}

    /* Inputs y otros elementos heredan de los tokens */
    QLineEdit {{
        background-color: {t['background']};
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
        padding: 8px;
        color: {t['foreground']};
    }}

    /* Labels y Textos */
    QLabel {{
        color: {t['foreground']};
    }}

    QRadioButton {{
        color: {t['foreground']};
        background-color: {t['background']};
        border-radius: {t['radius']};
        padding: 8px;
        border: 1px solid {t['border']};
    }}

    QRadioButton::indicator {{
        width: 14px;
        height: 14px;
        border-radius: 7px;
        border: 2px solid {t['border']};
        background-color: {t['background']};
    }}

    QRadioButton::indicator:checked {{
        background-color: {t['primary']};
        border: 2px solid {t['accent']};
    }}

    /* Botones de Acción (Procesar, Exportar) */
    QPushButton {{
        background-color: {t['primary']};
        color: {t['primary_fg']};
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 14px;
        border: none;
    }}

    QPushButton#destructive {{
        background-color: {t['destructive']};
        color: {t['destructive_fg']};
    }}

    /* El área de scroll donde están los archivos */
    /* 1. El contenedor exterior (bordes y radio) */
    QScrollArea#scroll_area {{
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
        background-color: transparent; /* Importante: que el padre no bloquee */
    }}

    /* 2. LA MAGIA: El viewport y el widget interno */
    /* Targeteamos el widget que vive dentro del scroll area */
    QScrollArea#scroll_area > QWidget > QWidget {{
        background-color: {t['sidebar']};
        border-radius: {t['radius']};
    }}

    /* El estado vacío (Dashed border) */
    QLabel#empty_state {{
        font-size: 14px;
        padding: 40px;
        border: 2px dashed {t['border']};
        border-radius: {t['radius']};
        color: {t['muted_fg']};
    }}

    /* Progress Bar */
    QProgressBar {{
        border: 1px solid {t['border']};
        border-radius: 4px;
        text-align: center;
        background-color: {t['muted']};
    }}
    QProgressBar::chunk {{
        background-color: {t['primary']};
    }}

    QFrame#options_frame {{
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
    }}

    QVBoxLayout#list_layout {{
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
    }}

    QLabel#lbl_original {{
        color: {t['muted_fg']};
    }}

    /* Estilos para ZIP Group */
    QFrame#zip_group {{
        background-color: {t['sidebar']};
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
    }}

    QFrame#file_item {{
        background-color: {t['sidebar']};
        border: 1px solid {t['border']};
        border-radius: {t['radius']};
    }}
    """