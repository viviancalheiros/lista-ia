import json

class Rule:
    def __init__(self, id_regra, antecedente, consequente):
        self.id = id_regra
        self.antecedente = antecedente  # Dicionário ex: {"Dor nos olhos": "sim"}
        self.consequente = consequente  # Dicionário ex: {"Diagnóstico": "Miopia"}

    def __repr__(self):
        ant = " E ".join([f"'{k}' = '{v}'" for k, v in self.antecedente.items()])
        con = " E ".join([f"'{k}' = '{v}'" for k, v in self.consequente.items()])
        return f"{self.id}: SE {ant} ENTAO {con}"


class KnowledgeBase:
    def __init__(self):
        self.regras = []
        self.fatos = {}  # Memória da consulta atual
        self.justificativas = {}

    def adicionar_regra(self, regra):
        self.regras.append(regra)

    def remover_regra(self, id_regra):
        regras_filtradas = [r for r in self.regras if r.id != id_regra]
        if len(regras_filtradas) == len(self.regras):
            return False
        self.regras = regras_filtradas
        return True

    def alterar_regra(self, id_regra, novo_antecedente, novo_consequente):
        for regra in self.regras:
            if regra.id == id_regra:
                regra.antecedente = novo_antecedente
                regra.consequente = novo_consequente
                return True
        return False

    def adicionar_fato(self, chave, valor, motivo="Informado pelo usuário"):
        self.fatos[chave] = valor
        self.justificativas[chave] = motivo

    def limpar_fatos(self):
        self.fatos.clear()
        self.justificativas.clear()

    def salvar_base(self, caminho_arquivo):
        dados = {
            "regras": [{"id": r.id, "ant": r.antecedente, "con": r.consequente} for r in self.regras]
        }
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    def carregar_base(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            self.regras = [Rule(r["id"], r["ant"], r["con"]) for r in dados["regras"]]


class InferenceEngine:
    def __init__(self, kb):
        self.kb = kb
        self.historico_perguntas = []

    def forward_chaining(self):
        mudou = True
        regras_disparadas = set()
        while mudou:
            mudou = False
            for regra in self.kb.regras:
                if regra.id in regras_disparadas:
                    continue
                condicoes_atendidas = True
                for var, val in regra.antecedente.items():
                    if var not in self.kb.fatos or self.kb.fatos[var] != val:
                        condicoes_atendidas = False
                        break
                if condicoes_atendidas:
                    for var_con, val_con in regra.consequente.items():
                        if var_con not in self.kb.fatos:
                            self.kb.adicionar_fato(var_con, val_con, f"Inferido via {regra.id}")
                            mudou = True
                    regras_disparadas.add(regra.id)
        return self.kb.fatos

    def backward_chaining(self, objetivo_var, objetivo_val=None, regra_contexto=None):
        if objetivo_var in self.kb.fatos:
            if objetivo_val is None or self.kb.fatos[objetivo_var] == objetivo_val:
                return True
            return False

        regras_candidatas = [r for r in self.kb.regras if objetivo_var in r.consequente]
        for regra in regras_candidatas:
            if objetivo_val is not None and regra.consequente[objetivo_var] != objetivo_val:
                continue
            sub_objetivos_provados = True
            for var_ant, val_ant in regra.antecedente.items():
                self.historico_perguntas.append((var_ant, regra))
                provado = self.backward_chaining(var_ant, val_ant, regra)
                self.historico_perguntas.pop()
                if not provado:
                    sub_objetivos_provados = False
                    break
            if sub_objetivos_provados:
                for var_con, val_con in regra.consequente.items():
                    if var_con not in self.kb.fatos:
                        self.kb.adicionar_fato(var_con, val_con, f"Inferido via {regra.id}")
                return True

        if objetivo_val is not None:
            resposta = self.solicitar_usuario(objetivo_var, regra_contexto)
            if resposta == objetivo_val:
                return True
        return False

    def solicitar_usuario(self, var, regra_contexto):
        if var in self.kb.fatos:
            return self.kb.fatos[var]
        while True:
            resp = input(f"O valor de '{var}' é necessário. [Digite o 'sim', 'nao' ou 'pq']: ").strip()
            
            if resp.lower() in ['pq', 'pq?']:
                if regra_contexto:
                    print(f"\n[EXPLICAÇÃO] Estou perguntando sobre '{var}' porque estou validando a regra {regra_contexto.id}:")
                    print(f"-> {regra_contexto}\n")
                else:
                    print("\n[EXPLICAÇÃO] Esta informação é necessária como um fato inicial do sistema.\n")
                continue
            
            self.kb.adicionar_fato(var, resp, "Fornecido pelo usuário")
            return resp

    def hybrid_chaining(self, hipotese_var):
        print("\n--- Executando Encadeamento Híbrido ---")
        self.forward_chaining()
        if hipotese_var in self.kb.fatos:
            return self.kb.fatos[hipotese_var]
        self.backward_chaining(hipotese_var)
        self.forward_chaining()
        return self.kb.fatos.get(hipotese_var, "Inconclusivo")

class ExplanationMechanism:
    @staticmethod
    def como(kb, variavel):
        motivo = kb.justificativas.get(variavel, "Desconhecido")
        print(f"\n[COMO] Conclusão para '{variavel} = {kb.fatos[variavel]}':")
        if "Inferido via" in motivo:
            id_regra = motivo.split("via ")[1]
            regra_objeto = next((r for r in kb.regras if r.id == id_regra), None)
            if regra_objeto:
                print(f"-> Inferido via {regra_objeto}\n")
            else:
                print(f"-> Inferido via {id_regra} -> regra não encontrada na base\n")
        else:
            print(f"-> {motivo}\n")

def menu_sistema():
    kb = KnowledgeBase()
    arquivo_nome = 'base.json'
    
    try:
        kb.carregar_base(arquivo_nome)
    except FileNotFoundError:
        print(f"Aviso: Arquivo '{arquivo_nome}' não encontrado.")
        return

    engine = InferenceEngine(kb)
    while True:
        print("\n=============================================")
        print("   SHELL DE SISTEMA BASEADO EM CONHECIMENTO  ")
        print("=============================================")
        print("1. Executar consulta diagnóstica")
        print("2. Explicar conclusão do último diagnóstico (COMO)")
        print("3. Visualizar regras carregadas")
        print("4. Cadastrar nova regra")
        print("5. Alterar regra existente")
        print("6. Remover regra existente")
        print("7. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            kb.limpar_fatos()
            engine.hybrid_chaining("Diagnóstico")
            print("\n================ RESULTADO ================")
            print(f"Diagnóstico Final: {kb.fatos.get('Diagnóstico', 'Não foi possível determinar.')}")
            print(f"Recomendação de Ação: {kb.fatos.get('Recomendação', 'Nenhuma cadastrada para este caso.')}")
            print("===========================================")
        elif opcao == '2':
            ExplanationMechanism.como(kb, "Diagnóstico")
        elif opcao == '3':
            print("\n--- Regras na Base de Conhecimento ---")
            for r in kb.regras:
                print(r)
        elif opcao == '4':
            id_r = input("Digite o ID da nova regra (ex: R22): ").strip()
            if any(r.id == id_r for r in kb.regras):
                print("Erro: Já existe uma regra com esse ID.")
                continue
            ant = {}
            print("Defina as condições (SE). Deixe vazio no nome para encerrar.")
            while True:
                var = input("Nome do sintoma/fato: ").strip()
                if not var: break
                val = input(f"Valor esperado para '{var}' (ex: sim): ").strip()
                ant[var] = val
            con = {}
            print("Defina a conclusão (ENTÃO).")
            var_c = input("Nome da variável de conclusão (ex: Diagnóstico): ").strip()
            val_c = input(f"Valor da conclusão para '{var_c}': ").strip()
            con[var_c] = val_c
            if ant and con:
                kb.adicionar_regra(Rule(id_r, ant, con))
                kb.salvar_base(arquivo_nome)
                print(f"Regra {id_r} cadastrada e salva com sucesso!")
        elif opcao == '5':
            print("\n--- Regras na Base de Conhecimento ---")
            for r in kb.regras:
                print(r)
            print("\n")
            id_r = input("Digite o ID da regra que deseja alterar: ").strip()
            regra_atual = next((r for r in kb.regras if r.id == id_r), None)
            if not regra_atual:
                print("Erro: Regra não encontrada.")
                continue
            novos_antecedentes = regra_atual.antecedente.copy()
            nova_conclusao = regra_atual.consequente.copy()
            
            # --- PASSO 1: Adicionar novos sintomas/fatos ---
            print("\n--- 1. ADICIONAR NOVOS SINTOMAS/FATOS ---")
            add_novo = input("Deseja adicionar um novo sintoma/fato a esta regra? (sim/nao): ").strip().lower()
            if add_novo == 'sim':
                print("Digite as novas condições. Deixe o nome vazio para encerrar.")
                while True:
                    var = input("Nome do novo sintoma/fato: ").strip()
                    if not var: break
                    val = input(f"Valor esperado para '{var}' (ex: sim): ").strip()
                    novos_antecedentes[var] = val

            # --- PASSO 2: Alterar sintomas/fatos já existentes ---
            print("\n--- 2. ALTERAR SINTOMAS/FATOS EXISTENTES ---")
            alt_existente = input("Deseja alterar o valor de algum sintoma já existente nesta regra? (sim/nao): ").strip().lower()
            if alt_existente == 'sim':
                print("\nSintomas atuais nesta regra:")
                for k, v in novos_antecedentes.items():
                    print(f" -> '{k}' = '{v}'")
                while True:
                    var = input("\nDigite o nome EXATO do sintoma que quer alterar (ou deixe vazio para encerrar): ").strip()
                    if not var: break
                    if var in novos_antecedentes:
                        novo_val = input(f"Digite o NOVO valor para '{var}': ").strip()
                        novos_antecedentes[var] = novo_val
                        print(f"Sintoma '{var}' atualizado temporariamente.")
                    else:
                        print("Esse sintoma não existe nesta regra. Tente novamente.")

            # --- PASSO 3: Alterar a conclusão ---
            print("\n--- 3. CONCLUSÃO (ENTÃO) ---")
            manter_conclusao = input(f"A conclusão atual é {nova_conclusao}. Deseja alterar? (sim/nao): ").strip().lower()
            if manter_conclusao == 'sim':
                nova_conclusao.clear()
                var_c = input("Nome da NOVA variável de conclusão (ex: Diagnóstico): ").strip()
                val_c = input(f"Valor da conclusão para '{var_c}': ").strip()
                nova_conclusao[var_c] = val_c
            if kb.alterar_regra(id_r, novos_antecedentes, nova_conclusao):
                kb.salvar_base(arquivo_nome)
                regra_atualizada = next((r for r in kb.regras if r.id == id_r), None)
                print(f"\n[SUCESSO] Regra {id_r} alterada e salva com sucesso!")
                print(f"Nova estrutura -> {regra_atualizada}")
        elif opcao == '6':
            print("\n--- Regras na Base de Conhecimento ---")
            for r in kb.regras:
                print(r)
            print("\n")
            id_r = input("Digite o ID da regra que deseja remover: ").strip()
            if kb.remover_regra(id_r):
                kb.salvar_base(arquivo_nome)
                print(f"Regra {id_r} removida com sucesso!")
            else:
                print("Erro: Regra não encontrada.")
        elif opcao == '7':
            print("Encerrando o sistema...")
            break

if __name__ == "__main__":
    menu_sistema()