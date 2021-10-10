#!/usr/bin/env python3

import sys
import json
import unicodedata

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

# https://stackoverflow.com/a/517974
def normalize_to_ascii(string):
    norm_unicode = unicodedata.normalize("NFKD", string)
    return norm_unicode.encode("ASCII", "ignore").decode()

strings = {}

json_path = sys.argv[1] if len(sys.argv) > 1 else "wallpapers.json"
with open(json_path, "r") as f:
    wallpapers_data = json.load(f)

with open("res/xml/wallpapers.xml", "w+") as f:
    f.write(WALLPAPERS_XML_HEADER)

    for category_name, cat_info in wallpapers_data.items():
        category_id = category_name.lower().replace(" ", "_")
        strings[f"category_{category_id}"] = category_name

        f.write(f"""

    <category id="{category_id}" title="@string/category_{category_id}" featured="{cat_info['featured']}">""")

        for set_name, wallpapers in cat_info["wallpapers"].items():
            set_id = normalize_to_ascii(set_name).lower().replace(" ", "_").replace("'", "").replace("-", "_")

            for wp_id, wp_name in sorted(wallpapers.items(), key=lambda w: w[1]):
                # Ignore special override keys
                if wp_id == "author" or wp_id == "url":
                    continue

                # Get contextual author
                author = wallpapers["author"] if "author" in wallpapers else cat_info["author"]
                author_id = normalize_to_ascii(author).lower().replace(" ", "_").replace("'", "")
                strings[f"author_{author_id}"] = f"by {author}"

                wp_res_id = f"{category_id}_{set_id}_{wp_id}"

                wp_user_name = set_name
                if wp_name:
                    wp_user_name += f" · {wp_name}"
                strings[f"wallpaper_{wp_res_id}"] = wp_user_name

                # Open tag and write common attributes
                f.write(f"""

        <static-wallpaper
            id="{wp_res_id}"
            src="@drawable/{wp_res_id}"
            title="@string/wallpaper_{wp_res_id}"
            subtitle1="@string/author_{author_id}\"""")

                # Add action URL, if available
                if "url" in wallpapers:
                    strings[f"url_{wp_res_id}"] = wallpapers["url"]

                    f.write(f"""
            actionUrl="@string/url_{wp_res_id}\"""")

                # End tag
                f.write(" />")

        f.write("""

    </category>""")

    f.write(WALLPAPERS_XML_FOOTER)

with open("res/values/wallpaper_strings.xml", "w+") as f:
    f.write(STRINGS_XML_HEADER)

    for str_id, value in strings.items():
        escaped = value.replace("'", r"\'").replace("&", "&amp;")
        f.write(f"""
    <string name="{str_id}">{escaped}</string>""")

    f.write(STRINGS_XML_FOOTER)
