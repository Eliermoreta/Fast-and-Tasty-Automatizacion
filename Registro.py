from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
import time
import os
import datetime


service = Service(r"C:\WebDriver\msedgedriver.exe")
driver = webdriver.Edge(service=service)


def take_screenshot(driver, step_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_name = f"screenshot_{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Captura tomada: {screenshot_name}")


def generate_report():
    report_content = """
    <html>
    <head><title>Reporte de Automatización</title></head>
    <body>
    <h1>Reporte de Automatización - Registro</h1>
    <p>Automatización completada con éxito. Las capturas de pantalla se han guardado.</p>
    <h2>Detalles</h2>
    <ul>
        <li>Página Accedida: Registro</li>
        <li>Campos Llenados: Nombre, Correo, Contraseña</li>
        <li>Capturas de Pantalla: Sí</li>
    </ul>
    <h2>Capturas de Pantalla</h2>
    <img src="screenshot" alt="Screenshot" width="100%">
    </body>
    </html>
    """
    with open("registro_report.html", "w") as file:
        file.write(report_content)
    print("Reporte HTML generado: registro_report.html")


html_path = "file:///C:/Users/elier/Desktop/proyecto_final_pedidos/Registro.html"
driver.get(html_path)


take_screenshot(driver, "cargar_pagina")


name_field = driver.find_element(By.ID, "name")
email_field = driver.find_element(By.ID, "email")
password_field = driver.find_element(By.ID, "password")
submit_button = driver.find_element(By.XPATH, "//button[text()='Crear Cuenta']")


name_field.send_keys("Juan Pérez")
email_field.send_keys("juan.perez@email.com")
password_field.send_keys("contraseña123")


take_screenshot(driver, "rellenar_formulario")


submit_button.click()


time.sleep(2)


take_screenshot(driver, "envio_formulario")


generate_report()


driver.quit()
