def descompactar_arquivo(input_path, output_path):
    with open(input_path, 'rb') as f:
        num_simbolos = f.read(1)[0]
        tabela_huffman = {}
        for _ in range(num_simbolos):
            simbolo = chr(f.read(1)[0])
            tamanho_codigo = f.read(1)[0]
            codigo_binario = f.read((tamanho_codigo + 7) // 8)
            codigo_binario = bin(int.from_bytes(codigo_binario, byteorder='big'))[2:]
            codigo_binario = codigo_binario.zfill(tamanho_codigo)
            tabela_huffman[codigo_binario] = simbolo
        
        codigo_compactado = ''
        while True:
            byte = f.read(1)
            if not byte:
                break
            codigo_compactado += bin(ord(byte))[2:].zfill(8)
    
    codigo_decodificado = ''
    resultado = []
    for bit in codigo_compactado:
        codigo_decodificado += bit
        if codigo_decodificado in tabela_huffman:
            resultado.append(tabela_huffman[codigo_decodificado])
            codigo_decodificado = ''
    
    with open(output_path, 'w', encoding='ISO-8859-1') as f:
        f.write(''.join(resultado))

# Execução da descompactação
descompactar_arquivo('teste.uzip', 'teste_desc.txt')