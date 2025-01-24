from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import pyautogui
import pyperclip

# Fixture do pytest para inicializar e finalizar o driver do Selenium
@pytest.fixture
def driver():
    # Inicializa o navegador Chrome
    driver = webdriver.Chrome()
    # Garantindo que o navegador será fechado após o teste
    yield driver
    driver.quit()

# Função para inserir dados no formulário e obter o resultado
def inserir_dados(lado_a, lado_b, lado_c, driver):
    # Acessa a página que será testada
    driver.get("https://www.vanilton.net/triangulo/#")

    # Espera explícita para garantir que os campos de entrada estejam carregados
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "V1")))
    
    # Encontra os campos de entrada para os lados do triângulo
    lado_a_input = driver.find_element(By.NAME, "V1")
    lado_b_input = driver.find_element(By.NAME, "V2")
    lado_c_input = driver.find_element(By.NAME, "V3")

    # Encontra o botão de submit
    botao_submit = driver.find_element(By.XPATH, "//input[@type='submit' and @value='Identificar']")

    # Preenche os campos com os valores fornecidos
    lado_a_input.send_keys(lado_a)
    lado_b_input.send_keys(lado_b)
    lado_c_input.send_keys(lado_c)

    # Clica no botão para identificar o tipo de triângulo
    botao_submit.click()

    # Chama a função para coletar o resultado da página
    resultado = coletar_resultado()

    # Exibe o resultado no console
    print(f"Resultado: {resultado}")

    # Retorna o tipo de triângulo (ou False se não for um triângulo válido)
    return resultado

# Função para coletar o resultado da página após a submissão
def coletar_resultado():
    # Utiliza pyautogui para copiar o resultado da tela
    pyautogui.hotkey('ctrl', 'a')  # Seleciona todo o texto na tela
    pyautogui.hotkey('ctrl', 'c')  # Copia o texto selecionado

    # Obtém o texto copiado usando pyperclip
    texto = pyperclip.paste()

    # Determina o tipo de triângulo com base no texto
    if "Equilátero" in texto:
        return "Equilátero"
    elif "Isósceles" in texto:
        return "Isósceles"
    elif "Escaleno" in texto:
        return "Escaleno"
    else:
        # Se o texto não corresponder a nenhum tipo de triângulo, retorna False
        return False

# Teste para verificar a resposta com entradas inválidas
def test_triangulo_erro(driver):
    # Verifica se os dados inválidos retornam False (não é um triângulo válido)
    assert inserir_dados(1, 2, 3, driver) == False  # Não é um triângulo
    assert inserir_dados(0, 0, 0, driver) == False  # Não é um triângulo
    assert inserir_dados(-1, -1, -5, driver) == False  # Não é um triângulo

# Testes para o caso do triângulo Equilátero (todos os lados iguais)
def test_equilatero(driver):
    # Verifica se os dados correspondem a um triângulo equilátero
    assert inserir_dados(1, 1, 1, driver) == 'Equilátero'
    assert inserir_dados(5, 5, 5, driver) == 'Equilátero'
    assert inserir_dados(10, 10, 10, driver) == 'Equilátero'

# Testes para o caso do triângulo Isósceles (dois lados iguais)
def test_isosceles(driver):
    # Verifica se os dados correspondem a um triângulo isósceles
    assert inserir_dados(1, 1, 2, driver) == "Isósceles"
    assert inserir_dados(3, 3, 5, driver) == "Isósceles"
    assert inserir_dados(12, 12, 15, driver) == "Isósceles"

# Testes para o caso do triângulo Escaleno (todos os lados diferentes)
def test_escaleno(driver):
    # Verifica se os dados correspondem a um triângulo escaleno
    assert inserir_dados(2, 3, 4, driver) == "Escaleno"
    assert inserir_dados(5, 4, 3, driver) == "Escaleno"
    assert inserir_dados(10, 8, 6, driver) == "Escaleno"
