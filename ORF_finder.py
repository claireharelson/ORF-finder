# Script to find open reading frames (ORFs) of a given size in a DNA sequence from an input FASTA file
from sys import stderr
import re


def find_ORFs(sequence, min_length=50) -> list:
    """
    Function to find the ORFs in a DNA sequence
    :param sequence: the DNA sequence to search
    :param min_length: minimum ORF length, default param of 50
    :return: ORFs of the sequence
    """
    # Create a regular expression for identifying ORFs
    regex = r"(ATG(?:[AGCT]{3})*?(?:TAG|TGA|TAA))"

    # Use a regular expression to identify ORFs in the given DNA sequence
    orfs = re.findall(regex, sequence)

    # Use a regular expression to identify ORFs in the reverse complementary sequence
    rev_seq = reverse_complement(sequence)
    rev_orfs = re.findall(regex, rev_seq)

    # Concatenate the ORFs from both sequences
    all_orfs = orfs + [reverse_complement(orf) for orf in rev_orfs]

    # Extract the ORFs of specified number of bases
    extracted_orfs = [orf for orf in all_orfs if len(orf) >= min_length]

    return extracted_orfs


def reverse_complement(sequence: str) -> str:
    """
    Returns the reverse complement of a DNA sequence
    :param sequence: the DNA sequence to be reversed
    :return: the reverse complement of the input sequence
    """
    complement_base = {"C": "G", "G": "C", "A": "T", "T": "A"}
    temp_sequence = sequence[::-1]
    reverse_sequence = ''
    for item in temp_sequence:
        reverse_sequence += complement_base[item]

    return reverse_sequence


def process_files():
    """
    Processes an input FASTA file and returns a dictionary mapping sequence ID to sequences
    :return: dictionary containing all sequences
    """
    # initialize variables
    sequences = {}
    sequence = ''
    sequence_id = 0
    min_length = 0
    output_file = open('output_file.txt', 'w')

    length = False
    while not length:
        min_length = int(input('Enter minimum ORF length here as an integer: '))
        if min_length >= 50:
            length = True
            output_file.write(f'Enter minimum length in bp for ORFS: {min_length}\n\n')
        else:
            print("Please enter another ORF length")

    try:
        input_file = open(input("Enter file name here: "), 'r')
        output_file.write(f'Enter FASTA file: {input_file.name}\n\n')
        next_line = input_file.readline()

        while next_line is not None and next_line != "":
            next_line = next_line.replace(' ', '').upper()
            if next_line.startswith('>'):
                if sequence_id != 0:
                    sequences[sequence_id] = sequence
                sequence_id = next_line[1:-1]
                sequence = ""
            else:
                sequence += next_line[:-1]

            next_line = input_file.readline()
        sequences[sequence_id] = sequence

    except FileNotFoundError:
        print(f'FILE NOT FOUND. CHECK INPUT FILE NAME OR PATH.', file=stderr)

    # Call to find orfs function
    for sequence_id, sequence in sequences.items():
        orfs = find_ORFs(sequence, min_length)

        # Write to output file
        for item, orf in enumerate(orfs):
            output_file.write(f'\n>{sequence_id} | FRAME =  POS =  LEN = {len(orf)}\n')
            for i in range(0, len(orf)-1, 3):
                if i % 45 == 0:
                    output_file.write(f'\n')
                output_file.write(f'{orf[i:i+3]} ')
            output_file.write(f'\n')


process_files()
