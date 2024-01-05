import requests
from bs4 import BeautifulSoup
import json
from unidecode import unidecode
import inflection


def limpar_texto(texto):
    # Limpa o texto removendo \n, espaços extras e caracteres especiais
    return " ".join(texto.split()).replace("------------", "")


def formatar_rotulo(rotulo):
    # Formata o rótulo para snake_case, sem acentos e substituindo ç por c
    return inflection.underscore(unidecode(rotulo)).replace("c_", "c")


def coletar_dados_intel():
    url = "https://ark.intel.com/content/www/br/pt/ark/products/series/122593/10th-gen-intel-core-processors.html"

    # Realiza a requisição HTTP
    response = requests.get(url)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        # Parseia o conteúdo HTML da página
        soup = BeautifulSoup(response.text, "html.parser")

        # Encontrando informações relevantes
        processadores = []
        for td_ark in soup.find_all("td", class_="ark-product-name"):
            div_processador = td_ark.find("div", class_="add-compare-wrap")
            if div_processador:
                a_element = div_processador.find("a")
                processador_nome = a_element.text.strip()
                processador_link = "https://ark.intel.com" + a_element["href"]

                # Realiza uma nova requisição para a página do processador
                response_processador = requests.get(processador_link)
                if response_processador.status_code == 200:
                    soup_processador = BeautifulSoup(
                        response_processador.text, "html.parser"
                    )

                    # Encontrar e extrair informações de todas as ul.specs-list
                    uls_specs_list = soup_processador.find_all(
                        "ul", class_="specs-list"
                    )
                    dados_formatados = {}
                    for ul_specs_list in uls_specs_list:
                        for li in ul_specs_list.find_all("li"):
                            span_label = li.find("span", class_="label")
                            span_value = li.find("span", class_="value")
                            if span_label and span_value:
                                # Corrige títulos específicos com espaços e caracteres especiais
                                chave = span_label.text.strip().lower()
                                chave = (
                                    chave.replace("intel® ", "")
                                    .replace("(", "")
                                    .replace(")", "")
                                    .replace(" ", "_")
                                )
                                chave = unidecode(chave)
                                valor = span_value.text.strip()
                                if "‡" in valor:
                                    valor = valor.replace(
                                        "‡", ""
                                    )  # Remover o caractere ‡
                                dados_formatados[chave] = valor

                    # Adiciona as informações coletadas à lista de processadores
                    processadores.append({"nome": processador_nome, **dados_formatados})
                else:
                    print(
                        f"Falha na requisição para {processador_link}. Código de status: {response_processador.status_code}"
                    )
            else:
                print(
                    f"Elemento 'div.add-compare-wrap' não encontrado na linha {td_ark}"
                )

        # Salvar os dados em um arquivo JSON
        with open("dados_processadores_intel.json", "w", encoding="utf-8") as arquivo:
            json.dump(processadores, arquivo, ensure_ascii=False, indent=2)
    else:
        print(f"Falha na requisição. Código de status: {response.status_code}")


if __name__ == "__main__":
    coletar_dados_intel()
