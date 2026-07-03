import streamlit as st
import pandas as pd

# --- 1. CONFIGURAÇÃO E DADOS INICIAIS ---
st.set_page_config(page_title="Sistema CBR Médico", page_icon="🩺", layout="wide")

# Lista expandida para 12 atributos lógicos (prevenção da Maldição da Dimensionalidade)
SINTOMAS_LISTA = [
    "Febre", "Dor de Cabeça", "Tosse", "Dor Muscular", 
    "Enjoo/Vômito", "Diarreia", "Manchas na Pele", "Perda de Olfato/Paladar",
    "Dor de Garganta", "Falta de Ar", "Coriza", "Sensibilidade à Luz"
]

# Base de Casos: 25 casos, 8 doenças
CASOS_INICIAIS = [
    # GRIPE 
    {"id": 1, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": True, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": True, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Gripe", "tratamento": "Repouso, hidratação e antitérmicos."},
    {"id": 2, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Gripe", "tratamento": "Repouso e hidratação."},
    {"id": 3, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": True, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Gripe (Leve)", "tratamento": "Chás quentes e analgésicos leves."},

    # DENGUE 
    {"id": 4, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": True, "Diarreia": False, "Manchas na Pele": True, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Dengue", "tratamento": "Hidratação intensa, evitar AAS. Repouso absoluto."},
    {"id": 5, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Dengue", "tratamento": "Acompanhamento médico, hidratação via oral."},
    
    # COVID-19 
    {"id": 6, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": True, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": True, "Dor de Garganta": True, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "COVID-19", "tratamento": "Isolamento, repouso e monitoramento."},
    {"id": 7, "sintomas": {"Febre": True, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": True, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "COVID-19 (Atenção Respiratória)", "tratamento": "Isolamento e busca imediata por avaliação de saturação de oxigênio."},
    {"id": 8, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": True, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "COVID-19", "tratamento": "Isolamento e uso de analgésicos."},

    # INTOXICAÇÃO ALIMENTAR 
    {"id": 9, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": True, "Diarreia": True, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Intoxicação Alimentar", "tratamento": "Soro caseiro, dieta leve e hidratação."},
    {"id": 10, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": True, "Diarreia": True, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Intoxicação Alimentar (Quadro Infeccioso)", "tratamento": "Repouso, medicamentos para náusea e avaliação médica."},

    # ENXAQUECA 
    {"id": 11, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": True, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": True}, "diagnostico": "Enxaqueca", "tratamento": "Repouso em local escuro e silencioso, analgésicos específicos."},
    {"id": 12, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": True}, "diagnostico": "Enxaqueca", "tratamento": "Uso de analgésicos e evitar exposição a telas e luz solar."},
    {"id": 13, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Cefaleia Tensional", "tratamento": "Relaxante muscular e controle de estresse."},

    # ZIKA 
    {"id": 14, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": True, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Zika Vírus", "tratamento": "Repouso, ingestão de líquidos e anti-histamínicos para alergia na pele."},
    {"id": 15, "sintomas": {"Febre": True, "Dor de Cabeça": False, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": True, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Zika Vírus", "tratamento": "Acompanhamento médico. Especial atenção se houver gravidez."},

    # ASMA 
    {"id": 16, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": True, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Asma / Crise Alérgica", "tratamento": "Uso de broncodilatadores (bombinha) e evitar alérgenos."},
    {"id": 17, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": True, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Asma induzida por rinite", "tratamento": "Antialérgicos e acompanhamento pneumológico."},

    # MENINGITE
    {"id": 18, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": True, "Diarreia": False, "Manchas na Pele": True, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": True}, "diagnostico": "Meningite (ALERTA GRAVE)", "tratamento": "BUSCAR PRONTO-SOCORRO IMEDIATAMENTE. Isolamento e possível uso de antibióticos venosos."},
    {"id": 19, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": True, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": True}, "diagnostico": "Suspeita de Meningite", "tratamento": "Avaliação médica urgente para descarte de quadro neurológico severo."},

    # VARIAÇÕES PARA ROBUSTEZ (Ruído natural)
    {"id": 20, "sintomas": {"Febre": True, "Dor de Cabeça": True, "Tosse": True, "Dor Muscular": True, "Enjoo/Vômito": True, "Diarreia": True, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": True, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Gripe com quadro gastrointestinal", "tratamento": "Hidratação rigorosa, repouso e antitérmicos."},
    {"id": 21, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": True, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Tensão / Estresse físico", "tratamento": "Descanso, relaxante muscular e hidratação."},
    {"id": 22, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": True, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Alergia Dermatológica", "tratamento": "Lavar o local com água fria e aplicar pomada anti-histamínica."},
    {"id": 23, "sintomas": {"Febre": True, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": True, "Falta de Ar": False, "Coriza": False, "Sensibilidade à Luz": False}, "diagnostico": "Amigdalite / Faringite", "tratamento": "Avaliação médica para possível prescrição de antibióticos."},
    {"id": 24, "sintomas": {"Febre": False, "Dor de Cabeça": False, "Tosse": True, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Resfriado Comum", "tratamento": "Repouso e lavagem nasal com soro fisiológico."},
    {"id": 25, "sintomas": {"Febre": False, "Dor de Cabeça": True, "Tosse": False, "Dor Muscular": False, "Enjoo/Vômito": False, "Diarreia": False, "Manchas na Pele": False, "Perda de Olfato/Paladar": False, "Dor de Garganta": False, "Falta de Ar": False, "Coriza": True, "Sensibilidade à Luz": False}, "diagnostico": "Sinusite", "tratamento": "Lavagem nasal constante, hidratação e analgésicos."}
]

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
    
    # Loop ajustado para distribuir dinamicamente os 12 sintomas nas colunas
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