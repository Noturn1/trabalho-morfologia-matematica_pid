import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def carregar_e_binarizar(caminho_imagem, limite_threshold):

    try:
        imagem = Image.open(caminho_imagem)

        # Converte para grayscale
        imagem_grey = imagem.convert("L")

        # Transforma em array Numpy
        dados_imagem = np.array(imagem_grey)

        # Aplica Threshold -> (acima limite=1), (abaixo limite=0)
        imagem_binaria_np = (dados_imagem > limite_threshold).astype(np.uint8)

        print(f"Imagem carregada com sucesso. Dimensões: {imagem_binaria_np.shape}")

        return imagem_binaria_np

    except FileNotFoundError:
        print("Erro: Arquivo de imagem não encontrado...")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


def erodir_imagem(imagem_binaria, elemento_estruturante):

    # Converte elemento estruturante em array Numpy e pega suas dimensoes
    ee = np.array(elemento_estruturante, dtype=np.uint8)
    altura_ee, largura_ee = ee.shape

    # Dimensoes da imagem de entrada
    altura_img, largura_img = imagem_binaria.shape

    # Calcula padding necessário para evitar erros aplicando EE nas bordas
    padding_y = altura_ee // 2
    padding_x = largura_ee // 2

    # Cria imagem de saída (inicialmente preenchida com 0)
    imagem_erodida = np.zeros_like(imagem_binaria)

    for y in range(padding_y, altura_img - padding_y):
        for x in range(padding_x, largura_img - padding_x):

            # Extrai vizinhança do mesmo tamanho do EE
            vizinhanca = imagem_binaria[
                y - padding_y : y + padding_y + 1, x - padding_x : x + padding_x + 1
            ]

            if np.all(vizinhanca[ee == 1]):
                imagem_erodida[y, x] = 1

    print("Erosao concluída.")
    return imagem_erodida


def dilatar_imagem(imagem_binaria, elemento_estruturante):

    # Converte elemento estruturante em array Numpy e pega suas dimensoes
    ee = np.array(elemento_estruturante, dtype=np.uint8)
    altura_ee, largura_ee = ee.shape

    # Dimensoes da imagem de entrada
    altura_img, largura_img = imagem_binaria.shape

    # Calcula padding necessário para evitar erros aplicando EE nas bordas
    padding_y = altura_ee // 2
    padding_x = largura_ee // 2

    # Cria imagem de saída (inicialmente preenchida com 0)
    imagem_dilatada = np.zeros_like(imagem_binaria)

    for y in range(padding_y, altura_img - padding_y):
        for x in range(padding_x, largura_img - padding_x):

            # Extrai vizinhança do mesmo tamanho do EE
            vizinhanca = imagem_binaria[
                y - padding_y : y + padding_y + 1, x - padding_x : x + padding_x + 1
            ]

            if np.any(vizinhanca[ee == 1]):
                imagem_dilatada[y, x] = 1

    print("Dilatação concluída.")
    return imagem_dilatada


def abrir_imagem(imagem_binaria, ee_selecionado):

    imagem_abertura = np.zeros_like(imagem_binaria)

    # Primeiro passo (Erodir imagem)
    imagem_abertura = erodir_imagem(imagem_binaria, ee_selecionado)

    # Segundo passo (dilatar imagem)
    imagem_abertura = dilatar_imagem(imagem_abertura, ee_selecionado)

    return imagem_abertura


def fechar_imagem(imagem_binaria, ee_selecionado):

    imagem_fechamento = np.zeros_like(imagem_binaria)

    # Primeiro passo (Erodir imagem)
    imagem_fechamento = erodir_imagem(imagem_binaria, ee_selecionado)

    # Segundo passo (dilatar imagem)
    imagem_fechamento = dilatar_imagem(imagem_fechamento, ee_selecionado)

    return imagem_fechamento


def salvar_imagem(dados_imagem_np, caminho_saida):

    # Converte de 0 e 1 para 0 e 256 para visualizacao
    imagem_para_salvar = (dados_imagem_np * 255).astype(np.uint8)
    imagem = Image.fromarray(imagem_para_salvar)
    imagem.save(caminho_saida)

    print(f"Imagem salva em {caminho_saida}")


def main():

    # Define os Elementos Estruturantes (EE) disponíveis
    ELEMENTOS_ESTRUTURANTES = {
        "cruz": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8),
        "quadrado": np.ones((3, 3), dtype=np.uint8),
        "quadrado5x5": np.ones((5, 5), dtype=np.uint8),
    }

    # Define as operações disponíveis
    OPERACOES = {
        "erosao": erodir_imagem,
        "dilatacao": dilatar_imagem,
        "abertura": abrir_imagem,
        "fechamento": fechar_imagem,
    }

    # Configura para ler os argumentos do terminal
    parser = argparse.ArgumentParser(
        description="Script para aplicar operações morfológicas básicas em imagens.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-i", "--input", type=Path, required=True, help="Caminho da imagem de entrada."
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Caminho para salvar a imagem processada.",
    )

    parser.add_argument(
        "-op",
        "--operation",
        type=str,
        required=True,
        choices=OPERACOES.keys(),
        help="Operação morfológica a ser aplicada.",
    )

    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=128,
        help="Valor de threshold para binarização (0-255).",
    )

    parser.add_argument(
        "-ee",
        "--element",
        type=str,
        default="quadrado",
        choices=ELEMENTOS_ESTRUTURANTES.keys(),
        help="Elemento estruturante a ser usado.",
    )

    args = parser.parse_args()

    # --- Execução do Pipeline ---
    print(f"--- Iniciando Processo ---")
    print(f"  Operação: {args.operation}")
    print(f"  Elemento Estruturante: {args.element}")
    print(f"  Threshold: {args.threshold}")

    # 1. Seleciona as funções e EEs com base nos argumentos
    funcao_operacao = OPERACOES[args.operation]
    ee_selecionado = ELEMENTOS_ESTRUTURANTES[args.element]

    # 2. Carrega e binariza a imagem
    imagem_original = carregar_e_binarizar(args.input, args.threshold)

    if imagem_original is not None:

        # 3. Processa a imagem
        imagem_processada = funcao_operacao(imagem_original, ee_selecionado)

        # 4. Salva o resultado
        salvar_imagem(imagem_processada, args.output)
        print("--- Processo Concluído ---")


if __name__ == "__main__":
    main()
