# Arquivo: app.py
import streamlit as st
import pandas as pd
import joblib
import numpy as np


st.set_page_config(page_title="Análise de Vulnerabilidade Digital", layout="wide")

st.title("Sistema de Apoio: Análise de Vulnerabilidade Digital")
st.markdown("""
Este sistema utiliza **Machine Learning** para identificar clientes que podem estar enfrentando dificuldades técnicas ou de acessibilidade.
""")

st.divider()

# Carregar o Modelo
@st.cache_resource
def carregar_modelo():
    try:
        return joblib.load('./model/model.joblib')
    except:
        st.error("Erro: Arquivo 'model.joblib' não encontrado.")
        return None

modelo = carregar_modelo()

# Sidebar (Inputs de indicadores)
st.sidebar.header("Perfil do Cliente")
st.sidebar.info("Insira os dados coletados na solicitação.")

# Inputs do Usuário (Valores padrão = Perfil Dona Nair)
idade = st.sidebar.number_input("Idade", min_value=18, max_value=100, value=67)
renda = st.sidebar.number_input("Renda Anual (R$)", value=18000.0)
beneficiario = st.sidebar.selectbox("Beneficiário INSS?", ["Não", "Sim"], index=1)
regiao = st.sidebar.selectbox("Região", ["Capital", "Interior"], index=1)
tempo_app = st.sidebar.slider("Tempo na Sessão do App (min)", 0.0, 60.0, 15.5)
erro_pct = st.sidebar.slider("Taxa de Erro de Digitação (%)", 0.0, 100.0, 18.0)
contato_suporte = st.sidebar.selectbox("Entrou em contato com Suporte recente?", ["Não", "Sim"], index=1)
pagamento_em_dia = st.sidebar.selectbox("Histórico de Pagamento em dia?", ["Não", "Sim"], index=1)

# Inputs secundários
st.sidebar.markdown("---")
st.sidebar.markdown("**Outros Indicadores**")
tem_emprestimo = st.sidebar.checkbox("Já tem empréstimo?", value=False)
tem_seguro = st.sidebar.checkbox("Já tem seguro?", value=False)
hist_problemas = st.sidebar.checkbox("Histórico de Problemas?", value=False)
visita_agente = st.sidebar.checkbox("Recebeu visita de agente?", value=False)

# Processamento dos inputs

if st.button("Analisar Perfil do Cliente", type="primary"):
    if modelo:
        
        # Preparar os dados para o método predict
        input_data = pd.DataFrame({
            'idade': [idade],
            'renda_anual': [renda],
            'beneficiario_inss': [1 if beneficiario == "Sim" else 0],
            'tem_emprestimo': [1 if tem_emprestimo else 0],
            'tem_seguro': [1 if tem_seguro else 0],
            'historico_problemas': [1 if hist_problemas else 0],
            'contato_suporte': [1 if contato_suporte == "Sim" else 0],
            'visita_agente': [1 if visita_agente else 0],
            'tempo_medio_app_min': [tempo_app],
            'erro_digitacao_pct': [erro_pct],
            'pagamento_em_dia': [1 if pagamento_em_dia == "Sim" else 0],
            'regiao_Interior': [1 if regiao == "Interior" else 0] 
        })

        # Previsão (.predict)
        classe = modelo.predict(input_data)[0]
        probabilidade = modelo.predict_proba(input_data)[0][1] # Probabilidade da classe 1

        # 3. Exibição dos Resultados
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Resultado da Análise")
            if classe == 1:
                st.error("⚠️ VULNERABILIDADE DIGITAL DETECTADA")
                st.markdown(f"**Probabilidade:** {probabilidade*100:.2f}%")
                st.markdown("""
                **Ação Recomendada:** * 🛑 **Não reprovar automaticamente.**
                * Encaminhar para fila de atendimento humanizado (Prioridade Alta).
                * Perfil compatível com dificuldade tecnológica.
                """)
            else:
                st.success("✅ CLIENTE COM AUTONOMIA DIGITAL")
                st.markdown(f"**Probabilidade de Vulnerabilidade:** {probabilidade*100:.2f}%")
                st.markdown("""
                **Ação Recomendada:** 
                * Seguir fluxo padrão de aprovação de crédito.
                """)

        with col2:
            st.subheader("Fatores Críticos")
            # Exibir métricas visuais
            st.progress(int(probabilidade * 100), text="Índice de Risco de Exclusão Digital")
            
            # Destaque para o que mais impacta (Regra de negócio visual)
            if idade > 60:
                st.warning(f"⚠️ Idade ({idade} anos) é um fator de atenção.")
            if (erro_pct > 10) and (erro_pct <= 30):
                st.warning(f"⚠️ Taxa de erro ({erro_pct}%) está acima da média.")
            elif erro_pct > 30:
                st.error(f"🛑 Atenção perfil com alta taxa de erro ({erro_pct}%)")
            if (tempo_app > 10) and (tempo_app <= 30):
                st.warning(f"⚠️ Tempo no app ({tempo_app} min) indica dificuldade.")
            elif tempo_app > 30:
                st.error(f"🛑 Atenção perfil com tempo no app muito alto ({tempo_app} min)")