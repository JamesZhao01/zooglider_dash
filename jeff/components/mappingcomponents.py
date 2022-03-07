from collections import defaultdict
import os
import imagesize
from dash import html, dcc
from app import config

dataset_type_options = ["Zooglider", "Zooscan", "UVP"]
mapping = {"Zooglider": [], "Zooscan": [], "UVP": []}
for f in os.listdir(config["datasets"]):
    if not os.path.isdir(os.path.join(config["datasets"], f)):
        continue
    lower = f.lower()
    if lower.startswith("uvp"):
        mapping["UVP"].append(f)
    elif lower.startswith("zooscan"):
        mapping["Zooscan"].append(f)
    else:
        mapping["Zooglider"].append(f)


def default_dd(id):
    default = [{"label": "None", "value": "None"}]
    return dcc.Dropdown(
        id=id,
        value="None",
        clearable=False,
        disabled=True,
        options=default
    )


def create_ds_dd(id, ds_type):
    assert ds_type in dataset_type_options
    default = [{"label": "None", "value": "None"}]
    return dcc.Dropdown(
        id=id,
        value="None",
        clearable=False,
        options=default + [{"label": f, "value": f} for f in mapping[ds_type]],
    )


def create_class_dd(id, ds):
    default = [{"label": "None", "value": "None"}]
    if not ds or ds == "None":
        return dcc.Dropdown(
            id=id,
            value="None",
            clearable=False,
            disabled=True,
            options=default,
        )
    class_path = os.path.join(config["datasets"], ds)
    # files = [f for f in os.listdir(class_path) if os.path.isdir(
    #     os.path.join(config["datasets"], ds, f))]
    files = [f for f in os.listdir(class_path)]
    return dcc.Dropdown(
        id=id,
        value="None",
        clearable=False,
        options=default + [{"label": f, "value": f} for f in files],
        optionHeight=20
    )


def create_ds_type_dd(id):
    return dcc.Dropdown(
        id=id,
        value="Zooglider",
        clearable=False,
        options=[{
            "label": f,
            "value": f
        } for f in dataset_type_options],
    )


def create_maxsize_in(id):
    return dcc.Input(
        id=id,
        type="number",
        placeholder="Input Load Size",
        value=5000,
        style={"max-width": "100%"}
    )


def create_group_size_in(id):
    return dcc.Input(
        id=id,
        type="number",
        placeholder="Input Group Size",
        value=50,
        style={"max-width": "100%"}
    )


def create_do_sort_dd(id):
    return dcc.Dropdown(
        id=id,
        value="No",
        clearable=False,
        options=[{
            "label": f,
            "value": f
        } for f in ["No", "Asc", "Des"]],
    )


files = defaultdict(list)
ct_per = defaultdict(lambda: 50)


def create_slider(idx, ds, classs, new_ct_per, max_size):
    slider_id = {"type": "slider", "index": idx}
    ct_per[idx] = new_ct_per
    if not ds or not classs or not max_size or ds == "None" or classs == "None":
        return dcc.Slider(id=slider_id, min=-1, max=-1, disabled=True)

    images_path = os.path.join(config["datasets"], ds, classs)
    files[idx] = sorted(list(os.listdir(images_path)))

    if max_size > 0:
        files[idx] = files[idx][:max_size]
    slider = dcc.Slider(id=slider_id, min=0, max=(len(
        files[idx]) - 1) // ct_per[idx], step=1, value=0)
    return slider


# def create_grid(idx, ds, classs, max_size):
#     '''
#     Builds Slider, Wrapper for images
#     '''
#     files[idx] = []

#     if not ds or not classs or not max_size or not idx or ds == "None" or classs == "None":
#         return html.Div()
#     slider_id = {"type": "slider", "index": idx}
#     images_id = {"type": "images", "index": idx}

#     images_path = os.path.join(config["datasets"], ds, classs)
#     files[idx] = sorted(list(os.listdir(images_path)))

#     if max_size > 0:
#         files[idx] = files[idx][:max_size]

#     slider = dcc.Slider(id=slider_id, min=0, max=len(
#         files[idx]) // ct_per[idx], step=1, value=0)
#     return html.Div(children=[
#         slider,
#         html.Div(id=images_id)
#     ])


def create_max_width(idx):
    max_width_id = {"type": "max_width", "index": idx}
    slider = dcc.Slider(id=max_width_id, min=0, max=100, step=5, value=25)
    return slider


def create_images(idx, ds, classs, page, do_sort, width):
    '''
    Builds Images, Indicator
    '''
    if not ds or not classs or page == None or not do_sort or ds == "None" or classs == "None" or page < 0:
        return html.Div()
    left = page*ct_per[idx]
    right = (page + 1) * ct_per[idx]
    subset = files[idx][left: right]

    if do_sort != "No":

        samples_path = os.path.join(config["datasets"], ds, classs)
        sizes = [-imagesize.get(os.path.join(samples_path, f))[1]
                 for f in subset]
        _, subset = zip(*sorted(list(zip(sizes, subset))))

        if do_sort == "Asc":
            subset = reversed(subset)

    indicator_text = f"[{left}, {min(right, len(files[idx])) - 1}] / {len(files[idx])}"
    imgs = html.Div(style={"height": "75vh"}, className="overflow-auto", children=[html.Img(src=f"static/{ds}/{classs}/{f}", title=f,
                                                                                            style={"max-width": f"{width}%", "border": "1px solid cyan"}) for f in subset])
    return html.Div(children=[indicator_text, imgs])
