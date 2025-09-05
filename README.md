MOPAC Tools - Analisador de Saída e Visualizador 3D
Este repositório contém um conjunto de ferramentas para analisar arquivos de saída do pacote de química quântica MOPAC. O objetivo é automatizar a extração de dados e facilitar a visualização de geometrias moleculares e cargas atômicas, otimizando o fluxo de trabalho de pesquisadoras e professoras da área.

O projeto está disponível em duas versões, cada uma com um propósito específico.

Versão Web (HTML)
Uma aplicação web interativa e de página única que roda diretamente no navegador. É a solução ideal para análises rápidas, apresentações ou para usuários que preferem uma interface gráfica, sem a necessidade de instalar qualquer software.

Funcionalidades
Interface Gráfica Intuitiva: Faça o upload do seu arquivo .out do MOPAC com um simples clique.

Visualização Instantânea: A molécula 3D e as cargas de Mulliken de cada átomo são renderizadas e exibidas imediatamente na própria página.

Portabilidade Total: Por ser um arquivo HTML único, funciona em qualquer sistema operacional (Windows, macOS, Linux) que possua um navegador de internet moderno.

Sem Dependências: Não requer instalação de Python, bibliotecas ou qualquer outra ferramenta.

Como Usar
A utilização é extremamente simples e direta:

Baixe o arquivo: Faça o download do arquivo mopac_parser.html.

Abra no Navegador:

No Windows 11: Dê um duplo-clique no arquivo. Ele será aberto automaticamente no seu navegador padrão (Edge, Chrome, Firefox, etc.).

No Linux: Clique com o botão direito no arquivo e selecione "Abrir com" para escolher seu navegador de preferência.

Carregue seu arquivo: Na página que se abriu, clique no botão "Escolher arquivo" e selecione o arquivo .out que deseja analisar.

Analise o resultado: A molécula será renderizada em 3D na tela, com os respectivos valores das cargas de Mulliken visíveis como rótulos em cada átomo.

Versão Original (Python Script)
Um script em Python para ser executado localmente via linha de comando. Esta versão é ideal para integrar em rotinas de análise de dados, processamento em lote ou para usuários que preferem trabalhar no ambiente de terminal.

Funcionalidades
Extração de Dados: Captura as coordenadas da geometria final (otimizada) e as cargas de Mulliken do arquivo de saída.

Geração de Arquivos Padrão: Cria um arquivo .xyz (molecula_final.xyz), formato universalmente compatível com softwares de visualização molecular (VMD, Avogadro, Chimera, etc.).

Geração de Visualizador HTML: Cria um arquivo .html (visualizacao_molecula.html) autocontido para visualização 3D da molécula e suas cargas.

Como Executar
Pré-requisitos:

Ter o Python 3 instalado em seu sistema. Para verificar, abra o terminal e digite python --version ou python3 --version.

Instruções para Linux (via Terminal):

Abra o terminal.

Navegue até a pasta onde o script mopac_parser.py e seu arquivo .out estão localizados, usando o comando cd. Exemplo: cd ~/Documentos/meu_projeto

Execute o script com o comando:

python3 mopac_parser.py

Após a execução, os arquivos molecula_final.xyz e visualizacao_molecula.html serão criados na mesma pasta.

Instruções para Windows 11 (via PowerShell ou Prompt de Comando):

Abra o PowerShell ou o Prompt de Comando (você pode encontrá-los no menu Iniciar).

Navegue até a pasta do projeto usando o comando cd. Exemplo: cd C:\Users\SeuUsuario\Documents\meu_projeto

Execute o script com um dos seguintes comandos:

python mopac_parser.py
# ou, caso o comando acima não funcione:
py mopac_parser.py

Os arquivos de saída, molecula_final.xyz e visualizacao_molecula.html, aparecerão na pasta.
