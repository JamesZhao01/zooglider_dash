from app import app, server
from jeff.mapping_tool import layout

app.layout = layout

if __name__ == '__main__':
    app.run_server(debug=True)
