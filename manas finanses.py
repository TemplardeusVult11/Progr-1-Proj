#Mans finanšu kalkulators

import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Manas Finanses")

st.title("Manas Finanses")

st.header("**Mēneša Ienākumi**")
st.subheader("Alga")
colGadaAlga, colNod = st.beta_columns(2)

with colGadaAlga:
    alga = st.number_input("Ievadi savu ikmēneša algu bruto(€): ", min_value=0.0, format='%f')
with colNod:
    nodokli = st.number_input("Ievadi atvelkamo nodokļu likmi(%): ", min_value=0.0, format='%f')

nodokli = nodokli / 100.0
alga_pec_nodokliem = alga * (1 - nodokli)
menesa_neto_alga = round(alga_pec_nodokliem / 12.0, 2)

st.header("**Mēneša izdevumi**")
colIzdevumi1, colIzdevumi2 = st.beta_columns(2)

with colIzdevumi1:
    st.subheader("Īres maksa")
    menesa_ire = st.number_input("Ievadi savu ikmēneša īres maksu(€): ", min_value=0.0,format='%f' )
    
    st.subheader("Pārtika un ēdiens")
    ikdienas_partika = st.number_input("Ievadi ikdienas pārtikas budžetu(€): ", min_value=0.0,format='%f' )
    menesa_partika = ikdienas_partika * 30
    
    st.subheader("Iespējamie mēneša neparadzētie izdevumi")
    menesa_neparadzetie = st.number_input("Ievadi ikmēneša summu neparadzētiem izdevumiem(€): ", min_value=0.0,format='%f' ) 
    
with colIzdevumi2:
    st.subheader("Mēneša transportsa izmaksas")
    menesa_transports = st.number_input("Ievadi ikmēneša transportsa izmaksas(€): ", min_value=0.0,format='%f' )   
    
    st.subheader("Ikmēneša komunālie maksājumi")
    menesa_komunalie = st.number_input("Ikmēneša komunālo maksājumu izmaksas(€): ", min_value=0.0,format='%f' )
    
    st.subheader("Izklaides")
    menesa_izklaides = st.number_input("Ievadi ikmēneša izklaižu budžetu(€): ", min_value=0.0,format='%f' )   

menesa_izdevumi = menesa_ire + menesa_partika + menesa_transports + menesa_izklaides + menesa_komunalie + menesa_neparadzetie
menesa_taupijumi = menesa_neto_alga - menesa_izdevumi 

st.header("**Ietaupījumi**")
st.subheader("Mēneša ienākumi uz rokas: €" + str(round(menesa_neto_alga,2)))
st.subheader("Mēneša izdevumi: €" + str(round(menesa_izdevumi, 2)))
st.subheader("Mēneša ietaupījums: €" + str(round(menesa_taupijumi, 2)))

st.markdown("---")

st.header("**Paredzētie ietaupījumi**")
colParedzamie1, colParedzamie2 = st.beta_columns(2)
with colParedzamie1:
    st.subheader("Gads")
    paredzamie_gada = st.number_input("Ievadi paredzētos iekrājumus (vismaz gadam uz priekšu): ", min_value=0,format='%d')
    paredzamie_menesu = 12 * paredzamie_gada 
    
    st.subheader("Gada inflācijas līmenis")
    annual_inflacijas = st.number_input("Ievadi paredzēto gada inflācijas līmeni (%): ", min_value=0.0,format='%f')
    menesa_inflacijas = (1+annual_inflacijas)**(1/12) - 1
    kumulativais_inflacijas_paredzamais = np.cumprod(np.repeat(1 + menesa_inflacijas, paredzamie_menesu))
    paredzamie_izdevumi = menesa_izdevumi*kumulativais_inflacijas_paredzamais
with colParedzamie2:
    st.subheader("Gada algas pieauguma apjoms")
    annual_pieaugums = st.number_input("Ievadi paredzēto algas pieaugumu (%): ", min_value=0.0,format='%f')
    menesa_pieaugums = (1 + annual_pieaugums) ** (1/12) - 1
    kumulativais_alga_pieaugums = np.cumprod(np.repeat(1 + menesa_pieaugums, paredzamie_menesu))
    paredzamie_alga = menesa_neto_alga * kumulativais_alga_pieaugums 
    
paredzamie_taupijumi = paredzamie_alga - paredzamie_izdevumi 
kumulativais_taupijumi = np.cumsum(paredzamie_taupijumi)

x_vertibas = np.arange(paredzamie_gada + 1)

fig = go.Figure()
fig.add_trace(
        go.Scatter(
            x=x_vertibas, 
            y=paredzamie_alga,
            name="Paredzētā alga"
        )
    )

fig.add_trace(
        go.Scatter(
            x=x_vertibas,
            y=paredzamie_izdevumi,
            name= "Parezēties izdevumi"
        )
    )

fig.add_trace(
        go.Scatter(
                x=x_vertibas, 
                y=kumulativais_taupijumi,
                name= "Paredzētie ietaupījumi"
            )
    )
fig.update_layout(title='Paredzētā alga, izdevumi un ietaupījumi gadu laikā...',
                   xaxis_title='Gads',
                   yaxis_title='Daudzums(€)')

st.plotly_chart(fig, use_container_width=True)

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y

def exponentiation(x, y):
    return x ** y

def root(x, y):
    return x // y

print("Izvēlies darbību")
print("1.Saskaitīt")
print("2.Atņemt")
print("3.Reizināt")
print("4.Dalīt")
print("5.Eksponentes")

while True:
    choice = input("Ievadiet izvēli (ciparu): ")

    if choice in ('1', '2', '3', '4', '5',):
        num1 = float(input("Ievadi pirmo skaitli: "))
        num2 = float(input("Ievadi otro skaitli: "))

        if choice == '1':
            print(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            print(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            print(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            print(num1, "/", num2, "=", divide(num1, num2))

        elif choice == '5':
            print(num1, "**", num2, "=", exponentiation(num1, num2))

        nak_darb = input("Vēlies turpināt darbības? (Jā, Nē): ")
        if nak_darb != "Jā":
            break
    else:
        print("Izvēlētais variants neatbilstošs!")