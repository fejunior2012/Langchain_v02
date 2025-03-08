# Execute como um serviço
# Remova o código While True do arquivo codigo.py para executar esse servidor

from codigo import chain
from fastapi import FastAPI
from langserve import add_routes

app = FastAPI(title="Meu app de IA", description="Pergunte qual o ano de descobrimento do Brasil?")

# Criar o link de acesso
add_routes(app=app, runnable=chain, path="/myia")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

# Acesse localhost:8000/myia/playground/ depois de executar