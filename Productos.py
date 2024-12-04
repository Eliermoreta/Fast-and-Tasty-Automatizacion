import time
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


service = Service(r"C:\WebDriver\msedgedriver.exe")


options = Options()
options.use_chromium = True  


driver = webdriver.Edge(service=service, options=options)


html_path = "C:/Users/elier/Desktop/proyecto_final_pedidos/productos.html"


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
        <h1>Reporte de Automatización - Productos</h1>
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
    
    with open("automation_report.html", "w") as file:
        file.write(report)
    print("Reporte generado: automation_report.html")


actions = []

try:
    
    driver.get(f"file:///{html_path}")
    actions.append({"action": "Abrir Productos", "screenshot": take_screenshot("open_products"), "status": "Éxito"})

    
    time.sleep(2)

    
    products = driver.find_elements(By.CSS_SELECTOR, ".product")
    for product in products:
        product_name = product.find_element(By.CSS_SELECTOR, "h2").text
        product_price = product.find_element(By.CSS_SELECTOR, "p").text
        buy_button = product.find_element(By.XPATH, ".//button")
        
        
        buy_button.click()
        actions.append({"action": f"Comprar {product_name} ({product_price})", "screenshot": take_screenshot(f"buy_{product_name}"), "status": "Éxito"})
        
        
        time.sleep(1)

    
    cart_button = driver.find_element(By.ID, "pay-button")
    cart_button.click()
    actions.append({"action": "Hacer clic en Pagar", "screenshot": take_screenshot("click_pay_button"), "status": "Éxito"})

    
    time.sleep(3)
    actions.append({"action": "Esperar respuesta", "screenshot": take_screenshot("wait_response"), "status": "Éxito"})

except Exception as e:
    print(f"Error durante la automatización: {e}")
    actions.append({"action": "Error", "screenshot": take_screenshot("error"), "status": "Fallido"})

finally:
   
    generate_report(actions)
    driver.quit()
