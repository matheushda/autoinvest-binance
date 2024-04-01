import pyautogui
import time
import pytesseract
import re
from PIL import ImageGrab
from colorama import Fore, Style, init

# Inicializar o colorama
init()

# Abrir o navegador (utilizo brave, mas pode ser substítuido)
pyautogui.hotkey('win', 'r')
pyautogui.typewrite('brave')
pyautogui.press('enter')
time.sleep(2)  # Aguardar o Brave abrir

# Entrar no site do CallBot
pyautogui.typewrite('https://web.telegram.org/a/#-1001557422965')
pyautogui.press('enter')
time.sleep(5) 
pyautogui.click("./img/guia.png")
time.sleep(1)
pyautogui.hotkey('ctrl', 'tab')
time.sleep(1)

# Clicar na seta para descer as mensagens da página
try:
    image_location = pyautogui.locateOnScreen("./img/seta.png")
    if image_location:
        x, y = pyautogui.center(image_location)
        pyautogui.click(x, y)
except Exception as e:
    pass 

# Definir as variáveis para armazenar os valores
enter_at = None
take_profit_at = None
stop_loss = None
accuracy = None
processed_currency_pairs = set()  # Conjunto para armazenar os pares de criptomoedas que já foram processadas

# Loop infinito de verificações
while True:
    # Capturar a tela
    screenshot = ImageGrab.grab()

    # pytesseract convertendo a captura de tela para texto
    text = pytesseract.image_to_string(screenshot)

    # Aviso de início de nova verificação em vermelho
    print(f"{Fore.RED}Iniciando verificação...{Style.RESET_ALL}")

    # Extrair somente a moeda, sem acrescentar o restante do texto que contém nas mensagens
    currency_pairs_match = re.findall(r'\b(\w+)/USDT\b', text)

    # Verificar cada currency pair encontrada
    for currency_pair in currency_pairs_match:
        print(f"{Fore.YELLOW}Criptomoeda: {currency_pair}{Style.RESET_ALL}") 

        # Verificar se a criptomoeda já foi processada
        if currency_pair not in processed_currency_pairs:
            processed_currency_pairs.add(currency_pair)  # Marcar a criptomoeda como processada

            # Extrair os valores das variáveis definidas anteriormente
            enter_match = re.search(r'Enter at:\s*([\d.]+)', text)
            if enter_match: 
                enter_at = float(enter_match.group(1))
                print(f"{Fore.CYAN}Enter at: {enter_at}{Style.RESET_ALL}")

            take_profit_match = re.search(r'Take profit at:\s*([\d.]+)', text)
            if take_profit_match:
                take_profit_at = float(take_profit_match.group(1))
                print(f"{Fore.MAGENTA}Take profit at: {take_profit_at}{Style.RESET_ALL}")

            stop_loss_match = re.search(r'Stop loss:\s*([\d.]+)', text)
            if stop_loss_match:
                stop_loss = float(stop_loss_match.group(1))
                print(f"{Fore.GREEN}Stop loss: {stop_loss}{Style.RESET_ALL}")

            accuracy_match = re.search(r'Accuracy:\s*([\d.]+)', text)
            if accuracy_match:
                accuracy = float(accuracy_match.group(1))
                print(f"{Fore.BLUE}Accuracy: {accuracy}{Style.RESET_ALL}")

                # Se a accuracy for maior que 90%, executar a segunda ação.
                if accuracy >= 50:
                    print(f"Criptomoeda encontrada, performando ação em {currency_pair}...")
                    pyautogui.click("./img/pontos.png")
                    pyautogui.hotkey('ctrl', 'tab')
                    pyautogui.typewrite(f'https://www.binance.com/pt-BR/trade/{currency_pair}_usdt')
                    pyautogui.press('enter')
                    time.sleep(10)
                    pyautogui.move(1800,0)
                    pyautogui.scroll(-10000)
                    time.sleep(3)
                    pyautogui.click("/img/total.png")
                    entrada = {enter_at}
                    pyautogui.write(str(entrada))
                    time.sleep(500)
                else:
                    print(f"A criptomoeda {currency_pair} tem uma precisão de {accuracy}. Continuando...")

    time.sleep(500)