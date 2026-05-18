import flet as ft
import flet_audio as fta
 
preguntas = {
 
    "Literature": {
 
        100: (
            "Who wrote Romeo and Juliet?",
            "william shakespeare"),
 
        200: (
            "What is the name of the magic school in Harry Potter?",
            "hogwarts"),
 
        300: (
            "What animal follows Alice in Alice's Adventures in Wonderland?",
            "white rabbit"),
 
        400: (
            "Who wrote Don Quijote de la Mancha?",
            "miguel de cervantes"),
 
        500: (
            "What literary genre tells long fictional stories?",
            "novel")},
 
    "General Culture": {
 
        100: (
            "What is the capital of France?",
            "paris"),
 
        200: (
            "What planet is known as the Red Planet?",
            "mars"),
 
        300: (
            "How many continents are there in the world?",
            "7"),
 
        400: (
            "In what continent is Brazil located?",
            "south america"),
 
        500: (
            "What is the largest ocean in the world?",
            "pacific ocean")}}
 
puntos = 0
usadas = []
juego = True
 
 
def main(page: ft.Page):
    audio = fta.Audio(
        src="audio/bgmusic.mp4",
        autoplay=True,
        volume=1)
    right_sound = fta.Audio(
        src="audio/right.mp4",
        volume=1)
    wrong_sound = fta.Audio(
        src="audio/wrong.mp4",
        volume=1)
 
    global puntos
    global juego
 
    page.services.append(audio)
    page.services.append(right_sound)
    page.services.append(wrong_sound)
 
    page.title = "Jeopardy"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 750
    page.bgcolor = "#001f3f"
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"
 
    logo = ft.Image(
        src="assets/logo.png",
        width=250,
        height=250,
        fit="contain")
 
    titulo = ft.Text(
        "JEOPARDY",
        size=42,
        weight="bold",
        color="yellow")
 
    score = ft.Text(
        f"Score: {puntos}",
        size=28,
        color="white")
 
    pregunta = ft.Text(
        "Choose a category and value!",
        size=24,
        color="white",
        text_align="center")
 
    resultado = ft.Text(
        "",
        size=22,
        weight="bold")

    correctas = 0
    incorrectas = 0
 
    right_text = ft.Text(
        f"Right Answers: {correctas}",
        size=22,
        color="lightgreen")
    wrong_text = ft.Text(
        f"Wrong Answers: {incorrectas}",
        size=22,
        color="red")
 
    entrada = ft.TextField(
        label="Type your answer",
        width=400,
        text_align="center")
 
    actual = ""
    valor_actual = 0
 
    def empezar():
 
        resultado.value = "Game Started!"
        resultado.color = "green"
        page.update()
    def mostrar(cat, valor):
        nonlocal actual
        nonlocal valor_actual
 
        try:
 
            if (cat, valor) in usadas:
                resultado.value = "Question already used!"
                resultado.color = "orange"
                page.update()
                return
 
            texto, respuesta = preguntas[cat][valor]
            pregunta.value = f"{cat} - ${valor}\n\n{texto}"
            actual = respuesta.lower()
            valor_actual = valor
            usadas.append((cat, valor))
            page.update()
 
        except Exception as e:
            resultado.value = f"Error: {e}"
            resultado.color = "red"
            page.update()
 
    def sumar(num):
        global puntos
        puntos += num
        score.value = f"Score: {puntos}"
        page.update()
 
    def terminar():
        pregunta.value = "YOU WIN THE GAME!"
        resultado.value = "Congratulations!"
        resultado.color = "yellow"
 
        page.update()
    async def revisar(e):
        global puntos
        nonlocal valor_actual
        nonlocal actual
        nonlocal correctas
        nonlocal incorrectas
 
        try:
            user = entrada.value.lower().strip()
            if actual == "":
                resultado.value = "Choose a question first!"
                resultado.color = "orange"
                page.update()
                return
            if user == "":
                resultado.value = "Please type an answer!"
                resultado.color = "orange"
                page.update()
                return
            if user == actual:
                await right_sound.play()
                sumar(valor_actual)
                correctas += 1
                right_text.value = f"Right Answers: {correctas}"
                resultado.value = "Correct!"
                resultado.color = "green"
 
            else:
                await wrong_sound.play()
                sumar(-valor_actual)
                incorrectas += 1
                wrong_text.value = f"Wrong Answers: {incorrectas}"
                resultado.value = f"Wrong! Correct answer: {actual}"
                resultado.color = "red"
            entrada.value = ""
 
            actual = ""
            valor_actual = 0
 
            page.update()
 
            if puntos >= 500:
                terminar()
        except Exception as e:
            resultado.value = f"Error: {e}"
            resultado.color = "red"
            page.update()
 
    def reset(e):
        global puntos
        nonlocal correctas
        nonlocal incorrectas
        nonlocal actual
        nonlocal valor_actual
 
        puntos = 0
        correctas = 0
        incorrectas = 0
 
        usadas.clear()
 
        score.value = f"Score: {puntos}"
        right_text.value = f"Right Answers: {correctas}"
        wrong_text.value = f"Wrong Answers: {incorrectas}"
        pregunta.value = "Choose a category and value!"
        resultado.value = ""
        entrada.value = ""
 
        actual = ""
        valor_actual = 0
 
        page.update()
 
    while juego:
        break
 
    tablero = []
 
    for cat in preguntas:
 
        cosas = [
 
            ft.Text(
                cat,
                size=24,
                weight="bold",
                color="yellow")]
 
        for valor in preguntas[cat]:
 
            boton = ft.ElevatedButton(
 
                f"${valor}",
 
                width=120,
 
                height=60,
 
                on_click=lambda e, c=cat, v=valor:
                mostrar(c, v))
 
            cosas.append(boton)
 
        tablero.append(
 
            ft.Column(
 
                controls=cosas,
 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER))
 
    enviar = ft.ElevatedButton(
 
        "Submit Answer",
 
        width=250,
 
        height=50,
 
        on_click=revisar)
 
    reiniciar = ft.ElevatedButton(
 
        "Reset Game",
 
        width=250,
 
        height=50,
 
        on_click=reset)
 
    empezar()
 
    page.add(
 
        ft.Column(
 
            controls=[
 
                logo,
 
                titulo,
 
                score,
 
                right_text,
 
                wrong_text,
 
                ft.Row(
 
                    controls=tablero,
 
                    alignment=ft.MainAxisAlignment.CENTER,
 
                    spacing=30),
 
                ft.Divider(),
 
                pregunta,
 
                entrada,
 
                enviar,
 
                reiniciar,
 
                resultado],
 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
 
            spacing=20))
 
ft.run(main=main, assets_dir="assets") 