# -*- coding: utf-8 -*-
"""
Este script analisa um arquivo de saída do MOPAC para extrair a geometria final
e as cargas de Mulliken, gerando um arquivo .xyz e um arquivo HTML para
visualização 3D com 3Dmol.js.
"""
import re

def parse_mopac_output(filepath):
    """
    Analisa o arquivo de saída do MOPAC para extrair coordenadas e cargas de Mulliken.

    Args:
        filepath (str): O caminho para o arquivo de saída do MOPAC.

    Returns:
        tuple: Uma tupla contendo uma lista de átomos e uma lista de cargas,
               ou (None, None) se os dados não puderem ser encontrados.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo '{filepath}' não foi encontrado.")
        return None, None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None, None

    # Encontra a seção da geometria final otimizada
    geom_block_match = re.search(
        r"ATOM\s+CHEMICAL\s+X\s+Y\s+Z\s*\(ANGSTROMS\)\s*\(ANGSTROMS\)\s*\(ANGSTROMS\)"
        r"\s*\n\s*\n(.*?)\n\n\s*CARTESIAN COORDINATES",
        content, re.S
    )

    if not geom_block_match:
        # Tenta um padrão alternativo se o primeiro falhar
        geom_block_match = re.search(
            r"FINAL HEAT OF FORMATION =.*?\n\n(.*?)\n\n\s*CARTESIAN COORDINATES",
            content, re.S
        )

    # Segunda tentativa para encontrar o bloco de geometria, mais perto do final
    if not geom_block_match:
         geom_block_match = re.search(
            r"ATOM\s+CHEMICAL\s+X\s+Y\s+Z\s*\n\s*NUMBER\s+SYMBOL\s+\(ANGSTROMS\)\s+\(ANGSTROMS\)\s+\(ANGSTROMS\)\s*\n\s*\n(.*?)\n\n\s*CARTESIAN COORDINATES",
            content, re.S
        )

    # Última tentativa para encontrar a geometria final
    if not geom_block_match:
        sections = content.split("FINAL HEAT OF FORMATION")
        if len(sections) > 1:
            final_section = sections[-1]
            geom_block_match = re.search(
                r"ATOM\s+CHEMICAL\s+X\s+Y\s+Z\s*\n\s*NUMBER\s+SYMBOL\s+\(ANGSTROMS\)\s+\(ANGSTROMS\)\s+\(ANGSTROMS\)\s*\n\s*\n(.*?)\n\n\s* CARTESIAN COORDINATES",
                final_section, re.S
            )

    # Encontra a seção de cargas de Mulliken
    charge_block_match = re.search(
        r"MULLIKEN POPULATIONS AND CHARGES\s*\n\s*\n"
        r"\s*NO\.\s+ATOM\s+POPULATION\s+CHARGE\s*\n(.*?)\n\s*\*",
        content, re.S
    )

    if not geom_block_match or not charge_block_match:
        print("Não foi possível encontrar a geometria final ou as cargas de Mulliken no arquivo.")
        return None, None

    atoms = []
    geom_lines = geom_block_match.group(1).strip().split('\n')
    for line in geom_lines:
        parts = line.split()
        if len(parts) >= 8:
            try:
                atom_symbol = parts[1]
                x = float(parts[2])
                y = float(parts[4])
                z = float(parts[6])
                atoms.append({'symbol': atom_symbol, 'x': x, 'y': y, 'z': z})
            except (ValueError, IndexError):
                continue # Pula linhas que não podem ser analisadas

    charges = []
    charge_lines = charge_block_match.group(1).strip().split('\n')
    for line in charge_lines:
        parts = line.split()
        if len(parts) >= 4:
            try:
                charges.append(float(parts[3]))
            except ValueError:
                continue # Pula linhas que não podem ser analisadas

    if len(atoms) == len(charges):
        for i, atom in enumerate(atoms):
            atom['charge'] = charges[i]
    else:
        print("Aviso: O número de átomos e de cargas não coincide. As cargas não serão atribuídas.")

    return atoms

def create_xyz_file(atoms, output_filename="molecule.xyz"):
    """
    Cria um arquivo .xyz a partir dos dados dos átomos.

    Args:
        atoms (list): Lista de dicionários de átomos.
        output_filename (str): Nome do arquivo .xyz de saída.
    """
    if not atoms:
        return
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(f"{len(atoms)}\n")
        f.write("Molecule generated from MOPAC output\n")
        for atom in atoms:
            f.write(f"{atom['symbol']} {atom['x']:.8f} {atom['y']:.8f} {atom['z']:.8f}\n")
    print(f"Arquivo '{output_filename}' criado com sucesso.")

def create_3dmol_html(atoms, output_filename="molecule.html"):
    """
    Cria um arquivo HTML para visualização 3D da molécula com 3Dmol.js.

    Args:
        atoms (list): Lista de dicionários de átomos, que podem incluir cargas.
        output_filename (str): Nome do arquivo HTML de saída.
    """
    if not atoms:
        return

    xyz_data_for_html = f"{len(atoms)}\\nGenerated from MOPAC\\n"
    for atom in atoms:
        xyz_data_for_html += f"{atom['symbol']} {atom['x']:.8f} {atom['y']:.8f} {atom['z']:.8f}\\n"

    labels_js = ""
    if all('charge' in atom for atom in atoms):
        labels_js = """
        viewer.addLabels(
            (atom) => `Mulliken: ${atom.charge.toFixed(4)}`,
            {
                fontColor: 'black',
                fontSize: 12,
                backgroundColor: 'lightgray',
                backgroundOpacity: 0.7,
                showBackground: true,
                inFront: true
            },
            { resi: 1 } // Seleciona todos os átomos no primeiro resíduo
        );
        """
        # Adiciona a carga como um atributo 'charge' para 3Dmol usar
        for i, atom in enumerate(atoms):
            labels_js = labels_js.replace(
                f"{{ resi: 1 }}",
                f"{{ atom: {i}, charge: {atom['charge']:.4f} }}, {i}"
            )

    html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Visualizador de Molécula 3D</title>
    <style>
        body {{ font-family: sans-serif; margin: 0; }}
        .viewer_container {{
            width: 100vw;
            height: 100vh;
            position: relative;
        }}
    </style>
</head>
<body>
    <div id="container" class="viewer_container"></div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.1.0/3Dmol-min.js"></script>

    <script>
        (function() {{
            let element = document.getElementById('container');
            let config = {{ backgroundColor: '0xeeeeee' }};
            let viewer = $3Dmol.createViewer(element, config);

            let xyz_data = `{xyz_data_for_html}`;

            viewer.addModel(xyz_data, "xyz");
            viewer.setStyle({{}}, {{stick: {{}}, sphere: {{scale:0.3}}}});

            // Adiciona rótulos com as cargas de Mulliken
            const atoms = viewer.getModel().selectedAtoms();
            const charges = [{', '.join(str(atom.get('charge', 'N/A')) for atom in atoms)}];

            for (let i = 0; i < atoms.length; i++) {{
                if (i < charges.length && typeof charges[i] === 'number') {{
                    viewer.addLabel(`Carga: ${{charges[i].toFixed(4)}}`, {{
                        position: atoms[i],
                        inFront: true,
                        fontSize: 12,
                        fontColor: 'black',
                        backgroundColor: 'lightgray',
                        backgroundOpacity: 0.7
                    }});
                }}
            }}

            viewer.zoomTo();
            viewer.render();
        }})();
    </script>
</body>
</html>
"""
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Arquivo HTML '{output_filename}' criado com sucesso.")
    print(f"Abra '{output_filename}' em seu navegador para ver a molécula.")


if __name__ == "__main__":
    # Substitua '3FAC.out' pelo nome do seu arquivo de saída do MOPAC
    mopac_file = '3FAC.out'
    parsed_atoms = parse_mopac_output(mopac_file)

    if parsed_atoms:
        create_xyz_file(parsed_atoms, 'molecula_final.xyz')
        create_3dmol_html(parsed_atoms, 'visualizacao_molecula.html')

