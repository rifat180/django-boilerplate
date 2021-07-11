def form_error(errors):
    error_list = []
    for title, errors in errors.items():
        title = " ".join([x.title() for x in title.split("_")])
        for error in errors:
            error_list.append(f"{title}: {error.get('message')}")
    return error_list
