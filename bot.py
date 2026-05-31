import os
import sys
import time
import json
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Carregar configuração
with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

class BarberBot:
    def __init__(self):
        self.setup_driver()
        self.ultima_msg = set()
        print("\n🤖 Bot Barbearia iniciado!")
        print(f"📍 {CONFIG['barbearia']['nome']}\n")
    
    def setup_driver(self):
        """Configura Selenium"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_argument('user-data-dir=./whatsapp_session')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            
            print("\n🌐 Abrindo WhatsApp Web...")
            self.driver.get('https://web.whatsapp.com')
            
            print("\n" + "="*50)
            print("📱 ESCANEIE O QR CODE COM WHATSAPP")
            print("="*50)
            print("\n1. Abra WhatsApp no celular")
            print("2. Vá em Configurações > Aparelhos conectados")
            print("3. Aponte câmera para o QR Code")
            print("\nAguardando scan...\n")
            
            # Aguarda login
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"]'))
            )
            
            print("\n✅ Conectado! Bot pronto para receber mensagens.\n")
            time.sleep(2)
        
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            sys.exit(1)
    
    def get_messages(self):
        """Obtém mensagens não processadas"""
        try:
            msgs = self.driver.find_elements(
                By.XPATH,
                '//div[contains(@class, "message-in")]'
            )
            
            novas = []
            for msg in msgs:
                try:
                    msg_id = msg.get_attribute('data-id')
                    if msg_id and msg_id not in self.ultima_msg:
                        texto = msg.find_element(
                            By.XPATH,
                            './/span[@class="_1wjpf"]'
                        ).text
                        novas.append({'id': msg_id, 'texto': texto})
                        self.ultima_msg.add(msg_id)
                except:
                    pass
            
            return novas
        except:
            return []
    
    def send_message(self, texto):
        """Envia mensagem"""
        try:
            campo = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@data-tab="1"]')
                )
            )
            
            campo.click()
            time.sleep(0.3)
            campo.send_keys(texto)
            time.sleep(0.3)
            campo.send_keys(Keys.CONTROL + Keys.ENTER)
            
            print(f"📤 Resposta enviada")
            time.sleep(1)
        except Exception as e:
            print(f"Erro ao enviar: {e}")
    
    def processar_msg(self, texto):
        """Processa mensagem e retorna resposta"""
        msg = texto.lower().strip()
        
        if msg in ['oi', 'olá', 'ola', 'oiii']:
            return self.menu_principal()
        elif msg == '1' or 'agendar' in msg:
            return self.agendar()
        elif msg == '2' or 'horário' in msg or 'horario' in msg:
            return self.horarios()
        elif msg == '3' or 'barbeiro' in msg:
            return self.barbeiros()
        elif msg == '4' or 'preço' in msg or 'preco' in msg:
            return self.precos()
        else:
            return self.menu_principal()
    
    def menu_principal(self):
        """Menu principal"""
        return f"""
👋 Bem-vindo à {CONFIG['barbearia']['nome']}!

📋 MENU:

1️⃣  Agendar corte
2️⃣  Horários
3️⃣  Barbeiros
4️⃣  Preços

Digite o número da opção.
        """.strip()
    
    def horarios(self):
        """Mostra horários"""
        return f"""
⏰ HORÁRIO DE FUNCIONAMENTO

📍 {CONFIG['barbearia']['nome']}
🕗 Abre: {CONFIG['barbearia']['horario_inicio']}
🕘 Fecha: {CONFIG['barbearia']['horario_fim']}

📞 {CONFIG['barbearia']['telefone']}
        """.strip()
    
    def barbeiros(self):
        """Lista barbeiros"""
        texto = "👨‍💼 NOSSOS BARBEIROS:\n\n"
        for b in CONFIG['barbeiros']:
            texto += f"{b['nome']}\n📱 {b['telefone']}\n\n"
        return texto.strip()
    
    def precos(self):
        """Mostra preços"""
        texto = "💰 TABELA DE PREÇOS:\n\n"
        for servico, preco in CONFIG['valores'].items():
            texto += f"✂️ {servico.title()}: R$ {preco:.2f}\n"
        return texto.strip()
    
    def agendar(self):
        """Inicia agendamento"""
        texto = "📅 AGENDAR CORTE\n\n"
        texto += "Escolha o serviço:\n\n"
        for i, (servico, preco) in enumerate(CONFIG['valores'].items(), 1):
            texto += f"{i}. {servico.title()} - R$ {preco:.2f}\n"
        texto += "\n(Responda com o número)\n\nOu fale com um atendente: " + CONFIG['barbearia']['telefone']
        return texto.strip()
    
    def run(self):
        """Loop principal"""
        print("🏪 Bot aguardando mensagens...\n")
        
        try:
            while True:
                msgs = self.get_messages()
                
                if msgs:
                    for msg in msgs:
                        texto = msg['texto']
                        print(f"\n📨 [{datetime.now().strftime('%H:%M')}] Cliente: {texto}")
                        
                        resposta = self.processar_msg(texto)
                        self.send_message(resposta)
                
                time.sleep(2)
        
        except KeyboardInterrupt:
            print("\n\n❌ Bot encerrado.")
            self.driver.quit()
            sys.exit(0)

if __name__ == "__main__":
    bot = BarberBot()
    bot.run()
