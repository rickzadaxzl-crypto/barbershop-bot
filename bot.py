import json
import time
from datetime import datetime

# Carregar configuração
with open('config.json', 'r', encoding='utf-8') as f:
    CONFIG = json.load(f)

class BarberBot:
    def __init__(self):
        self.agendamentos = []
        print("\n🤖 Bot Barbearia iniciado!")
        print(f"📍 {CONFIG['barbearia']['nome']}\n")
        print("⚠️  MODO SIMULAÇÃO (sem WhatsApp Web)")
        print("Digite suas mensagens para testar:\n")
    
    def processar_msg(self, texto):
        """Processa mensagem e retorna resposta"""
        msg = texto.lower().strip()
        
        if msg in ['oi', 'olá', 'ola', 'oiii', 'e ai', '']:
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
        if isinstance(CONFIG.get('barbeiros'), list):
            for b in CONFIG['barbeiros']:
                texto += f"{b['nome']}\n📱 {b['telefone']}\n\n"
        return texto.strip()
    
    def precos(self):
        """Mostra preços"""
        texto = "💰 TABELA DE PREÇOS:\n\n"
        if isinstance(CONFIG.get('valores'), dict):
            for servico, preco in CONFIG['valores'].items():
                texto += f"✂️ {servico.title()}: R$ {preco:.2f}\n"
        return texto.strip()
    
    def agendar(self):
        """Inicia agendamento"""
        texto = "📅 AGENDAR CORTE\n\n"
        texto += "Escolha o serviço:\n\n"
        if isinstance(CONFIG.get('valores'), dict):
            for i, (servico, preco) in enumerate(CONFIG['valores'].items(), 1):
                texto += f"{i}. {servico.title()} - R$ {preco:.2f}\n"
        texto += "\n(Responda com o número)\n\nOu fale com um atendente: " + CONFIG['barbearia']['telefone']
        return texto.strip()
    
    def run(self):
        """Loop principal"""
        print("🏪 Bot pronto para receber mensagens...\n")
        print("=" * 50)
        
        try:
            while True:
                usuario_input = input("\n📝 Você: ").strip()
                
                if usuario_input.lower() == 'sair':
                    print("\n❌ Bot encerrado.")
                    break
                
                resposta = self.processar_msg(usuario_input)
                print(f"\n🤖 Bot:\n{resposta}")
                print("\n" + "=" * 50)
        
        except KeyboardInterrupt:
            print("\n\n❌ Bot encerrado.")

if __name__ == "__main__":
    bot = BarberBot()
    bot.run()
