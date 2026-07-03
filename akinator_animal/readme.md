IA Akinator de Animais

Um sistema inteligente de perguntas e respostas no estilo **Akinator**, desenvolvido para identificar animais pensados pelo usuário. O projeto utiliza raciocínio probabilístico e o **Algoritmo ID3 (Entropia de Shannon)** para selecionar dinamicamente a pergunta que melhor divide as hipóteses restantes, otimizando a busca.

---

## 🚀 Funcionalidades Principais

* **Motor de Inferência Inteligente (ID3):** Seleciona perguntas com base no cálculo em tempo real do **Ganho de Informação**, convergindo rapidamente para a resposta.
* **Arquitetura Desacoplada:** A base de dados (`base_conhecimento.json`) é separada da lógica computacional (`akinator_animal.py`), facilitando manutenções e expansões do domínio.
* **Tolerância a Ruído e Incerteza:** Estruturado com sistema de pontuação (*Soft Pruning*) e alta redundância (24 animais por 26 atributos taxonômicos/comportamentais), permitindo acertos mesmo quando o usuário responde **"Não Sei"** ou erra algumas questões.
* **Registro Acumulativo de Sessão:** Gera relatórios em `.txt` com o histórico de perguntas, respostas e conclusões de todas as partidas jogadas.
* **Saída de Emergência (IHM):** Botão de desistência acessível em qualquer etapa, retornando ao menu inicial sem corromper os logs.

---

## 📁 Estrutura de Arquivos

Certifique-se de que os seguintes arquivos estejam no mesmo diretório:

---

## 🛠️ Pré-requisitos e Dependências

Para rodar o projeto localmente, você precisará ter o **Python 3.8+** instalado em sua máquina.

### Dependências

A principal biblioteca externa necessária é o **Streamlit** (para a interface gráfica web) e o **Pandas** (caso utilize manipulações tabulares auxiliares). As bibliotecas matemáticas (`math`, `random`, `json`) já são nativas do Python.

---

## 💻 Como Executar o Projeto

Siga o passo a passo abaixo no terminal (Prompt de Comando, PowerShell ou Terminal do VS Code):

### 1. Instalar as dependências

Abra o terminal na pasta onde os arquivos estão localizados e execute:

```bash
pip install streamlit pandas
```

### 2. Executar a aplicação web

Com as dependências instaladas, inicie o servidor local do Streamlit executando:

```bash
streamlit run akinator_animal.py
```

### 3. Acessar o sistema

O seu navegador padrão se abrirá automaticamente com o sistema rodando no endereço local:
👉 `http://localhost:8501`
