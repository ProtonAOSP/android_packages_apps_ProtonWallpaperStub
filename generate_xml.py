#!/usr/bin/env python3


WALLPAPERS = {
    "Radiant Glow": {
        "author": "Infinitum",
        "featured": "radiant_glow_rings_1",
        "wallpapers": {
            "Arrow": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
            "Gem": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
            "Hex": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
            "Geometric": {
                "1": "Forest",
                "2": "Flame",
                "3": "Ocean",
            },
            "Orbit": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
            "Rings": {
                "1": "Forest",
                "2": "Flame",
                "3": "Ocean",
            },
            "Square": {
                "1": "Ocean",
                "2": "Flame",
                "3": "Forest",
            },
            "Tilt": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
            "Cross": {
                "1": "Flame",
                "2": "Forest",
                "3": "Ocean",
            },
        },
    },
    "Space": {
        "author": "Infinitum",
        "featured": "space_strange_landscape_1",
        "wallpapers": {
            "As Seen From Mars": {
                "1": "",
            },
            "Blue Giant": {
                "1": "",
            },
            "Strange Solar Planets": {
                "1": "",
            },
            "Strange Landscape": {
                "1": "",
            },
        },
    },
    "Strange Dimension": {
        "author": "Infinitum",
        "featured": "strange_dimension_vortex_3",
        "wallpapers": {
            "Vortex": {
                "1": "Flat",
                "2": "Flower",
                "3": "Portal",
                "4": "Sun",
            },
            "Fractal": {
                "1": "Hypnotic",
                "2": "Rotor",
                "3": "Star",
                "4": "Disaster",
                "5": "Crimson Blue",
            },
            "Warped": {
                "1": "",
                "2": "Corrupted",
                "3": "Flare",
                "4": "Fluid",
                "5": "Matter",
                "6": "Stars",
                "7": "Corrupted Fluid",
            },
        },
    },
}

WALLPAPERS_XML_HEADER = """<?xml version="1.0" encoding="utf-8" ?>
<!--
    Copyright (C) 2020 The Proton AOSP Project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<wallpapers>"""

WALLPAPERS_XML_FOOTER = """

</wallpapers>
"""

STRINGS_XML_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<!--
    Copyright (C) 2020 The Proton AOSP Project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
-->
<resources>"""

STRINGS_XML_FOOTER = """
</resources>
"""

strings = {}

with open("res/xml/wallpapers.xml", "w+") as f:
    f.write(WALLPAPERS_XML_HEADER)

    for category_name, cat_info in WALLPAPERS.items():
        category_id = category_name.lower().replace(" ", "_")
        strings[f"category_{category_id}"] = category_name

        author = cat_info["author"]
        author_id = author.lower().replace(" ", "_")
        strings[f"author_{author_id}"] = f"by {author}"

        f.write(f"""

    <category id="{category_id}" title="@string/category_{category_id}" featured="{cat_info['featured']}">""")

        for set_name, wallpapers in cat_info["wallpapers"].items():
            set_id = set_name.lower().replace(" ", "_")

            for wp_id, wp_name in sorted(wallpapers.items(), key=lambda w: w[1]):
                wp_res_id = f"{category_id}_{set_id}_{wp_id}"

                wp_user_name = set_name
                if wp_name:
                    wp_user_name += f" \u2022 {wp_name}"
                strings[f"wallpaper_{wp_res_id}"] = wp_user_name

                f.write(f"""

        <static-wallpaper
            id="{wp_res_id}"
            src="@drawable/{wp_res_id}"
            title="@string/wallpaper_{wp_res_id}"
            subtitle1="@string/author_{author_id}" />""")

        f.write("""

    </category>""")

    f.write(WALLPAPERS_XML_FOOTER)

with open("res/values/wallpaper_strings.xml", "w+") as f:
    f.write(STRINGS_XML_HEADER)

    for str_id, value in strings.items():
        f.write(f"""
    <string name="{str_id}">{value}</string>""")

    f.write(STRINGS_XML_FOOTER)
