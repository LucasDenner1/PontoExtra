# Grupo: Lucas Denner Soares da Rocha, Bernardo josé da Silveira Vieira, Antonio jailson da Silva Segundo, e Samuel Vitor de Oliveira Galdino


from collections import Counter
import heapq
import os

def construir_trie(freq):
    heap = [[peso, [simbolo, ""]] for simbolo, peso in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Função para compactar o arquivo usando o algoritmo de Huffman
def compactar_arquivo(input_path, output_path):
    with open(input_path, 'r', encoding='ISO-8859-1') as f:
        texto = f.read()

    freq = Counter(texto)
    trie = construir_trie(freq)
    codigos = {simbolo: codigo for simbolo, codigo in trie}

    with open(output_path, 'wb') as f:
        f.write(bytes([len(freq)]))
        for simbolo, codigo in trie:
            f.write(bytes([ord(simbolo)]))
            tamanho_codigo = len(codigo)
            f.write(bytes([tamanho_codigo]))
            f.write(int(codigo, 2).to_bytes((tamanho_codigo + 7) // 8, byteorder='big'))
        
        codigo_compactado = ''.join([codigos[simbolo] for simbolo in texto])
        while len(codigo_compactado) % 8 != 0:
            codigo_compactado += '0'
        for i in range(0, len(codigo_compactado), 8):
            byte = int(codigo_compactado[i:i+8], 2)
            f.write(bytes([byte]))

# Execução da compactação
compactar_arquivo('teste.txt', 'teste.uzip')