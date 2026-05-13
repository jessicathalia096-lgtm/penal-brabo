# -*- coding: utf-8 -*-
"""
TESTE PENAL - ROTA PENAL CE
Compatível com python-telegram-bot==13.15

Instalar:
pip install python-telegram-bot==13.15

Rodar:
python teste_penal.py

IMPORTANTE:
Use BOT_TOKEN de um bot de TESTE, diferente do oficial, para não dar conflito.
"""

import os
import json
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext


BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [8450100073, 1130170420]

NOME_BOT = "🚔 TESTE PENAL CE"
ARQUIVO_DADOS = "dados_teste_penal.json"


NIVEIS = {
    "facil": "🟢 Patrulha Básica",
    "medio": "🟡 Operação Regional",
    "dificil": "🔴 Missão Tática",
    "caveira": "⚫ OPERAÇÃO CAVEIRA",
}


VIDEOAULAS = {
    "📚 Português IDECAN": "https://www.youtube.com/results?search_query=portugu%C3%AAs+IDECAN+concurso",
    "💻 Informática": "https://www.youtube.com/results?search_query=inform%C3%A1tica+concurso+pol%C3%ADcia+penal",
    "🧠 Raciocínio lógico": "https://www.youtube.com/results?search_query=racioc%C3%ADnio+l%C3%B3gico+concurso+pol%C3%ADcia",
    "⚖️ Constitucional": "https://www.youtube.com/results?search_query=direito+constitucional+pol%C3%ADcia+penal",
    "⚖️ Administrativo": "https://www.youtube.com/results?search_query=direito+administrativo+pol%C3%ADcia+penal",
    "🚔 Penal": "https://www.youtube.com/results?search_query=direito+penal+pol%C3%ADcia+penal",
    "🚔 Processo Penal": "https://www.youtube.com/results?search_query=processo+penal+pol%C3%ADcia+penal",
    "📖 LEP": "https://www.youtube.com/results?search_query=lei+de+execu%C3%A7%C3%A3o+penal+pol%C3%ADcia+penal",
    "🏛️ Direitos Humanos": "https://www.youtube.com/results?search_query=direitos+humanos+sistema+prisional",
    "🌎 Ceará/Fortaleza": "https://www.youtube.com/results?search_query=hist%C3%B3ria+geografia+atualidades+cear%C3%A1+concurso",
    "📕 Legislação específica PPCE": "https://www.youtube.com/results?search_query=legisla%C3%A7%C3%A3o+espec%C3%ADfica+pol%C3%ADcia+penal+cear%C3%A1",
}


def cabecalho(titulo):
    return "━━━━━━━━━━━━━━\n" + titulo + "\n━━━━━━━━━━━━━━"


def q(origem, nivel, materia, tema, correta, erradas, explicacao, discursiva=False):
    pergunta = montar_enunciado(nivel, tema)
    alternativas, correta_letra = alternativas_pegadinha(correta, erradas)

    return {
        "id": str(abs(hash(origem + nivel + materia + pergunta + correta))),
        "origem": origem,
        "nivel": nivel,
        "materia": materia,
        "pergunta": pergunta,
        "alternativas": alternativas,
        "correta": correta_letra,
        "explicacao": explicacao,
        "discursiva": discursiva,
    }


def alternativas_pegadinha(correta, erradas):
    itens = [correta] + erradas
    random.shuffle(itens)
    letras = ["A", "B", "C", "D", "E"]
    alternativas = []
    correta_letra = "A"

    for i, texto in enumerate(itens[:5]):
        alternativas.append(f"{letras[i]}) {texto}")
        if texto == correta:
            correta_letra = letras[i]

    return alternativas, correta_letra


def montar_enunciado(nivel, tema):
    if nivel == "facil":
        return (
            "📄 Situação hipotética\n\n"
            f"Em prova objetiva para carreira policial, a banca apresenta situação relacionada a {tema}. "
            "A questão exige atenção ao contexto, ao comando e à alternativa que melhor se harmoniza com a legislação, "
            "com os princípios constitucionais e com a atuação estatal em segurança pública. Assinale a alternativa correta."
        )

    if nivel == "medio":
        return (
            "📄 Situação hipotética\n\n"
            f"Durante estudo dirigido para concurso policial, foi apresentada situação envolvendo {tema}. "
            "Algumas alternativas trazem conceitos juridicamente verdadeiros, mas incompletos ou deslocados do contexto. "
            "Considerando a interpretação normativa, institucional e o padrão de cobrança da banca, assinale a opção correta."
        )

    if nivel == "dificil":
        return (
            "📄 Situação hipotética\n\n"
            f"Em contexto de segurança pública e sistema penitenciário, determinado servidor analisa situação prática envolvendo {tema}. "
            "A questão exige diferenciar legalidade, eficiência administrativa, dever funcional, preservação de direitos e responsabilidade institucional. "
            "À luz do ordenamento jurídico e da atuação policial, assinale a alternativa mais adequada."
        )

    return (
        "📄 Situação hipotética\n\n"
        f"Considere cenário complexo envolvendo {tema}, no qual há tensão entre eficiência estatal, legalidade, direitos fundamentais, "
        "segurança pública, gestão prisional, cadeia de responsabilidade e interpretação normativa. A questão foi elaborada com alternativas próximas, "
        "expressões absolutas e pegadinhas de generalização. Assinale a conclusão juridicamente e institucionalmente mais adequada."
    )


MODELOS = [
    # Português / interpretação
    {
        "origem": "geral", "materia": "Português e Interpretação", "tema": "interpretação textual em prova policial",
        "correta": "a alternativa correta deve respeitar o comando da questão e decorrer de informação explícita ou inferência autorizada pelo texto.",
        "erradas": [
            "a alternativa mais extensa deve prevalecer quando houver dúvida entre duas respostas parecidas.",
            "inferência textual autoriza conclusão contrária ao ponto de vista sustentado no texto-base.",
            "elementos de coesão são irrelevantes para a compreensão global em provas objetivas.",
            "expressões como 'exceto' e 'incorreta' não alteram o raciocínio exigido pela banca."
        ],
        "exp": "Interpretação exige atenção ao texto, ao comando e às inferências autorizadas."
    },
    # Informática
    {
        "origem": "geral", "materia": "Informática", "tema": "segurança da informação em ambiente institucional",
        "correta": "autenticação forte, backup, controle de acesso e prevenção contra phishing reduzem riscos à integridade e confidencialidade dos dados.",
        "erradas": [
            "backup substitui controle de acesso, pois cópias eliminam riscos de vazamento.",
            "phishing é ameaça física restrita a computadores sem internet.",
            "senhas compartilhadas aumentam eficiência sem comprometer segurança.",
            "confidencialidade impede qualquer registro de acesso aos sistemas institucionais."
        ],
        "exp": "Segurança da informação envolve confidencialidade, integridade, disponibilidade, autenticação e prevenção de golpes."
    },
    # Raciocínio lógico
    {
        "origem": "geral", "materia": "Raciocínio Lógico", "tema": "interpretação lógica de enunciados normativos",
        "correta": "expressões como 'todo', 'algum', 'nenhum' e 'somente se' alteram a validade da conclusão.",
        "erradas": [
            "a palavra 'todo' equivale sempre a 'algum' quando o assunto é jurídico.",
            "negações compostas podem ser resolvidas apenas pela intuição.",
            "a conclusão lógica independe das premissas em temas de segurança pública.",
            "condicionais não aparecem em questões de concursos policiais."
        ],
        "exp": "Raciocínio lógico exige atenção a quantificadores, condicionais e negações."
    },
    # Constitucional
    {
        "origem": "geral", "materia": "Direito Constitucional", "tema": "direitos fundamentais e segurança pública",
        "correta": "a segurança pública deve proteger a ordem pública e a incolumidade das pessoas e do patrimônio, sem afastar direitos fundamentais.",
        "erradas": [
            "a atuação policial em segurança pública afasta automaticamente a incidência de direitos fundamentais.",
            "a Constituição não relaciona segurança pública com responsabilidade estatal.",
            "direitos fundamentais impedem qualquer medida de controle, disciplina ou contenção estatal.",
            "a preservação da ordem pública autoriza atuação sem legalidade ou controle."
        ],
        "exp": "Segurança pública deve conciliar proteção social, legalidade e direitos fundamentais."
    },
    # Administrativo
    {
        "origem": "geral", "materia": "Direito Administrativo", "tema": "legalidade, poder disciplinar e atuação funcional",
        "correta": "o poder disciplinar deve respeitar legalidade, apuração, proporcionalidade, contraditório e ampla defesa quando cabíveis.",
        "erradas": [
            "o poder disciplinar permite punição definitiva sem apuração quando houver interesse público.",
            "a hierarquia administrativa elimina a necessidade de motivação dos atos punitivos.",
            "a eficiência administrativa autoriza descumprimento de normas legais.",
            "a moralidade administrativa é princípio sem relevância para servidores de segurança."
        ],
        "exp": "A atuação disciplinar deve respeitar legalidade, motivação, proporcionalidade e garantias."
    },
    # Penal
    {
        "origem": "geral", "materia": "Direito Penal", "tema": "dolo, culpa e responsabilização penal",
        "correta": "o dolo eventual exige que o agente assuma o risco de produzir o resultado, não bastando a simples previsão abstrata do perigo.",
        "erradas": [
            "dolo eventual se confunde com culpa consciente, pois em ambos o agente aceita o resultado.",
            "culpa consciente exige vontade direta de produzir o resultado.",
            "todo resultado lesivo no ambiente prisional gera responsabilidade penal objetiva.",
            "negligência sempre afasta tipicidade quando praticada por servidor público."
        ],
        "exp": "Dolo eventual exige assunção do risco; culpa consciente envolve previsão sem aceitação do resultado."
    },
    # Processo Penal
    {
        "origem": "geral", "materia": "Processo Penal", "tema": "cadeia de custódia e preservação de prova",
        "correta": "a cadeia de custódia busca preservar autenticidade, integridade e rastreabilidade dos vestígios.",
        "erradas": [
            "cadeia de custódia é dispensável quando houver confissão informal.",
            "quebra da cadeia de custódia sempre gera absolvição automática.",
            "vestígios em presídio podem ser manipulados sem registro por urgência administrativa.",
            "cadeia de custódia aplica-se somente a crimes patrimoniais."
        ],
        "exp": "A cadeia de custódia preserva a confiabilidade da prova e deve ser documentada."
    },
    # LEP
    {
        "origem": "geral", "materia": "LEP e Execução Penal", "tema": "finalidade, disciplina e direitos na execução penal",
        "correta": "a execução penal efetiva a sentença e busca proporcionar condições para integração social do condenado e do internado.",
        "erradas": [
            "a execução penal possui finalidade exclusivamente retributiva.",
            "a LEP trata apenas de cálculo de pena, sem direitos e deveres da pessoa presa.",
            "a integração social impede sanções disciplinares no cárcere.",
            "o cumprimento da pena depende apenas de ato administrativo sem controle judicial."
        ],
        "exp": "A LEP combina efetivação da sentença, disciplina e integração social."
    },
    # Direitos Humanos
    {
        "origem": "geral", "materia": "Direitos Humanos", "tema": "dignidade humana no cárcere",
        "correta": "a pessoa privada de liberdade mantém direitos fundamentais compatíveis com a execução da pena, inclusive integridade física e moral.",
        "erradas": [
            "a condenação elimina a titularidade de direitos fundamentais.",
            "a disciplina prisional autoriza tratamento degradante.",
            "direitos humanos no cárcere são recomendações sem efeito jurídico.",
            "a proteção da dignidade impede qualquer sanção disciplinar."
        ],
        "exp": "A prisão restringe a liberdade, mas não elimina dignidade e direitos compatíveis."
    },
    # Legislação Especial
    {
        "origem": "geral", "materia": "Legislação Penal Especial", "tema": "leis penais especiais e atuação policial",
        "correta": "leis penais especiais devem ser interpretadas conforme seus tipos, finalidades, limites constitucionais e consequências jurídicas.",
        "erradas": [
            "leis penais especiais afastam princípios constitucionais em contexto policial.",
            "a gravidade abstrata dispensa análise dos elementos do tipo penal.",
            "legislação especial não se relaciona com processo penal ou direitos humanos.",
            "toda lei penal especial gera regime idêntico ao da LEP."
        ],
        "exp": "Leis especiais exigem atenção a tipo penal, contexto, limites constitucionais e efeitos jurídicos."
    },
    # IDECAN
    {
        "origem": "idecan", "materia": "IDECAN - Estilo de Banca", "tema": "literalidade, exceções e alternativas parcialmente corretas",
        "correta": "a banca pode combinar literalidade legal com interpretação institucional, exigindo atenção ao comando 'correta', 'incorreta' e 'exceto'.",
        "erradas": [
            "a IDECAN cobra somente memorização de números de artigos.",
            "a palavra 'sempre' torna a alternativa automaticamente correta.",
            "alternativas parcialmente corretas devem ser marcadas quando trouxerem termo técnico verdadeiro.",
            "legislação específica não pode misturar Constituição, lei estadual e direitos humanos."
        ],
        "exp": "Bancas usam alternativas parcialmente corretas e comandos que mudam a resposta."
    },
    # Operacional
    {
        "origem": "policial", "materia": "Operacional Policial", "tema": "conduta funcional, preservação de prova e gestão de crise",
        "correta": "a atuação policial deve conciliar eficiência, legalidade, preservação da prova, respeito aos direitos fundamentais e finalidade pública.",
        "erradas": [
            "eficiência policial autoriza desprezar formalidades legais quando houver suspeita.",
            "investigação criminal e segurança penitenciária possuem atribuições idênticas.",
            "registro formal de ocorrência é dispensável quando há convicção pessoal.",
            "direitos fundamentais são incompatíveis com atividades de segurança pública."
        ],
        "exp": "Atuação policial exige técnica, legalidade, registro, proporcionalidade e respeito a direitos."
    },
]


MODELOS_CEARA = [
    {
        "origem": "ceara", "materia": "História do Ceará", "tema": "formação histórica, interiorização, secas e desigualdades regionais",
        "correta": "a formação histórica cearense envolve interiorização, pecuária, secas, migrações e organização social do território.",
        "erradas": [
            "a história do Ceará pode ser explicada exclusivamente pela mineração aurífera colonial.",
            "as secas não influenciaram migrações, políticas públicas ou economia.",
            "a interiorização ocorreu sem relação com atividades econômicas ou conflitos territoriais.",
            "Fortaleza sempre concentrou toda a dinâmica histórica, sem relevância do sertão."
        ],
        "exp": "História do Ceará envolve sertão, pecuária, secas, migrações e desigualdade territorial."
    },
    {
        "origem": "ceara", "materia": "Geografia do Ceará", "tema": "semiárido, recursos hídricos e dinâmica territorial",
        "correta": "a geografia cearense exige atenção ao semiárido, irregularidade de chuvas, gestão hídrica, urbanização e contrastes regionais.",
        "erradas": [
            "o Ceará possui clima predominantemente polar no interior.",
            "gestão hídrica é irrelevante porque há chuvas regulares todo o ano.",
            "a Caatinga não possui relação com o semiárido nordestino.",
            "a geografia do Ceará deve ser estudada sem considerar população ou urbanização."
        ],
        "exp": "Geografia cearense envolve semiárido, Caatinga, recursos hídricos, litoral, sertão e urbanização."
    },
    {
        "origem": "ceara", "materia": "Fortaleza e Região Metropolitana", "tema": "urbanização, mobilidade, desigualdade e segurança",
        "correta": "Fortaleza e sua região metropolitana concentram desafios urbanos ligados à mobilidade, desigualdade socioespacial, segurança pública e serviços.",
        "erradas": [
            "a Região Metropolitana de Fortaleza não possui relevância para segurança pública estadual.",
            "a urbanização de Fortaleza eliminou desigualdades socioespaciais.",
            "Fortaleza deve ser estudada apenas por aspectos turísticos.",
            "questões regionais nunca relacionam capital, periferia, economia urbana e segurança."
        ],
        "exp": "Fortaleza/RM envolve urbanização, desigualdade, mobilidade, turismo, economia e segurança."
    },
    {
        "origem": "ceara", "materia": "Segurança Pública no Ceará", "tema": "prevenção, investigação, sistema penitenciário e políticas públicas",
        "correta": "a segurança pública no Ceará pode ser analisada pela integração entre prevenção, investigação, policiamento, sistema penitenciário e políticas sociais.",
        "erradas": [
            "segurança pública estadual se limita ao policiamento ostensivo.",
            "prevenção, inteligência e investigação não se relacionam com políticas públicas.",
            "o sistema penitenciário é tema isolado, sem impacto na segurança pública.",
            "direitos humanos impedem atuação firme do Estado em segurança pública."
        ],
        "exp": "Segurança pública envolve integração institucional, prevenção, investigação, sistema prisional e direitos."
    },
    {
        "origem": "ceara", "materia": "SAP/CE e Sistema Penitenciário", "tema": "estrutura penitenciária, função da Polícia Penal e gestão prisional",
        "correta": "a atuação da Polícia Penal no Ceará relaciona-se à segurança dos estabelecimentos penais, preservação da ordem, disciplina e respeito à legalidade.",
        "erradas": [
            "a Polícia Penal atua apenas como força administrativa sem relação com segurança prisional.",
            "disciplina prisional autoriza medidas sem registro, controle ou proporcionalidade.",
            "sistema penitenciário não se conecta com execução penal, direitos humanos ou segurança pública.",
            "a função policial penal dispensa análise de dever funcional e responsabilidade institucional."
        ],
        "exp": "Polícia Penal envolve segurança prisional, disciplina, legalidade, dever funcional e proteção institucional."
    },
    {
        "origem": "ceara", "materia": "Atualidades do Ceará", "tema": "segurança, economia regional, vulnerabilidade social e gestão estatal",
        "correta": "atualidades do Ceará podem envolver segurança, desigualdade, políticas públicas, economia regional, vulnerabilidade social e gestão estatal.",
        "erradas": [
            "atualidades regionais não podem ser cobradas em concurso estadual de segurança.",
            "notícias locais devem ser decoradas sem relação com contexto histórico ou social.",
            "segurança pública não se relaciona com economia, urbanização ou vulnerabilidade.",
            "análise de atualidades deve ignorar dados institucionais e políticas públicas."
        ],
        "exp": "Atualidades exigem contexto: segurança, economia, políticas públicas, vulnerabilidade, território e instituições."
    },
]


MODELOS_APOSTILA = [
    {
        "origem": "apostila", "materia": "Legislação Específica PPCE", "tema": "Constituição Estadual, legislação estadual e estrutura penitenciária",
        "correta": "a legislação específica deve ser estudada de forma integrada com Constituição Estadual, organização penitenciária, dever funcional e direitos fundamentais.",
        "erradas": [
            "a legislação específica deve ser decorada apenas pelo número das leis.",
            "normas administrativas podem contrariar a Constituição em matéria penitenciária.",
            "portarias, leis e Constituição possuem a mesma hierarquia normativa.",
            "a função policial penal é incompatível com direitos humanos e controle institucional."
        ],
        "exp": "Legislação específica exige hierarquia normativa, leitura da lei, finalidade institucional e limites constitucionais."
    },
]


def gerar_banco():
    banco = []
    planos = {"facil": 20, "medio": 30, "dificil": 42, "caveira": 55}

    for grupo in [MODELOS, MODELOS_CEARA, MODELOS_APOSTILA]:
        for modelo in grupo:
            for nivel, qtd in planos.items():
                for _ in range(qtd):
                    banco.append(q(
                        modelo["origem"], nivel, modelo["materia"], modelo["tema"],
                        modelo["correta"], modelo["erradas"], modelo["exp"]
                    ))

    discursivas = [
        ("Sistema prisional", "Explique como a Polícia Penal deve conciliar segurança institucional, direitos humanos e disciplina interna em uma unidade prisional.", "A resposta deve mencionar legalidade, dignidade humana, prevenção de crises, registro de ocorrências e proporcionalidade."),
        ("Ceará e segurança pública", "Analise como desigualdade territorial, urbanização e sistema penitenciário podem impactar a segurança pública no Ceará.", "A resposta deve relacionar contexto regional, políticas públicas, urbanização, prevenção e sistema prisional."),
        ("Fortaleza/RM", "Explique por que Fortaleza e sua Região Metropolitana são relevantes para estudos de segurança pública no Ceará.", "A resposta deve abordar urbanização, mobilidade, desigualdade socioespacial, economia urbana e demanda por políticas públicas."),
        ("Legislação específica", "Explique por que a legislação específica deve ser estudada de forma integrada com Constituição, LEP e direitos humanos.", "A resposta deve destacar hierarquia normativa, finalidade pública, dever funcional e limites da atuação estatal."),
        ("Atuação policial", "Analise a importância da preservação da prova e da cadeia de custódia na atuação policial.", "A resposta deve mencionar rastreabilidade, integridade, registro, legalidade e confiabilidade da prova."),
    ]

    for i in range(50):
        materia, pergunta, resposta = discursivas[i % len(discursivas)]
        banco.append({
            "id": str(abs(hash("discursiva" + str(i) + pergunta))),
            "origem": "discursiva",
            "nivel": "caveira",
            "materia": materia,
            "pergunta": f"📄 Situação discursiva\n\n{pergunta}",
            "alternativas": [],
            "correta": "RESPOSTA ABERTA",
            "explicacao": resposta,
            "discursiva": True,
        })

    random.shuffle(banco)
    return banco


QUESTOES = gerar_banco()


def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {"usuarios": {}}
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"usuarios": {}}


def salvar_dados(dados):
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def usuario_id(update):
    return str(update.effective_user.id)


def garantir_usuario(uid):
    dados = carregar_dados()
    usuarios = dados.setdefault("usuarios", {})
    if uid not in usuarios:
        usuarios[uid] = {
            "fila": [],
            "posicao": 0,
            "atual": None,
            "modo": None,
            "acertos": 0,
            "erros": 0,
            "erradas": [],
            "favoritas": [],
            "por_materia": {},
            "por_nivel": {},
            "por_origem": {},
        }
        salvar_dados(dados)
    return usuarios[uid]


def atualizar_usuario(uid, user):
    dados = carregar_dados()
    dados.setdefault("usuarios", {})[uid] = user
    salvar_dados(dados)


def filtrar(origem=None, nivel=None, materia=None, discursiva=None):
    r = QUESTOES.copy()
    if origem:
        r = [x for x in r if x["origem"] == origem]
    if nivel:
        r = [x for x in r if x["nivel"] == nivel]
    if materia:
        r = [x for x in r if x["materia"] == materia]
    if discursiva is not None:
        r = [x for x in r if x["discursiva"] == discursiva]
    random.shuffle(r)
    return r


def sortear(lista, qtd):
    c = lista.copy()
    random.shuffle(c)
    return c[:qtd]


def menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📚 Estudos gerais", callback_data="menu_geral")],
        [InlineKeyboardButton("🧲 Central IDECAN", callback_data="menu_idecan")],
        [InlineKeyboardButton("🌎 Ceará & Fortaleza", callback_data="menu_ceara")],
        [InlineKeyboardButton("📕 Minha Apostila", callback_data="menu_apostila")],
        [InlineKeyboardButton("📝 Simulados operacionais", callback_data="menu_simulados")],
        [InlineKeyboardButton("📝 Discursivas", callback_data="discursivas")],
        [InlineKeyboardButton("🧠 Treino inteligente", callback_data="inteligente")],
        [InlineKeyboardButton("❌ Revisar erros", callback_data="erros")],
        [InlineKeyboardButton("▶️ Continuar", callback_data="continuar")],
        [InlineKeyboardButton("📊 Desempenho", callback_data="desempenho")],
        [InlineKeyboardButton("🎥 Videoaulas", callback_data="videos")],
    ])


def menu_niveis(prefixo):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Patrulha Básica", callback_data=f"{prefixo}_facil")],
        [InlineKeyboardButton("🟡 Operação Regional", callback_data=f"{prefixo}_medio")],
        [InlineKeyboardButton("🔴 Missão Tática", callback_data=f"{prefixo}_dificil")],
        [InlineKeyboardButton("⚫ OPERAÇÃO CAVEIRA", callback_data=f"{prefixo}_caveira")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def menu_ceara():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Patrulha Básica CE", callback_data="ceara_facil")],
        [InlineKeyboardButton("🟡 Operação Regional CE", callback_data="ceara_medio")],
        [InlineKeyboardButton("🔴 Missão Tática CE", callback_data="ceara_dificil")],
        [InlineKeyboardButton("⚫ Caveira Ceará", callback_data="ceara_caveira")],
        [InlineKeyboardButton("🌎 Simulado Ceará — 150Q", callback_data="sim_ceara_150")],
        [InlineKeyboardButton("🏙️ Fortaleza/RM — 100Q", callback_data="sim_fortaleza_100")],
        [InlineKeyboardButton("⚫ Caveira Ceará — 200Q", callback_data="sim_ceara_200")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def menu_apostila():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🟢 Apostila Patrulha", callback_data="ap_facil")],
        [InlineKeyboardButton("🟡 Apostila Regional", callback_data="ap_medio")],
        [InlineKeyboardButton("🔴 Apostila Tática", callback_data="ap_dificil")],
        [InlineKeyboardButton("⚫ Caveira da Apostila", callback_data="ap_caveira")],
        [InlineKeyboardButton("📝 Simulado Apostila 100Q", callback_data="sim_ap_100")],
        [InlineKeyboardButton("⚫ Simulado Apostila 200Q", callback_data="sim_ap_200")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def menu_simulados():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Treino rápido — 100Q difíceis", callback_data="sim_100")],
        [InlineKeyboardButton("📘 Simulado médio — 150Q", callback_data="sim_150")],
        [InlineKeyboardButton("🎯 Prova real — 90Q", callback_data="sim_90")],
        [InlineKeyboardButton("⚫ Caveira — 200Q", callback_data="sim_200")],
        [InlineKeyboardButton("🧲 IDECAN Caveira — 90Q", callback_data="sim_idecan_90")],
        [InlineKeyboardButton("🚔 Polícia Penal + Civil — 250Q", callback_data="sim_policial_250")],
        [InlineKeyboardButton("🌎 Ceará — 150Q", callback_data="sim_ceara_150")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def teclado_questao():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("A", callback_data="resp_A"),
            InlineKeyboardButton("B", callback_data="resp_B"),
            InlineKeyboardButton("C", callback_data="resp_C"),
            InlineKeyboardButton("D", callback_data="resp_D"),
            InlineKeyboardButton("E", callback_data="resp_E"),
        ],
        [InlineKeyboardButton("⭐ Favoritar", callback_data="favoritar")],
        [InlineKeyboardButton("⏸️ Parar", callback_data="parar")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def teclado_pos():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➡️ Próxima", callback_data="proxima")],
        [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
    ])


def iniciar(update, fila, modo):
    query = update.callback_query
    uid = usuario_id(update)
    user = garantir_usuario(uid)
    if not fila:
        query.edit_message_text("Não encontrei questões nessa opção.", reply_markup=menu())
        return
    user["fila"] = fila
    user["posicao"] = 0
    user["atual"] = None
    user["modo"] = modo
    atualizar_usuario(uid, user)
    enviar_questao(update)


def enviar_questao(update):
    query = update.callback_query
    uid = usuario_id(update)
    user = garantir_usuario(uid)
    fila = user.get("fila", [])
    pos = user.get("posicao", 0)

    if not fila:
        query.edit_message_text("Nenhum estudo ativo.", reply_markup=menu())
        return

    if pos >= len(fila):
        a = user.get("acertos", 0)
        e = user.get("erros", 0)
        pct = round((a / (a + e)) * 100, 1) if a + e else 0
        query.edit_message_text(f"✅ Estudo finalizado!\n\n✅ Acertos: {a}\n❌ Erros: {e}\n📊 Aproveitamento: {pct}%", reply_markup=menu())
        return

    questao = fila[pos]
    user["atual"] = questao
    atualizar_usuario(uid, user)

    if questao["discursiva"]:
        texto = (
            f"{cabecalho('⚫ OPERAÇÃO CAVEIRA')}\n\n"
            f"{NOME_BOT}\n\n"
            f"📝 Questão discursiva\n"
            f"📚 Matéria: {questao['materia']}\n"
            f"🧾 Missão {pos+1}/{len(fila)}\n\n"
            f"{questao['pergunta']}\n\n"
            "Pense na resposta antes de ver o modelo."
        )
        teclado = InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 Ver resposta-modelo", callback_data="ver_discursiva")],
            [InlineKeyboardButton("➡️ Próxima", callback_data="proxima")],
            [InlineKeyboardButton("🏠 Menu", callback_data="menu")],
        ])
        query.edit_message_text(texto, reply_markup=teclado)
        return

    texto = (
        f"{cabecalho('⚫ OPERAÇÃO CAVEIRA')}\n\n"
        f"{NOME_BOT}\n\n"
        f"📌 Modo: {user.get('modo')}\n"
        f"📚 Matéria: {questao['materia']}\n"
        f"🎚️ Nível: {NIVEIS.get(questao['nivel'], questao['nivel'])}\n"
        f"🧾 Questão {pos+1}/{len(fila)}\n\n"
        f"{questao['pergunta']}\n\n"
        + "\n".join(questao["alternativas"]) +
        "\n\nEscolha uma alternativa:"
    )
    query.edit_message_text(texto, reply_markup=teclado_questao())


def registrar(user, questao, acertou):
    if acertou:
        user["acertos"] += 1
    else:
        user["erros"] += 1
        if questao["id"] not in user["erradas"]:
            user["erradas"].append(questao["id"])

    for campo, chave in [("por_materia", questao["materia"]), ("por_nivel", questao["nivel"]), ("por_origem", questao["origem"])]:
        user.setdefault(campo, {})
        user[campo].setdefault(chave, {"acertos": 0, "erros": 0})
        if acertou:
            user[campo][chave]["acertos"] += 1
        else:
            user[campo][chave]["erros"] += 1


def responder(update, resposta):
    query = update.callback_query
    uid = usuario_id(update)
    user = garantir_usuario(uid)
    questao = user.get("atual")

    if not questao:
        query.edit_message_text("Nenhuma questão ativa.", reply_markup=menu())
        return

    acertou = resposta == questao["correta"]
    registrar(user, questao, acertou)
    user["posicao"] += 1
    atualizar_usuario(uid, user)

    status = "✅ Resposta confirmada." if acertou else "❌ Resposta incorreta."
    query.edit_message_text(
        f"{status}\n\n✅ Correta: {questao['correta']}\n📝 Sua resposta: {resposta}\n\n📖 Explicação:\n{questao['explicacao']}",
        reply_markup=teclado_pos()
    )


def desempenho(update):
    query = update.callback_query
    uid = usuario_id(update)
    user = garantir_usuario(uid)
    a = user.get("acertos", 0)
    e = user.get("erros", 0)
    pct = round((a / (a + e)) * 100, 1) if a + e else 0

    texto = f"{cabecalho('📊 DESEMPENHO OPERACIONAL')}\n\n✅ Acertos: {a}\n❌ Erros: {e}\n🎯 Aproveitamento: {pct}%\n\n📚 Por matéria:\n"
    if not user.get("por_materia"):
        texto += "Ainda não há dados."
    else:
        for mat, d in user["por_materia"].items():
            t = d["acertos"] + d["erros"]
            p = round((d["acertos"] / t) * 100, 1) if t else 0
            texto += f"• {mat}: {d['acertos']}✅ / {d['erros']}❌ ({p}%)\n"

    query.edit_message_text(texto, reply_markup=menu())


def start(update: Update, context: CallbackContext):
    garantir_usuario(usuario_id(update))
    total = len(QUESTOES)
    texto = (
        f"{cabecalho('🚨 TREINAMENTO OPERACIONAL')}\n\n"
        f"{NOME_BOT}\n\n"
        "🚨 Sistema de treinamento operacional iniciado.\n\n"
        "📚 Banco tático pesado carregado.\n"
        "⚫ Nível Caveira desbloqueado.\n"
        "🌎 Ceará & Fortaleza ativado.\n"
        "🧠 Análise inteligente ativa.\n\n"
        "Treine até a aprovação.\n\n"
        f"📌 Questões carregadas: {total}\n\n"
        "Escolha uma opção:"
    )
    update.message.reply_text(texto, reply_markup=menu())


def callbacks(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    uid = usuario_id(update)
    garantir_usuario(uid)
    data = query.data

    if data == "menu":
        query.edit_message_text(f"{cabecalho('🚔 TESTE PENAL CE')}\n\nMenu principal:", reply_markup=menu())

    elif data == "menu_geral":
        query.edit_message_text(f"{cabecalho('📚 ESTUDOS GERAIS')}\n\nEscolha o nível operacional:", reply_markup=menu_niveis("geral"))

    elif data == "menu_idecan":
        query.edit_message_text(f"{cabecalho('🧲 CENTRAL IDECAN')}\n\nTreinamento estilo banca:", reply_markup=menu_niveis("idecan"))

    elif data == "menu_ceara":
        query.edit_message_text(f"{cabecalho('🌎 CEARÁ & FORTALEZA')}\n\nTreinamento regional de alta dificuldade:", reply_markup=menu_ceara())

    elif data == "menu_apostila":
        query.edit_message_text(f"{cabecalho('📕 ÁREA DA APOSTILA')}\n\nTreinamento baseado na sua legislação:", reply_markup=menu_apostila())

    elif data == "menu_simulados":
        query.edit_message_text(f"{cabecalho('📝 SIMULADOS OPERACIONAIS')}\n\nEscolha o modo de treinamento:", reply_markup=menu_simulados())

    elif data == "videos":
        botoes = [[InlineKeyboardButton(nome, url=link)] for nome, link in VIDEOAULAS.items()]
        botoes.append([InlineKeyboardButton("🏠 Menu", callback_data="menu")])
        query.edit_message_text(f"{cabecalho('🎥 CENTRAL DE VIDEOAULAS')}\n\nEscolha uma aula:", reply_markup=InlineKeyboardMarkup(botoes))

    elif data.startswith("geral_"):
        nivel = data.replace("geral_", "")
        iniciar(update, filtrar(nivel=nivel, discursiva=False), f"Estudo geral {NIVEIS.get(nivel, nivel)}")

    elif data.startswith("idecan_"):
        nivel = data.replace("idecan_", "")
        iniciar(update, filtrar(origem="idecan", nivel=nivel, discursiva=False), f"IDECAN {NIVEIS.get(nivel, nivel)}")

    elif data.startswith("ceara_"):
        nivel = data.replace("ceara_", "")
        iniciar(update, filtrar(origem="ceara", nivel=nivel, discursiva=False), f"Ceará/Fortaleza {NIVEIS.get(nivel, nivel)}")

    elif data.startswith("ap_"):
        nivel = data.replace("ap_", "")
        iniciar(update, filtrar(origem="apostila", nivel=nivel, discursiva=False), f"Apostila {NIVEIS.get(nivel, nivel)}")

    elif data == "sim_100":
        iniciar(update, sortear(filtrar(nivel="dificil", discursiva=False), 100), "⚡ Treino rápido — 100Q difíceis")

    elif data == "sim_150":
        iniciar(update, sortear(filtrar(discursiva=False), 150), "📘 Simulado médio — 150Q")

    elif data == "sim_90":
        base = filtrar(origem="idecan", discursiva=False) + filtrar(origem="geral", nivel="dificil", discursiva=False)
        iniciar(update, sortear(base, 90), "🎯 Prova real — 90Q")

    elif data == "sim_200":
        iniciar(update, sortear(filtrar(nivel="caveira", discursiva=False), 200), "⚫ Caveira — 200Q")

    elif data == "sim_idecan_90":
        iniciar(update, sortear(filtrar(origem="idecan", nivel="caveira", discursiva=False), 90), "🧲 IDECAN Caveira — 90Q")

    elif data == "sim_policial_250":
        base = [x for x in QUESTOES if x["origem"] in ["geral", "policial"] and not x["discursiva"]]
        iniciar(update, sortear(base, 250), "🚔 Polícia Penal + Civil — 250Q")

    elif data == "sim_ceara_150":
        iniciar(update, sortear(filtrar(origem="ceara", discursiva=False), 150), "🌎 Simulado Ceará — 150Q")

    elif data == "sim_fortaleza_100":
        base = [x for x in QUESTOES if x["materia"] == "Fortaleza e Região Metropolitana" and not x["discursiva"]]
        iniciar(update, sortear(base, 100), "🏙️ Fortaleza/RM — 100Q")

    elif data == "sim_ceara_200":
        iniciar(update, sortear(filtrar(origem="ceara", nivel="caveira", discursiva=False), 200), "⚫ Caveira Ceará — 200Q")

    elif data == "sim_ap_100":
        iniciar(update, sortear(filtrar(origem="apostila", discursiva=False), 100), "📕 Apostila — 100Q")

    elif data == "sim_ap_200":
        iniciar(update, sortear(filtrar(origem="apostila", nivel="caveira", discursiva=False), 200), "📕 Apostila Caveira — 200Q")

    elif data == "discursivas":
        iniciar(update, filtrar(origem="discursiva", discursiva=True), "📝 Discursivas — 50 questões abertas")

    elif data == "ver_discursiva":
        user = garantir_usuario(uid)
        atual = user.get("atual")
        if atual:
            user["posicao"] += 1
            atualizar_usuario(uid, user)
            query.edit_message_text(f"📖 Resposta-modelo:\n\n{atual['explicacao']}", reply_markup=teclado_pos())

    elif data == "inteligente":
        user = garantir_usuario(uid)
        ids = set(user.get("erradas", []))
        fila = [x for x in QUESTOES if x["id"] in ids and not x["discursiva"]]
        if len(fila) < 80:
            fila += sortear(filtrar(nivel="caveira", discursiva=False), 80 - len(fila))
        iniciar(update, fila, "🧠 Treino inteligente")

    elif data == "erros":
        user = garantir_usuario(uid)
        ids = set(user.get("erradas", []))
        fila = [x for x in QUESTOES if x["id"] in ids]
        if not fila:
            query.edit_message_text("✅ Você ainda não tem erros para revisar.", reply_markup=menu())
        else:
            iniciar(update, fila, "❌ Revisão de erros")

    elif data == "continuar":
        enviar_questao(update)

    elif data == "desempenho":
        desempenho(update)

    elif data == "proxima":
        enviar_questao(update)

    elif data.startswith("resp_"):
        responder(update, data.replace("resp_", ""))

    elif data == "favoritar":
        user = garantir_usuario(uid)
        atual = user.get("atual")
        if atual and atual["id"] not in user["favoritas"]:
            user["favoritas"].append(atual["id"])
            atualizar_usuario(uid, user)
        query.answer("Favoritada ⭐")

    elif data == "parar":
        user = garantir_usuario(uid)
        query.edit_message_text(f"⏸️ Estudo salvo.\n\nVocê parou na questão {user.get('posicao', 0) + 1} de {len(user.get('fila', []))}.", reply_markup=menu())


def main():
    if BOT_TOKEN == "COLE_AQUI_O_BOT_TOKEN_DO_BOT_TESTE":
        print("⚠️ Coloque o BOT_TOKEN do bot de teste antes de rodar.")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(callbacks))

    print("🚔 TESTE PENAL CE ONLINE")
    print(f"📚 Questões carregadas: {len(QUESTOES)}")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
