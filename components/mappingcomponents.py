from collections import defaultdict
import os
import imagesize
from dash import html, dcc
from appsrc import config

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
        options=default + [{"label": f, "value": f} for f in mapping[ds_type]]
    )


def create_class_dd(id, ds):
    default = [{"label": "None", "value": "None"}]
    if not ds or ds == "None":
        return dcc.Dropdown(
            id=id,
            value="None",
            clearable=False,
            disabled=True,
            options=default
        )
    class_path = os.path.join(config["datasets"], ds)
    files = [f for f in os.listdir(class_path) if os.path.isdir(
        os.path.join(config["datasets"], ds, f))]
    return dcc.Dropdown(
        id=id,
        value="None",
        clearable=False,
        options=default + [{"label": f, "value": f} for f in files]
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


def create_do_sort_dd(id):
    return dcc.Dropdown(
        id=id,
        value="No",
        clearable=False,
        options=[{
            "label": f,
            "value": f
        } for f in ["Yes", "No"]],
    )


files = defaultdict(list)
ct_per = 50


def create_grid(idx, ds, classs, max_size):
    '''
    Builds Slider, Wrapper for images
    '''
    files[idx] = []

    if not ds or not classs or not max_size or not idx or ds == "None" or classs == "None":
        return html.Div()
    slider_id = {"type": "slider", "index": idx}
    images_id = {"type": "images", "index": idx}

    images_path = os.path.join(config["datasets"], ds, classs)
    files[idx] = list(os.listdir(images_path))

    if max_size > 0:
        files[idx] = files[idx][:max_size]

    slider = dcc.Slider(id=slider_id, min=0, max=len(
        files[idx]) // ct_per, step=1, value=0)
    return html.Div(children=[
        slider,
        html.Div(id=images_id)
    ])


def create_images(idx, ds, classs, page, do_sort):
    '''
    Builds Images, Indicator
    '''
    if not ds or not classs or not do_sort or ds == "None" or classs == "None":
        return html.Div()
    left = page*ct_per
    right = (page + 1) * ct_per
    subset = files[idx][left: right]

    if do_sort == "Yes":
        samples_path = os.path.join(config["datasets"], ds, classs)
        sizes = [-imagesize.get(os.path.join(samples_path, f))[1]
                 for f in subset]
        _, subset = zip(*sorted(list(zip(sizes, subset))))

    indicator_text = f"[{left}, {min(right, len(files[idx])) - 1}] / {len(files[idx])}"
    imgs = html.Div(style={"height": "75vh"}, className="overflow-auto", children=[html.Img(src=f"static/{ds}/{classs}/{f}", title=f,
                                                                                            style={"max-width": "500px", "border": "1px solid cyan"}) for f in subset])
    return html.Div(children=[indicator_text, imgs])
