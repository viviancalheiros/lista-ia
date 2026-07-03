import streamlit as st
import random
import math

# --- 1. BASE DE CONHECIMENTO BLINDADA E TAXONÔMICA (24 Entidades, 26 Atributos) ---
BASE_CONHECIMENTO = {
    # MAMÍFEROS
    "Cachorro 🐶": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": True, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Gato 🐱": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": True, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": True, "tem_bico": False, "pula": True, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Elefante 🐘": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": True, "predador": False, "e_primata": False, "e_marsupial": False},
    "Morcego 🦇": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": True, "e_domestico": False, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": True, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": False, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Baleia 🐋": {"e_mamifero": True, "e_ave": False, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": True, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": True, "predador": True, "e_primata": False, "e_marsupial": False},
    "Canguru 🦘": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": True, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": False, "e_primata": False, "e_marsupial": True},
    "Macaco 🐒": {"e_mamifero": True, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": True, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": False, "e_primata": True, "e_marsupial": False},
    "Ornitorrinco 🦆🦦": {"e_mamifero": True, "e_ave": False, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": True, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": True, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},

    # AVES
    "Águia 🦅": {"e_mamifero": False, "e_ave": True, "vive_na_agua": False, "respira_agua": False, "voa": True, "e_domestico": False, "tem_pelos": False, "tem_penas": True, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": True, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Pinguim 🐧": {"e_mamifero": False, "e_ave": True, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": True, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": True, "pula": True, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Avestruz 🦤": {"e_mamifero": False, "e_ave": True, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": True, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": True, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": True, "predador": False, "e_primata": False, "e_marsupial": False},
    "Coruja 🦉": {"e_mamifero": False, "e_ave": True, "vive_na_agua": False, "respira_agua": False, "voa": True, "e_domestico": False, "tem_pelos": False, "tem_penas": True, "tem_escamas": False, "bota_ovos": True, "e_noturno": True, "tem_bico": True, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},

    # RÉPTEIS E ANFÍBIOS
    "Cobra 🐍": {"e_mamifero": False, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": True, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": True, "quatro_patas": False, "tem_cauda": True, "e_peconhento": True, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Tartaruga 🐢": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": True, "bota_ovos": True, "e_noturno": False, "tem_bico": True, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": True, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": False, "e_primata": False, "e_marsupial": False},
    "Jacaré 🐊": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": True, "bota_ovos": True, "e_noturno": True, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": True, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": True, "predador": True, "e_primata": False, "e_marsupial": False},
    "Camaleão 🦎": {"e_mamifero": False, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": True, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": True, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Sapo 🐸": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": True, "tem_bico": False, "pula": True, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": True, "tem_cauda": False, "e_peconhento": True, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},

    # PEIXES E AQUÁTICOS
    "Tubarão 🦈": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": True, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": True, "bota_ovos": False, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": True, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": True, "predador": True, "e_primata": False, "e_marsupial": False},
    "Cavalo Marinho 🐎🌊": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": True, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": False, "tem_antenas": False, "oito_membros": False, "muda_de_cor": True, "tem_carapaca": True, "sem_patas": True, "quatro_patas": False, "tem_cauda": True, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},

    # INVERTEBRADOS
    "Aranha 🕷️": {"e_mamifero": False, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": True, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": True, "tem_bico": False, "pula": True, "invertebrado": True, "tem_antenas": False, "oito_membros": True, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": False, "e_peconhento": True, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Borboleta 🦋": {"e_mamifero": False, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": True, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": True, "tem_antenas": True, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": False, "sem_patas": False, "quatro_patas": False, "tem_cauda": False, "e_peconhento": False, "gigante": False, "predador": False, "e_primata": False, "e_marsupial": False},
    "Formiga 🐜": {"e_mamifero": False, "e_ave": False, "vive_na_agua": False, "respira_agua": False, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": True, "tem_antenas": True, "oito_membros": False, "muda_de_cor": False, "tem_carapaca": True, "sem_patas": False, "quatro_patas": False, "tem_cauda": False, "e_peconhento": False, "gigante": False, "predador": False, "e_primata": False, "e_marsupial": False},
    "Polvo 🐙": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": True, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": True, "tem_bico": True, "pula": False, "invertebrado": True, "tem_antenas": False, "oito_membros": True, "muda_de_cor": True, "tem_carapaca": False, "sem_patas": True, "quatro_patas": False, "tem_cauda": False, "e_peconhento": True, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False},
    "Caranguejo 🦀": {"e_mamifero": False, "e_ave": False, "vive_na_agua": True, "respira_agua": True, "voa": False, "e_domestico": False, "tem_pelos": False, "tem_penas": False, "tem_escamas": False, "bota_ovos": True, "e_noturno": False, "tem_bico": False, "pula": False, "invertebrado": True, "tem_antenas": True, "oito_membros": True, "muda_de_cor": False, "tem_carapaca": True, "sem_patas": False, "quatro_patas": False, "tem_cauda": False, "e_peconhento": False, "gigante": False, "predador": True, "e_primata": False, "e_marsupial": False}
}

PERGUNTAS_TEXTO = {
    "e_mamifero": "É um mamífero (dá de mamar aos filhotes)?",
    "e_ave": "É uma ave?",
    "vive_na_agua": "Passa boa parte da vida dentro d'água?",
    "respira_agua": "Respira debaixo d'água (ex: possui guelras)?",
    "voa": "Consegue voar ativamente?",
    "e_domestico": "É comum ser criado como animal de estimação em casas?",
    "tem_pelos": "Possui o corpo coberto por pelos?",
    "tem_penas": "Possui penas?",
    "tem_escamas": "Possui escamas na pele?",
    "bota_ovos": "Esse animal bota ovos?",
    "e_noturno": "Possui hábitos predominantemente noturnos (ativo à noite)?",
    "tem_bico": "Possui bico?",
    "pula": "Sua principal forma de locomoção rápida inclui dar saltos?",
    "invertebrado": "É um animal invertebrado (não possui ossos/coluna vertebral)?",
    "tem_antenas": "Possui antenas visíveis na cabeça?",
    "oito_membros": "Possui 8 ou mais pernas, braços ou tentáculos?",
    "muda_de_cor": "É famoso por conseguir mudar de cor para se camuflar?",
    "tem_carapaca": "Possui uma carapaça dura, casco ou exoesqueleto forte?",
    "sem_patas": "É um animal que NÃO possui patas/pernas?",
    "quatro_patas": "Possui exatamente quatro patas para caminhar?",
    "tem_cauda": "Possui rabo/cauda visível?",
    "e_peconhento": "Pode ser peçonhento, venenoso ou soltar toxinas?",
    "gigante": "É um animal de porte muito grande ou gigante?",
    "predador": "É um predador ou tem a carne como base principal de sua dieta?",
    "e_primata": "Pertence à ordem dos primatas ?",
    "e_marsupial": "É um marsupial (termina de desenvolver os filhotes numa bolsa)?"
}

# --- 2. CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="IA Akinator", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; }
    .titulo-principal { text-align: center; font-size: 38px; font-weight: 800; color: #3b82f6; }
    .pergunta-card { 
        background-color: #1e293b; 
        border: 2px solid #3b82f6; 
        border-radius: 15px; 
        padding: 30px; 
        text-align: center; 
        font-size: 22px; 
        font-weight: 600; 
        color: #f8fafc !important;
        margin: 20px 0; 
    }
    .card-animal { 
        text-align: center; 
        padding: 10px; 
        background-color: #334155; 
        color: #f8fafc; 
        border-radius: 8px; 
        border: 1px solid #475569;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .suspeito-box {
        background-color: #064e3b;
        color: #10b981;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- [FUNCIONALIDADE MODULAR DE LOG ACUMULATIVO] Função criadora do documento ---
def gerar_log_txt():
    """Gera a string contendo o histórico de TODAS as partidas completas da sessão."""
    texto = "=== REGISTRO ACUMULADO DE PARTIDAS - AKINATOR IA ===\n\n"
    
    if not st.session_state.partidas_salvas:
        return "Nenhum histórico de partida concluída disponível para esta sessão."
    
    # Itera sobre todas as partidas que chegaram ao fim
    for i, partida in enumerate(st.session_state.partidas_salvas):
        texto += f"--- TENTATIVA {i+1} ---\n"
        texto += "PERGUNTAS E RESPOSTAS:\n"
        for j, (perg, resp) in enumerate(partida['historico']):
            texto += f"  {j+1}. {perg} -> {resp}\n"
        
        texto += "\nRESULTADO DA INFERÊNCIA:\n"
        cands = partida['candidatos_finais']
        if len(cands) == 1:
            texto += f"  Animal concluído com certeza: {cands[0]}\n"
        elif len(cands) > 1:
            texto += f"  Palpite mais provável do sistema: {cands[0]}\n"
            texto += f"  Outras opções restantes (Incerteza): {', '.join(cands[1:])}\n"
        else:
            texto += "  Nenhum animal da base correspondeu exatamenta às características.\n"
        texto += "\n" + "="*50 + "\n\n"
        
    return texto

# --- 3. ESTADOS ---
if 'tela' not in st.session_state: st.session_state.tela = 'MENU'
if 'candidatos' not in st.session_state: st.session_state.candidatos = list(BASE_CONHECIMENTO.keys())
if 'perguntas_feitas' not in st.session_state: st.session_state.perguntas_feitas = set()

# [FUNCIONALIDADE MODULAR DE LOG ACUMULATIVO]
# partidas_salvas guarda o histórico acumulado, historico_atual guarda só a partida rodando agora
if 'partidas_salvas' not in st.session_state: st.session_state.partidas_salvas = []
if 'historico_atual' not in st.session_state: st.session_state.historico_atual = []

# --- 4. LÓGICA DO MECANISMO DE INFERÊNCIA ---
def selecionar_pergunta():
    disponiveis = [p for p in PERGUNTAS_TEXTO.keys() if p not in st.session_state.perguntas_feitas]
    if not disponiveis: return None
        
    if len(st.session_state.perguntas_feitas) == 0:
        return random.choice(disponiveis)
    
    melhor_pergunta = None
    maior_entropia = -1 
    total_candidatos = len(st.session_state.candidatos)
    
    for p in disponiveis:
        sim = sum(1 for a in st.session_state.candidatos if BASE_CONHECIMENTO[a].get(p) is True)
        nao = total_candidatos - sim
        
        if sim == 0 or nao == 0: continue
            
        p_sim = sim / total_candidatos
        p_nao = nao / total_candidatos
        entropia = -(p_sim * math.log2(p_sim) + p_nao * math.log2(p_nao))
        
        if entropia > maior_entropia:
            maior_entropia = entropia
            melhor_pergunta = p
            
    return melhor_pergunta if melhor_pergunta else disponiveis[0]

def responder(resp, perg):
    st.session_state.perguntas_feitas.add(perg)
    
    # [FUNCIONALIDADE MODULAR DE LOG ACUMULATIVO] Armazena a ação apenas no histórico temporário
    st.session_state.historico_atual.append((PERGUNTAS_TEXTO[perg], resp))
    
    if resp == 'SIM':
        st.session_state.candidatos = [a for a in st.session_state.candidatos if BASE_CONHECIMENTO[a].get(perg) is True]
    elif resp == 'NAO':
        st.session_state.candidatos = [a for a in st.session_state.candidatos if BASE_CONHECIMENTO[a].get(perg, False) is False]
        
    # Checagem de Folha ou Fim de Árvore
    if len(st.session_state.candidatos) <= 1 or not selecionar_pergunta():
        st.session_state.tela = 'RESULTADO'
        
        # [FUNCIONALIDADE MODULAR DE LOG ACUMULATIVO]
        # O jogo acabou! Empacotamos o histórico atual e o salvamos no acumulado
        st.session_state.partidas_salvas.append({
            "historico": list(st.session_state.historico_atual),
            "candidatos_finais": list(st.session_state.candidatos)
        })

# --- 5. TELAS E IHM ---
if st.session_state.tela == 'MENU':
    st.markdown("<p class='titulo-principal'>Akinator de Animais</p>", unsafe_allow_html=True)
    st.write("### Animais na Base de Conhecimento:")
    cols = st.columns(4)
    for i, a in enumerate(BASE_CONHECIMENTO.keys()):
        with cols[i%4]: st.markdown(f"<div class='card-animal'>{a}</div>", unsafe_allow_html=True)
        
    st.write("---")
    if st.button("🚀 INICIAR JOGO", use_container_width=True, type="primary"):
        st.session_state.candidatos = list(BASE_CONHECIMENTO.keys())
        st.session_state.perguntas_feitas = set()
        st.session_state.historico_atual = [] # Zera apenas a partida atual. O acumulado fica salvo!
        st.session_state.tela = 'JOGO'
        st.rerun()

elif st.session_state.tela == 'JOGO':
    st.markdown("<p class='titulo-principal'>Analisando Dados...</p>", unsafe_allow_html=True)
    
    if len(st.session_state.candidatos) > 0:
        st.markdown(f"<div class='suspeito-box'>🔍 Hipótese Mais Provável: {st.session_state.candidatos[0]}</div>", unsafe_allow_html=True)
    
    perg = selecionar_pergunta()
    if perg:
        st.markdown(f"<div class='pergunta-card'>{PERGUNTAS_TEXTO[perg]}</div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: st.button("✅ SIM", use_container_width=True, on_click=responder, args=('SIM', perg))
        with c2: st.button("❌ NÃO", use_container_width=True, on_click=responder, args=('NAO', perg))
        with c3: st.button("🤷 NÃO SEI", use_container_width=True, on_click=responder, args=('NAOSEI', perg))
        
        st.write("---")
        if st.button("🏳️ Desistir da Tentativa", use_container_width=True):
            # Se desistir, volta pro MENU e a partida não é empacotada no histórico acumulado.
            st.session_state.tela = 'MENU'
            st.rerun()
            
    else:
        st.session_state.tela = 'RESULTADO'
        st.rerun()

elif st.session_state.tela == 'RESULTADO':
    st.markdown("<p class='titulo-principal'>Conclusão do Sistema</p>", unsafe_allow_html=True)
    
    if len(st.session_state.candidatos) == 1:
        st.success(f"### 🎉 É o(a): {st.session_state.candidatos[0]}!")
    elif len(st.session_state.candidatos) > 1:
        st.warning(f"As suas respostas foram um pouco imprecisas, mas o meu melhor palpite é: **{st.session_state.candidatos[0]}**!")
        st.info(f"Outras possibilidades que restaram na base: {', '.join(st.session_state.candidatos[1:])}")
    else:
        st.error("Nenhum animal da base corresponde exatamenta a todas as características informadas.")
        
    st.write("---")
    
    # --- [FUNCIONALIDADE MODULAR DE LOG ACUMULATIVO] Interface de Download ---
    log_conteudo = gerar_log_txt()
    st.download_button(
        label="📄 Baixar Histórico Acumulado de Partidas (Opcional - Formato TXT)",
        data=log_conteudo,
        file_name="historico_acumulado_akinator.txt",
        mime="text/plain",
        use_container_width=True
    )
    
    st.write("---")
    
    st.button("🔄 Iniciar Nova Análise", on_click=lambda: setattr(st.session_state, 'tela', 'MENU'), use_container_width=True, type="primary")