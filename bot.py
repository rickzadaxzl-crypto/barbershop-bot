import json
import time
from datetime import datetime

# Carregar configuração
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        CONFIG = json.load(f)
except Exception as e:
    print(f"❌ Erro ao carregar config.json: {e}")
    exit(1)

class BarberBot:
    def __init__(self):
        self.agendamentos = []
        self.carrega_agendamentos()
        print("\n" + "="*60)
        print("🤖 BOT BARBEARIA - MODO SIMULAÇÃO")
        print("="*60)
        print(f"📍 {CONFIG['barbearia']['nome']}")
        print(f"📞 {CONFIG['barbearia']['telefone']}")
        print(f"⏰ {CONFIG['barbearia']['horario_inicio']} - {CONFIG['barbearia']['horario_fim']}")
        print("\n💡 Use este bot para testar as respostas")
        print("Digite 'sair' para encerrar\n")
    
    def carrega_agendamentos(self):
        """Carrega agendamentos salvos"""
        try:
            with open('agendamentos.json', 'r', encoding='utf-8') as f:
                self.agendamentos = json.load(f).get('agendamentos', [])
        except:
            self.agendamentos = []
    
    def salva_agendamentos(self):
        """Salva agendamentos em arquivo"""
        try:
            with open('agendamentos.json', 'w', encoding='utf-8') as f:
                json.dump({'agendamentos': self.agendamentos}, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar agendamentos: {e}")
    
    def processar_msg(self, texto):
        """Processa mensagem e retorna resposta"""
        if not texto:
            return self.menu_principal()
        
        msg = texto.lower().strip()
        
        if msg in ['oi', 'olá', 'ola', 'oiii', 'e ai', 'opa', 'e aí', 'opa', 'tudo bem']:
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
        nome = CONFIG.get('barbearia', {}).get('nome', 'Barbearia')
        return f"""👋 Bem-vindo à {nome}!

📋 MENU:

1️⃣  Agendar corte
2️⃣  Horários
3️⃣  Barbeiros
4️⃣  Preços

Digite o número da opção."""
    
    def horarios(self):
        """Mostra horários"""
        barbearia = CONFIG.get('barbearia', {})
        nome = barbearia.get('nome', 'Barbearia')
        inicio = barbearia.get('horario_inicio', '08:00')
        fim = barbearia.get('horario_fim', '20:00')
        telefone = barbearia.get('telefone', 'N/A')
        
        return f"""⏰ HORÁRIO DE FUNCIONAMENTO

📍 {nome}
🕗 Abre: {inicio}
🕘 Fecha: {fim}

📞 {telefone}"""
    
    def barbeiros(self):
        """Lista barbeiros"""
        texto = "👨‍💼 NOSSOS BARBEIROS:\n\n"
        barbeiros_list = CONFIG.get('barbeiros', [])
        
        if isinstance(barbeiros_list, list) and len(barbeiros_list) > 0:
            for b in barbeiros_list:
                nome = b.get('nome', 'Barbeiro')
                telefone = b.get('telefone', 'N/A')
                texto += f"{nome}\n📱 {telefone}\n\n"
        else:
            texto += "Nenhum barbeiro cadastrado."
        
        return texto.strip()
    
    def precos(self):
        """Mostra preços"""
        texto = "💰 TABELA DE PREÇOS:\n\n"
        valores = CONFIG.get('valores', {})
        
        if isinstance(valores, dict) and len(valores) > 0:
            for servico, preco in valores.items():
                servico_formatado = servico.replace('_', ' ').title()
                texto += f"✂️ {servico_formatado}: R$ {preco:.2f}\n"
        else:
            texto += "Nenhum serviço cadastrado."
        
        return texto.strip()
    
    def agendar(self):
        """Inicia agendamento"""
        texto = "📅 AGENDAR CORTE\n\nEscolha o serviço:\n\n"
        valores = CONFIG.get('valores', {})
        
        if isinstance(valores, dict) and len(valores) > 0:
            for i, (servico, preco) in enumerate(valores.items(), 1):
                servico_formatado = servico.replace('_', ' ').title()
                texto += f"{i}. {servico_formatado} - R$ {preco:.2f}\n"
        else:
            texto += "Nenhum serviço disponível."
        
        barbearia = CONFIG.get('barbearia', {})
        telefone = barbearia.get('telefone', 'N/A')
        texto += f"\n(Responda com o número)\n\nOu fale com um atendente: {telefone}"
        
        return texto
    
    def run(self):
        """Loop principal"""
        print("="*60)
        print("🏪 Bot pronto para receber mensagens\n")
        
        while True:
            try:
                usuario_input = input("📝 Você: ").strip()
                
                if usuario_input.lower() in ['sair', 'exit', 'quit']:
                    print("\n❌ Bot encerrado.")
                    break
                
                resposta = self.processar_msg(usuario_input)
                print(f"\n🤖 Bot:\n{resposta}")
                print("\n" + "="*60 + "\n")
            
            except KeyboardInterrupt:
                print("\n\n❌ Bot encerrado.")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")

if __name__ == "__main__":
    bot = BarberBot()
    bot.run()
