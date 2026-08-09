from django.utils.translation import gettext_lazy as _
from django.templatetags.static import static



UNFOLD = {
    "DASHBOARD_TEMPLATE": "dashboard.html",
    "SITE_TITLE": "Admin Dashboard",
    "SITE_HEADER": "Administration",
    "SITE_SYMBOL": "admin_panel_settings",
    "LOGO": "ADMIN",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_SITE_HEADER": True,
    
    "FORMS": {
    "INLINE_ACTIONS": True,
},
      "SITE_ICON": {
        "light": "ADMIN",  # light mode
        "dark": "ADMIN",  # dark mode
    },
    # "SITE_LOGO": "logo.svg"),  # both modes, optimise for 32px height
    "SITE_LOGO": {
        "light": "ADMIN",  # light mode
        "dark": "ADMIN",  # dark mode
    },
   
    "THEME": "light",
    "ACTIONS": {
        "ENABLE_DELETE": True,
        "ENABLE_ADD": True,
        "ENABLE_CHANGE": True,
        "ENABLE_BULK_DELETE": True,
    },

    "ENVIRONMENT": "Development",

    "LOGIN": {
        "redirect_after": lambda request: "/admin/",
    },
    "STYLES": [
        lambda request: static("css/custom_admin.css"),
    ],
    "SCRIPTS": [
        "/static/js/ckeditor-media.js",
        "/admin/media-data-js/",
    ],
    
   "BORDER_RADIUS": "6px",
   "COLORS": {
    "base": {
        "50": "oklch(98.5% .002 247.839)",
        "100": "oklch(96.7% .003 264.542)",
        "200": "oklch(92.8% .006 264.531)",
        "300": "oklch(87.2% .01 258.338)",
        "400": "oklch(70.7% .022 261.325)",
        "500": "oklch(55.1% .027 264.364)",
        "600": "oklch(44.6% .03 256.802)",
        "700": "oklch(37.3% .034 259.733)",
        "800": "oklch(27.8% .033 256.848)",
        "900": "oklch(21% .034 264.665)",
        "950": "oklch(13% .028 261.692)",
    },

    # 🌟 Primary: Gold / Amber tone (#CEA664)
    "primary": {
        "50": "oklch(97% .02 85)",     # very light cream
        "100": "oklch(93% .04 85)",    # pale gold
        "200": "oklch(88% .06 85)",    # soft gold
        "300": "oklch(82% .09 85)",    # warm sand
        "400": "oklch(77% .13 85)",    # main gold (#CEA664)
        "500": "oklch(70% .15 85)",    # richer tone
        "600": "oklch(63% .14 85)",    # deeper amber
        "700": "oklch(54% .12 85)",    # dark gold
        "800": "oklch(45% .10 85)",    # antique bronze
        "900": "oklch(36% .08 85)",    # shadow gold
        "950": "oklch(26% .06 85)",    # deep brown gold
    },

        "font": {
            "subtle-light": "var(--color-base-500)",  # text-base-500
            "subtle-dark": "var(--color-base-400)",  # text-base-400
            "default-light": "var(--color-base-600)",  # text-base-600
            "default-dark": "var(--color-base-300)",  # text-base-300
            "important-light": "var(--color-base-900)",  # text-base-900
            "important-dark": "var(--color-base-100)",  # text-base-100
        },
    },

    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {"en": "🇺🇸", "bn": "🇧🇩"},
        },
    },

   "SIDEBAR": {
    "show_search": True,
    "show_all_applications": True,
    "navigation": [
        {
            "title": _("User Management"),
            "separator": True,
            "collapsible": True,
            "items": [
                {
                    "title": _("Users"),
                    "icon": "verified_user",
                    "link": "/admin/auths/customuser/",
                },
                {
                    "title": _("Groups"),
                    "icon": "group",
                    "link": "/admin/auth/group/",
                },
            ],
        },

        {
            "title": "Multimedia & News",
            "separator": True,
            "collapsible": True,
            "items": [
                {
                    "title": "Multimedia Assets",
                    "icon": "perm_media",
                    "link": "/admin/multicontent/multimediaasset/"
                },
                {
                    "title": "News Articles",
                    "icon": "article",
                    "link": "/admin/multicontent/newsarticle/"
                },
                {
                    "title": "Content",
                    "icon": "description",
                    "link": "/admin/multicontent/content/"
                },
            ]
        },
    ]
},

    "TABS": [
        
    ],
}
