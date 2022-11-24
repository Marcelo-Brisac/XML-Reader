import pandas as pd
f1= "09622314000109.xml"  #Macauba
f2= "35699303000129.xml"  #Ebano

def get_frame(xp):
    try:
        x = pd.read_xml(f1, xpath=xp)
        x["fundo"]=["Macauba" for _ in range(len(x.index))]
    except:
        x = None
    
    try:
        y = pd.read_xml(f2, xpath=xp)
        y["fundo"]=["Ebano" for _ in range(len(y.index))]
    except:
         y=None

    if y is None:
        return x 
    elif x is None:
        return y
    else:
        return pd.concat([x,y],ignore_index=True, axis=0)

tit_publico =       get_frame("//arquivoposicao_4_01/fundo/titpublico")
debentures =        get_frame("//arquivoposicao_4_01/fundo/debenture")
acoes =             get_frame("//arquivoposicao_4_01/fundo/acoes")
caixa =             get_frame("//arquivoposicao_4_01/fundo/caixa")
cotas =             get_frame("//arquivoposicao_4_01/fundo/cotas")
provisao =          get_frame("//arquivoposicao_4_01/fundo/provisao")
outrasdespesas =   get_frame("//arquivoposicao_4_01/fundo/outrasdespesas")

p1 = tit_publico[["isin","valorfindisp","puposicao","qtdisponivel","fundo"]].copy()
p2 = debentures[["isin","valorfindisp","puposicao","qtdisponivel","fundo"]].copy()
p3 = acoes[["codativo","valorfindisp","puposicao","qtdisponivel", "fundo"]].copy()

caixa["valorfindisp"]=caixa["saldo"]
caixa["puposicao"]=caixa["saldo"]
caixa["qtdisponivel"] = [1 for _ in caixa.index]
p4 = caixa[["isininstituicao","valorfindisp","puposicao","qtdisponivel","fundo"]]

cotas["valorfindisp"]=cotas["puposicao"]*cotas["qtdisponivel"]
p5=cotas[["cnpjfundo","valorfindisp","puposicao","qtdisponivel","fundo"]].copy()

p1.columns=["ID","Valor","Preco","Qtt","Fundo"]
p2.columns=["ID","Valor","Preco","Qtt","Fundo"]
p3.columns=["ID","Valor","Preco","Qtt","Fundo"]
p4.columns=["ID","Valor","Preco","Qtt","Fundo"]
p5.columns=["ID","Valor","Preco","Qtt","Fundo"]
final = pd.concat([p1,p2,p3,p4,p5],ignore_index=True, axis=0)

with pd.ExcelWriter("output.xlsx") as writer:
    final.to_excel(writer,sheet_name="resumo")
    tit_publico.to_excel(writer,sheet_name="tit_publico")
    debentures.to_excel(writer,sheet_name="debentures")
    acoes.to_excel(writer,sheet_name="acoes")
    cotas.to_excel(writer,sheet_name="cotas")
    caixa.to_excel(writer,sheet_name="caixa")
    try:
        provisao.to_excel(writer,sheet_name="provisao")
    except:
        pass
    try:
        outrasdespesas.to_excel(writer,sheet_name="outrasdespesas")
    except:
        pass