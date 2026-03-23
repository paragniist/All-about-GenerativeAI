from langchain_community.document_loaders import PyPDFLoader
#pip install pypdf
loader = PyPDFLoader('ERP-2008-chapter4.pdf')

docs = loader.load()

print(len(docs))

print(docs[0].page_content)
print(docs[1].metadata)