def parse_query(query):

    result = {

        "text": "",
        "extension": None,
        "language": None,
        "exact": False
    }

    parts = query.split()

    text_parts = []

    for part in parts:

        if part.startswith("ext:"):

            result["extension"] = (
                part.replace(
                    "ext:",
                    ""
                )
            )

        elif part.startswith("lang:"):

            result["language"] = (
                part.replace(
                    "lang:",
                    ""
                )
            )

        else:

            text_parts.append(
                part
            )

    result["text"] = " ".join(
        text_parts
    )

    if (
        result["text"].startswith('"')
        and
        result["text"].endswith('"')
    ):

        result["exact"] = True

        result["text"] = (
            result["text"]
            .replace('"', '')
        )

    return result