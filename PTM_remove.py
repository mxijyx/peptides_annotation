import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

cleaned_records = []
def remove_PTMs(input, output):
    for record in SeqIO.parse(input, "fasta"):
        raw_seq = str(record.seq)

        # Remove modification annotations like [...]
        cleaned_seq = re.sub(r'\[.*?\]', '', raw_seq).upper()

        # Filter to only valid aa
        cleaned_seq = ''.join([aa for aa in cleaned_seq if aa in "ACDEFGHIKLMNPQRSTVWY"])

        if cleaned_seq:
            cleaned_records.append(SeqRecord(Seq(cleaned_seq), id=record.id, description=""))

        with open(output, "w") as output:
            SeqIO.write(cleaned_records, output, "fasta")

if __name__ == '__main__':
    inp = input("Enter the input fasta file: ")
    out = input("Enter the output fasta file: ")
    remove_PTMs(inp, outp)

