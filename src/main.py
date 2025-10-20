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
        for x in range(padding_x, altura_img - padding_x):

            # Extrai vizinhança do mesmo tamanho do EE
            vizinhanca = imagem_binaria[
                y - padding_y : y + padding_y + 1, x - padding_x : x + padding_x + 1
            ]

            # Lógica da erosao
            if np.all(vizinhanca[ee == 1]):
                imagem_erodida[x, y] = 1

    print("Erosao concluída.")
    return imagem_erodida


def salvar_imagem(dados_imagem_np, caminho_saida):

    # Converte de 0 e 1 para 0 e 256 para visualizacao
    imagem_para_salvar = (dados_imagem_np * 256).astype(np.uint8)
    imagem = Image.fromarray(imagem_para_salvar)
    imagem.save(caminho_saida)

    print(f"Imagem salva em {caminho_saida}")


if __name__ == "__main__":

    caminho_input = "../imagens/input/imagem1.jpeg"
    caminho_output_erosao = "../imagens/output/imagem1_erodida.jpeg"

    # Define elemento estruturante

    EE_cruz = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]

    # Carrega e binariza imagem
    imagem_original_binaria = carregar_e_binarizar(caminho_input, limite_threshold=127)

    if imagem_original_binaria is not None:

        # Aplicar erosao
        imagem_final_erodida = erodir_imagem(imagem_original_binaria, EE_cruz)

        # Salvar resultado
        salvar_imagem(imagem_final_erodida, caminho_output_erosao)
