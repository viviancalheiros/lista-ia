import streamlit as st
import random
import math
import json

# --- 1. CARREGAMENTO DA BASE DE CONHECIMENTO JSON ---
# Lê o arquivo JSON externo e converte para dicionários nativos do Python
@st.cache_data
def carregar_base_conhecimento():
    with open("base_conhecimento.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados["animais"], dados["perguntas"]

BASE_CONHECIMENTO, PERGUNTAS_TEXTO = carregar_base_conhecimento()

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

# --- [FUNCIONALIDADE DE LOG ACUMULATIVO] Função criadora do documento ---
def gerar_log_txt():
    """Gera a string contendo o histórico de TODAS as partidas completas da sessão."""
    texto = "=== REGISTRO ACUMULADO DE PARTIDAS - AKINATOR IA ===\n\n"
    
    if not st.session_state.partidas_salvas:
        return "Nenhum histórico de partida concluída disponível para esta sessão."
    
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

# [FUNCIONALIDADE DE LOG ACUMULATIVO]
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
    st.session_state.historico_atual.append((PERGUNTAS_TEXTO[perg], resp))
    
    if resp == 'SIM':
        st.session_state.candidatos = [a for a in st.session_state.candidatos if BASE_CONHECIMENTO[a].get(perg) is True]
    elif resp == 'NAO':
        st.session_state.candidatos = [a for a in st.session_state.candidatos if BASE_CONHECIMENTO[a].get(perg, False) is False]
        
    if len(st.session_state.candidatos) <= 1 or not selecionar_pergunta():
        st.session_state.tela = 'RESULTADO'
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
        st.session_state.historico_atual = []
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