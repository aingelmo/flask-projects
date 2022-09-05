from flask import Blueprint, render_template
from flask_login import current_user

base_app = Blueprint("views", __name__)

top_menus = [
    {"path": "/", "title": "Home"},
    {"path": "/auth/login", "title": "Login"},
    {"path": "/auth/register", "title": "Register"},
]


@base_app.route("/")
def index():
    """Landing Page."""
    return render_template("views/index.html", top_menu_items=get_top_menu_items("/"))


def get_top_menu_items(current_path: str = "/"):
    """Get html template for top menu items."""
    items = []

    # if current_user.is_authenticated:
    #     top_menus = [
    #         {"path": "/", "title": "Home"},
    #         {"path": "/auth/logout", "title": "Logout"},
    #     ]
    # else:
    #     top_menus = [
    #         {"path": "/", "title": "Home"},
    #         {"path": "/auth/login", "title": "Login"},
    #         {"path": "/auth/register", "title": "Register"},
    #     ]

    for menu in top_menus:
        link_class_name = "nav-link"

        if menu["path"] == "/":
            items.append(
                f'<li class="nav-item"><a class="nav-link active" aria-current="page" href={menu["path"]}>{menu["title"]}</a></li>'
            )

        else:
            items.append(
                f'<li class="nav-item"><a href="{menu["path"]}" class="{link_class_name}">{menu["title"]}</a></li>'
            )

    return "\n".join(items)
