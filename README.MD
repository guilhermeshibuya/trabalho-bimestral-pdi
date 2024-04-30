# Projeto Bimestral - Processamento de Imagens e Reconhecimento de Padrões

O seguinte projeto foi desenvolvido como requisito parcial da disciplina de Processamento de Imagens e Reconhecimento de Padrões. O objetivo era desenvolver uma aplicação capaz de aplicar diferentes tipos de processamento em imagens.

# Tecnologias utilizadas

- Python;
- Pillow;
- Numpy;
- custom tkinter;
- tkinter.

# Funcionalidades

- **Conversão de cores:** é possível converter uma imagem para os seguintes espaços de cores: RGB, Grayscale, HSV, XYZ, Luv, Lab, YCrCb;
- **Filtros:** os seguintes filtros estão disponíveis: média, gaussiano e bilateral;
- **Detector de bordas:** foram implementados o Sobel, Laplace e Canny
- **Limiarização:** pode-se aplicar Threshold binário, binário invertido, truncated e otsu;
- **Operações morfológicas:** estão disponíveis dois tipos: erosão e diltação;
- **Contraste e brilho:** é possível ajustar o contraste e brilho da imagem.

  Além disso, a aplicação conta com um histórico, com todas as modificações feitas. Ao salvar a imagem modificado, no mesmo diretório é salvo um arquivo txt contendo o histórico de modificações e os parâmetros utilzizados.
  Também conta com a opção de `desfazer` uma ação ou de `refazer` uma ação, que podem ser acionadas pelos seus botões ou pelos seus atalhos, `CTRL + Z` e `CTRL + Y`, respectivamente.

# Como utilizar

1. Clone o repositório: `git clone https://github.com/guilhermeshibuya/trabalho-bimestral-pdi`

2. Instale as dependências utilizadas:
   `pip install opencv-python tkinter pillow customtkinter CTkListbox CTkToolTip CTkMessagebox numpy`

- opencv-python;
- pillow;
- numpy;
- custom tkinter;
- tkinter;
- CTkListbox;
- CTkToolTip;
- CTkMessagebox;

3. Execute o seguinte comando na raiz do projeto:

- Windows: `python main.py`
- Linux: `python3 main.py`

# Exemplo

![Alt "interface da aplicação e exemplo de uso"](./imgs/ex.png)
