MOPAC Tools - Analisador de Saída e Visualizador 3D
Este repositório contém um conjunto de ferramentas em Python para analisar arquivos de saída do pacote de química quântica MOPAC.

Ferramentas Incluídas
mopac_parser.py
Este script Python analisa um arquivo de saída (.out) do MOPAC para extrair informações importantes e gerar arquivos úteis para análise e visualização.

Funcionalidades:

Extração de Geometria: Localiza e extrai as coordenadas atômicas da geometria final mais estável do cálculo.

Extração de Cargas de Mulliken: Localiza e extrai as cargas de Mulliken calculadas para cada átomo.

Geração de Arquivo .xyz: Cria um arquivo molecula_final.xyz com as coordenadas da geometria otimizada, compatível com a maioria dos softwares de visualização molecular (VMD, Avogadro, etc.).

Geração de Visualizador 3D: Cria um arquivo visualizacao_molecula.html que pode ser aberto em qualquer navegador de internet para uma visualização 3D interativa da molécula, com rótulos indicando as cargas de Mulliken em cada átomo.

Como Usar
Pré-requisitos:

Ter o Python 3 instalado.

Nenhuma biblioteca externa é necessária.

Execução:

Coloque o script mopac_parser.py na mesma pasta que o seu arquivo de saída do MOPAC (ex: 3FAC.out).

Se o nome do seu arquivo de saída não for 3FAC.out, edite a última seção do script mopac_parser.py, alterando a variável mopac_file.

Abra um terminal ou prompt de comando na pasta e execute o script:

python mopac_parser.py

Após a execução, os arquivos molecula_final.xyz e visualizacao_molecula.html serão criados na mesma pasta.

