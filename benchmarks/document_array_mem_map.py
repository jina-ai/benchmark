import os
from jina import Document
from jina.types.arrays.memmap import DocumentArrayMemmap


dlist = []
dam_size = 1000000
dam = DocumentArrayMemmap(os.path.join(os.getcwd(), 'MyMemMap'))

for i in range(dam_size):
    dlist.append(
        Document(
            text=f'This is the document number: {i}',
        )
    )

dam.extend(dlist)