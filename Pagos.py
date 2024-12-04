import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


service = Service(r"C:\WebDriver\msedgedriver.exe")


options = Options()
options.use_chromium = True  


driver = webdriver.Edge(service=service, options=options)


html_path = "C:/Users/elier/Desktop/proyecto_final_pedidos/pagos.html"


screenshot_dir = "screenshots"
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


def take_screenshot(step_name):
    timestamp = int(time.time())
    screenshot_path = f"{screenshot_dir}/{step_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_path)
    print(f"Captura tomada: {screenshot_path}")
    return screenshot_path


def generate_report(actions):
    report = """
    <html>
    <head><title>Reporte de Automatización</title></head>
    <body>
        <h1>Reporte de Automatización - Pago</h1>
        <table border="1">
            <tr><th>Acción</th><th>Captura de Pantalla</th><th>Estado</th></tr>
    """
    
    for action in actions:
        report += f"""
        <tr>
            <td>{action['action']}</td>
            <td><img src="{action['screenshot']}" alt="Captura de {action['action']}" width="300"></td>
            <td>{action['status']}</td>
        </tr>
        """
    
    report += """
        </table>
    </body>
    </html>
    """
    
    with open("payment_report.html", "w") as file:
        file.write(report)
    print("Reporte generado: payment_report.html")


actions = []

try:
   
    driver.get(f"file:///{html_path}")
    actions.append({"action": "Abrir Página de Pago", "screenshot": take_screenshot("open_payment_page"), "status": "Éxito"})

    
    time.sleep(2)

   
    url_params = driver.current_url
    total_amount = url_params.split("total=")[-1]
    actions.append({"action": f"Total de pago: ${total_amount}", "screenshot": take_screenshot("display_total"), "status": "Éxito"})

    
    name_input = driver.find_element(By.ID, "name")
    email_input = driver.find_element(By.ID, "email")
    card_input = driver.find_element(By.ID, "card")
    
    
    name_input.send_keys("Juan Pérez")
    email_input.send_keys("juan.perez@email.com")
    card_input.send_keys("1234567890123456")
    actions.append({"action": "Rellenar formulario", "screenshot": take_screenshot("fill_form"), "status": "Éxito"})

   
    pay_button = driver.find_element(By.CSS_SELECTOR, ".pay-button")
    pay_button.click()
    actions.append({"action": "Confirmar Pago", "screenshot": take_screenshot("confirm_payment"), "status": "Éxito"})

    
    time.sleep(2)
    confirmation_message = driver.find_element(By.ID, "confirmation-message")
    if confirmation_message.is_displayed():
        actions.append({"action": "Verificar confirmación", "screenshot": take_screenshot("payment_confirmation"), "status": "Éxito"})
    else:
        actions.append({"action": "Verificar confirmación", "screenshot": take_screenshot("payment_failed"), "status": "Fallido"})

except Exception as e:
    print(f"Error durante la automatización: {e}")
    actions.append({"action": "Error", "screenshot": take_screenshot("error"), "status": "Fallido"})

finally:
   
    generate_report(actions)
    driver.quit()
