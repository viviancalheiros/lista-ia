import streamlit as st
import pandas as pd
import json

# --- 1. CONFIGURAÇÃO E CARREGAMENTO DA BASE EXTERNA ---
st.set_page_config(page_title="Sistema CBR Médico", page_icon="🩺", layout="wide")

# Função em cache para carregar a base de dados em JSON
@st.cache_data
def carregar_base_cbr():
    with open("base_casos_medicos.json", "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    return dados["sintomas_lista"], dados["casos_iniciais"]

SINTOMAS_LISTA, CASOS_INICIAIS = carregar_base_cbr()

# Inicializa a base de casos na sessão para permitir a retenção (aprendizado)
if 'base_casos' not in st.session_state:
    st.session_state.base_casos = CASOS_INICIAIS

# --- 2. MOTOR DO CBR (CÁLCULO DE SIMILARIDADE) ---
def calcular_similaridade_jaccard(sintomas_novo, sintomas_caso_base):
    """Calcula a similaridade de Jaccard entre dois vetores de sintomas (True/False)"""
    set_novo = set([s for s, presente in sintomas_novo.items() if presente])
    set_base = set([s for s, presente in sintomas_caso_base.items() if presente])
    
    intersecao = len(set_novo.intersection(set_base))
    uniao = len(set_novo.union(set_base))
    
    if uniao == 0: 
        return 0.0 # Se nenhum sintoma foi relatado em ambos
    return intersecao / uniao

# --- 3. INTERFACE DE USUÁRIO ---
st.title("🩺 Sistema de Diagnóstico Médico (CBR)")
st.write("Raciocínio Baseado em Casos: Recupere, Reutilize, Revise e Retenha.")

tab1, tab2 = st.tabs(["Nova Consulta (Diagnóstico)", "Base de Conhecimento (Casos)"])

with tab1:
    st.header("1. Informar Sintomas")
    st.write("Marque os sintomas que o paciente está apresentando:")
    
    col1, col2 = st.columns(2)
    sintomas_atuais = {}
    
    # Loop ajustado para distribuir dinamicamente os sintomas nas colunas
    for i, sintoma in enumerate(SINTOMAS_LISTA):
        if i % 2 == 0:
            sintomas_atuais[sintoma] = col1.checkbox(sintoma)
        else:
            sintomas_atuais[sintoma] = col2.checkbox(sintoma)

    if st.button("Analisar Caso", type="primary"):
        # Verifica se pelo menos um sintoma foi marcado
        if not any(sintomas_atuais.values()):
            st.warning("Por favor, selecione pelo menos um sintoma.")
        else:
            # --- ETAPA 1: RETRIEVE (Recuperação) ---
            resultados = []
            for caso in st.session_state.base_casos:
                sim = calcular_similaridade_jaccard(sintomas_atuais, caso["sintomas"])
                resultados.append({"caso": caso, "similaridade": sim})
            
            # Ordena pelos mais similares (decrescente)
            resultados = sorted(resultados, key=lambda x: x["similaridade"], reverse=True)
            casos_similares = resultados[:3] # Pega os 3 mais próximos
            
            st.markdown("---")
            st.header("2. Casos Recuperados (Retrieve)")
            
            # Mostra os casos recuperados
            cols_casos = st.columns(3)
            for i, res in enumerate(casos_similares):
                with cols_casos[i]:
                    st.info(f"**Caso #{res['caso']['id']}**\n\n"
                            f"**Similaridade:** {res['similaridade']*100:.1f}%\n\n"
                            f"**Diag.:** {res['caso']['diagnostico']}")
            
            # --- ETAPA 2: REUSE (Reutilização) ---
            st.markdown("---")
            st.header("3. Diagnóstico Sugerido (Reuse)")
            
            melhor_caso = casos_similares[0]['caso']
            confianca = casos_similares[0]['similaridade'] * 100
            
            st.success(f"**Diagnóstico Baseado no Histórico:** {melhor_caso['diagnostico']} (Confiança: {confianca:.1f}%)")
            st.write(f"**Tratamento Sugerido:** {melhor_caso['tratamento']}")
            
            # Guardamos o caso atual na sessão para a etapa de revisão
            st.session_state.caso_em_analise = sintomas_atuais
            st.session_state.diag_sugerido = melhor_caso['diagnostico']
            st.session_state.trat_sugerido = melhor_caso['tratamento']

# --- ETAPA 3 e 4: REVISE E RETAIN (Revisão e Retenção) ---
    if 'caso_em_analise' in st.session_state:
        st.markdown("---")
        st.header("4. Validação do Especialista (Revise & Retain)")
        st.write("O diagnóstico sugerido está correto? Caso o médico discorde ou queira refinar o tratamento, ele pode alterar os dados abaixo e salvar este novo caso na base para o sistema aprender.")
        
        with st.form("form_retencao"):
            novo_diag = st.text_input("Diagnóstico Final do Médico:", value=st.session_state.diag_sugerido)
            novo_trat = st.text_area("Tratamento Recomendado:", value=st.session_state.trat_sugerido)
            
            if st.form_submit_button("Aprovar e Salvar Novo Caso (Retain)"):
                novo_id = len(st.session_state.base_casos) + 1
                novo_caso = {
                    "id": novo_id,
                    "sintomas": st.session_state.caso_em_analise,
                    "diagnostico": novo_diag,
                    "tratamento": novo_trat
                }
                st.session_state.base_casos.append(novo_caso)
                del st.session_state['caso_em_analise'] # Limpa a tela
                st.success(f"Novo caso #{novo_id} retido com sucesso! O sistema acabou de aprender.")
                st.rerun()

with tab2:
    st.header("Base de Conhecimento de Casos")
    st.write(f"Total de casos armazenados: **{len(st.session_state.base_casos)}**")
    
    # Formata os dados para exibição em tabela
    df_casos = []
    for caso in st.session_state.base_casos:
        linha = {"ID": caso["id"], "Diagnóstico": caso["diagnostico"], "Tratamento": caso["tratamento"]}
        for sint, pres in caso["sintomas"].items():
            linha[sint] = "Sim" if pres else "Não"
        df_casos.append(linha)
        
    st.dataframe(pd.DataFrame(df_casos), use_container_width=True)