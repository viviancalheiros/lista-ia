import json

class Rule:
    def __init__(self, id_regra, antecedente, consequente):
        self.id = id_regra
        self.antecedente = antecedente
        self.consequente = consequente

    def __repr__(self):
        ant = " E ".join([f"{k} = {v}" for k, v in self.antecedente.items()])
        con = " E ".join([f"{k} = {v}" for k, v in self.consequente.items()])
        return f"{self.id}: SE {ant} ENTAO {con}"

class KnowledgeBase:
    def __init__(self):
        self.regras = []
        self.fatos = {}
        self.justificativas = {}

    def adicionar_regra(self, regra):
        self.regras.append(regra)

    def adicionar_fato(self, chave, valor, motivo="Informado pelo usuário"):
        self.fatos[chave] = valor
        self.justificativas[chave] = motivo

    def limpar_fatos(self):
        self.fatos.clear()
        self.justificativas.clear()

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
            resp = input(f"O valor de '{var}' é necessário. [Digite 'sim', 'nao' ou 'pq']: ").strip()
            if resp.lower() in ['pq', 'pq?']:
                if regra_contexto:
                    print("\n[EXPLICAÇÃO] ")
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
        if variavel not in kb.fatos:
            print(f"A variável '{variavel}' ainda não foi determinada.")
            return
        motivo = kb.justificativas.get(variavel, "Desconhecido")
        print(f"\n[COMO] Conclusão para '{variavel} = {kb.fatos[variavel]}':")
        print(f"-> {motivo}\n")

def menu_sistema():
    kb = KnowledgeBase()
    try:
        kb.carregar_base('base.json')
    except FileNotFoundError:
        print("Erro: O arquivo 'base.json' não foi encontrado na mesma pasta.")
        return

    engine = InferenceEngine(kb)
    while True:
        print("\n=============================================")
        print("   SHELL DE SISTEMA BASEADO EM CONHECIMENTO  ")
        print("=============================================")
        print("1. Executar Consulta Diagnóstica (Híbrida)")
        print("2. Explicar Conclusão (COMO?)")
        print("3. Visualizar Regras Carregadas")
        print("4. Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == '1':
            kb.limpar_fatos()
            engine.hybrid_chaining("Diagnóstico")
            engine.forward_chaining()
            print("\n================ RESULTADO ================")
            print(f"Diagnóstico Final: {kb.fatos.get('Diagnóstico', 'Não foi possível determinar.')}")
            print(f"Recomendação de Ação: {kb.fatos.get('Recomendação', 'Nenhuma cadastrada para este caso.')}")
            print("===========================================")
        elif opcao == '2':
            var = input("De qual variável deseja ver a explicação 'COMO'? ").strip()
            ExplanationMechanism.como(kb, var)
        elif opcao == '3':
            print("\n--- Regras na Base de Conhecimento ---")
            for r in kb.regras:
                print(r)
        elif opcao == '4':
            break

if __name__ == "__main__":
    menu_sistema()