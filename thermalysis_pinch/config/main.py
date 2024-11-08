STORE_ID = "pinch" + "_store"
PROJECT_NAME = "pinch".replace("_", " ").title()
PROJECT_SLUG = "pinch"

CONFIG_SIDEBAR = {
    "logo_path": "/pinch/assets/logo_horizontal.png",
    "sidenav_title": "STEPS",
    "nav_items": [
        {"name": "Data Collection", "path": "pi-data"},
        {"name": "Pinch Point Temperature ", "path": "pi-pinchet"},
        {"name": "Temperature Interval Diagram", "path": "pi-tid"},
        {"name": "Problem Table", "path": "pi-ptable"},
        {"name": "Heat Cascade", "path": "pi-hcas"},
        {
            "name": "The Shifted Temperature-Enthalpy Composite Diagram ",
            "path": "pi-stec",
        },
        {"name": "The Temperature-Enthalpy Composite Diagram", "path": "pi-tecd"},
        {"name": "The Grand Composite Curve", "path": "pi-gcc"},
        {"name": "Report", "path": "pi-report"},
    ],
}
