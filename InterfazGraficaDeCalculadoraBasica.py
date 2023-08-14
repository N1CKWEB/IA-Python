import PySimpleGUI as nd

layout = [
    [nd.Text('Valor 1'), nd.InputText(key="val1")],
    [nd.Text('Valor 2'), nd.InputText(key="val2")],
    [nd.Button('+'), nd.Button('-'), nd.Button('*'), nd.Button('/')],
    [nd.Text('Resultado'), nd.Text('', key='result')],
    [nd.Button('Salir')]
]
window = nd.Window('Calculadora', layout, margins=(10, 10))
while True:
    event, values = window.read()
    if event == '+':
        window["result"].update(float(values['val1']) + float(values['val2']))
    if event == '-':
        window["result"].update(float(values['val1']) - float(values['val2']))
    if event == '*':
        window["result"].update(float(values['val1']) * float(values['val2']))
    if event == '/':
        window["result"].update(float(values['val1']) / float(values['val2']))
    if event == "Salir" or event == nd.WIN_CLOSED:
        break
window.close()