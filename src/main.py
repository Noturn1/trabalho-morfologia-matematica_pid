from PIL import Image


def imagem_binaria(caminho_imagem, limite_threshold):

    try:
        imagem = Image.open(caminho_imagem)

        imagem_grey = imagem.convert("L")

        # Aplica o Threshold
        imagem_thresh = imagem_grey.point(lambda p: 255 if p > limite_threshold else 0)

        # Converte para grayscale para realizar o Thresholding
        imagem_binaria = imagem_thresh.convert("1")
        imagem_binaria.save("../imagens/output/imagem1_out.jpeg")
        altura, largura = imagem_binaria.size[0], imagem_binaria.size[1]
        print(f"Altura: {altura}")
        print(f"Largura: {largura}")

        return imagem_binaria

    except FileNotFoundError:
        print("Erro: Arquivo de imagem não encontrado...")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# def erodir_imagem(imagem_binaria, EE):

imagem_binaria("../imagens/input/imagem1.jpeg", 100)

EE = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
