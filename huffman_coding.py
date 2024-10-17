import os
import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    frequency = defaultdict(int)
    for char in data:
        frequency[char] += 1

    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_codes(node, prefix="", codebook={}):
    if node:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    return codebook

def compress_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        data = file.read()
    
    huffman_tree = build_huffman_tree(data)
    huffman_codes = build_codes(huffman_tree)

    compressed_data = ''.join(huffman_codes[char] for char in data)

    # Save compressed data to a binary file
    with open(output_file_path, 'wb') as file:
        file.write(int(compressed_data, 2).to_bytes((len(compressed_data) + 7) // 8, byteorder='big'))

    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)

    return original_size, compressed_size
