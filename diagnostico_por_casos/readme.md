🩺 Sistema de Diagnóstico Médico (CBR) — Raciocínio Baseado em Casos

Um sistema especialista de apoio à decisão clínica desenvolvido em Python e Streamlit, baseado no paradigma de Inteligência Artificial de **Raciocínio Baseado em Casos (CBR - *Case-Based Reasoning*)**. O sistema auxilia no pré-diagnóstico médico ao comparar os sintomas apresentados por um novo paciente com uma base histórica de casos clínicos, utilizando o **Índice de Similaridade de Jaccard**.

---

## 🚀 Funcionalidades Principais (O Ciclo 4R do CBR)

O projeto implementa integralmente as quatro etapas clássicas da metodologia CBR:

1. **Recuperação (*Retrieve*):**

   * Compara o vetor binário de sintomas do paciente atual com os **25 casos clínicos históricos** armazenados na base de conhecimento.
   * Aplica o **Índice de Similaridade de Jaccard** para identificar e apresentar os 3 casos históricos mais semelhantes.
2. **Reutilização (*Reuse*):**

   * Sugere automaticamente o diagnóstico e a conduta terapêutica (tratamento) do caso histórico com maior percentagem de similaridade, apresentando o respectivo nível de confiança.
3. **Revisão (*Revise*):**

   * Permite que o médico especialista (utilizador do sistema) analise o diagnóstico e o tratamento sugeridos, possibilitando a edição e validação clínica das informações antes de as aprovar.
4. **Retenção (*Retain* / Aprendizagem Contínua):**

   * Ao aprovar e validar uma nova consulta, o sistema armazena o novo par *(Problema, Solução)* na memória da sessão (`session_state`). O sistema aprende dinamicamente com novos casos sem necessidade de reprogramação.

---

## 📁 Estrutura de Ficheiros

O projeto utiliza uma arquitetura desacoplada, separando o motor de inferência computacional da base de conhecimento médica:

---

## 🛠️ Pré-requisitos e Dependências

Para executar o projeto localmente, é necessário ter o **Python 3.8+** instalado no sistema.

### Dependências Necessárias

O sistema consome as bibliotecas **Streamlit** (para a interface interativa em abas) e **Pandas** (para a formatação tabular dos casos retidos). As bibliotecas de manipulação de conjuntos e leitura JSON já fazem parte da biblioteca padrão do Python.

---

## 💻 Como Executar o Projeto

Abra o terminal (Prompt de Comando, PowerShell ou Terminal do VS Code) na pasta onde se encontram os ficheiros e siga os passos abaixo:

### 1. Instalar as dependências

```bash
pip install streamlit pandas
```

### 2. Executar a aplicação web

```bash
streamlit run cbr_medico.py
```

### 3. Acessar o sistema

Após a execução, o navegador abrirá automaticamente a interface do sistema no endereço:
👉 `http://localhost:8501`

---

## 📐 Fundamentação Teórica: Índice de Jaccard

Na área médica, a ausência simultânea de sintomas (ambos os pacientes não apresentarem diarreia, por exemplo) não é um indicador forte de que partilham a mesma patologia. Por esta razão, o sistema adota o **Índice de Similaridade de Jaccard**, que foca apenas nos atributos positivos (presentes):

$$
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$

Onde:

* $A$ é o conjunto de sintomas ativos marcados para o paciente atual.
* $B$ é o conjunto de sintomas ativos registados no caso histórico da base de dados.
* A intersecção $|A \cap B|$ representa os sintomas partilhados entre ambos.
* A união $|A \cup B|$ representa o total de sintomas distintos observados considerando ambos os quadros clínicos.
