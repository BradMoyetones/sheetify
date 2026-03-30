class Theme:
    # Tokens de diseño
    COLORS = {
        "primary": "#0ea5e9",      # Sky-500
        "bg_dark": "#0f172a",      # Slate-900
        "bg_card": "#1e293b",      # Slate-800
        "text_main": "#f8fafc",    # Slate-50
        "text_muted": "#94a3b8"    # Slate-400
    }

    @staticmethod
    def get_button_style(variant="primary"):
        # Esto es como el "cva" o "tailwind-variants" de React
        base = """
            QPushButton {
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
        """
        if variant == "primary":
            return base + f"""
                QPushButton {{
                    background-color: {Theme.COLORS['primary']};
                    color: white;
                }}
                QPushButton:hover {{ background-color: #38bdf8; }}
            """
        return base