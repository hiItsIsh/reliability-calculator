import streamlit as st
from PIL import Image
import math 

# Function to calculate sy and se
def calculate_sy_and_se(sut,material_condition,kc,ke):
    # Convert SUT to MPa
    sut_kpsi = sut / 6.895  # 1 psi = 0.006895 MPa
  # Define material condition-specific values for 'a' and 'b'
    material_conditions = {
        "ground": (1.58, -0.085),
        "machined or cold-drawn": (4.51, -0.265),
        "hot-rolled": (57.7, -0.718),
        "as-forged": (272, -0.995),
    }
 # Get 'a' and 'b' values based on the selected material condition
    if material_condition in material_conditions:
        a, b = material_conditions[material_condition]
    else:
        st.error("Invalid material condition selected.")
        return None, None, None, None
    # Calculate sy and se in MPa
    sy_mpa = sut* 0.9
    se_mpa = sut* 0.5

    # Convert sy and se back to kpsi for display
    sy_kpsi = sy_mpa / 6.895
    se_kpsi = se_mpa / 6.895
    
#     cal ka
    ka = a * (sut ** b)
    
     #     cal Se corrected endurence limit
    
    Se=ka*kc*ke*se_mpa
    
    return sy_mpa, sy_kpsi, se_mpa, se_kpsi,sut_kpsi,ka,Se
    

    
def calculate_sy_and_se_torsional(sut, material_condition, cross_section_geometry, thickness,diameter,kc,ke):
    # Convert SUT to MPa
    
  # Define material condition-specific values for 'a' and 'b'
    material_conditions = {
        "ground": (1.58, -0.085),
        "machined or cold-drawn": (4.51, -0.265),
        "hot-rolled": (57.7, -0.718),
        "as-forged": (272, -0.995),
    }
    
     # Calculate the size factor based on the cross-section geometry
    
    if cross_section_geometry == "hollow":
        kb = 0.310*diameter
    elif cross_section_geometry == "rectangle":
        if diameter:
            kb = 1.0 - (0.275 * (diameter / thickness) ** 0.5)
    else:
        kb=diameter
 # Get 'a' and 'b' values based on the selected material condition
    if material_condition in material_conditions:
        a, b = material_conditions[material_condition]
    else:
        st.error("Invalid material condition selected.")
        return None, None, None, None
    
    
    #     cal ka
    ka = a * (sut ** b)
    

    sut_kpsi = sut / 6.895  # 1 psi = 0.006895 MPa
    # Calculate sy and se in MPa
    sy_mpa = sut* 0.9
    se_mpa = sut* 0.5

    # Convert sy and se back to kpsi for display
    sy_kpsi = sy_mpa / 6.895
    se_kpsi = se_mpa / 6.895
    #     cal Se corrected endurence limit
    
    Se=ka*kc*ke*se_mpa*kb


   
        
    return sy_mpa, sy_kpsi, se_mpa, se_kpsi,sut_kpsi,ka,Se



def kc_factor(kc1):
    if kc1=="bending":
        kc=1
    elif kc1=="axial":
        kc=0.85
    else:
        kc=0.59
    
    return kc
def no_of_cycles(f,syt,se,sf):
    se_kpsi=round(se / 6.895,4)
    sf_kpsi=round(sf/6.895,2)
    a=((syt * f)**2) / se_kpsi
    b= (-1/3) * math.log((f * syt) / se_kpsi,10)
    n=(sf_kpsi / a) ** (1 / b)
    return n,a,b,sf_kpsi,se_kpsi
# Streamlit UI
st.title("Material Strength Calculator")
i1 = Image.open('Downloads/pic-1.png')
i2 = Image.open('Downloads/pic-2.png')
i3 = Image.open('Downloads/pic-3.png')
i4 = Image.open('Downloads/pic-4.png')
i5 = Image.open('Downloads/pic-5.png')
i6 = Image.open('Downloads/pic-6.png')
i7 = Image.open('Downloads/pic-7.png')
i8 = Image.open('Downloads/pic-8.png')
i9 = Image.open('Downloads/pic-9.png')
i10 = Image.open('Downloads/pic-10.png')


# Input field for user to enter Ultimate Tensile Strength (SUT)
sut = st.number_input("Enter the Ultimate Tensile Strength (SUT) in psi:", min_value=0.0)
with st.container():
    col1, col2,col3 = st.columns([1, 1,1])
    col1.image(i8,"Sinusoidal fluctuating stress")
    col2.image(i9,"Repeated stress")
    col3.image(i10,"Completely reversed stress")
    col1, col2 = st.columns([2, 2])
    smin= col1.number_input("Enter the minimum stress ", min_value=0.0)
    smax= col2.number_input("Enter the maximum stress", min_value=0.0)
    sa=(abs(smax-smin))/2
    sm=(smax+smin)/2
st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    
    col1, col2 = st.columns([2, 3])
    material_condition = col1.selectbox("Select Material Condition:", ["ground", "machined or cold-drawn", "hot-rolled", "as-forged"])

# Input field for loading type (axial or torsional)
   
    col2.image(i1)
st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns([2, 3])
    col2.image(i2)
    loading_type = col1.selectbox("Select Loading Type:", ["axial", "torsional"])
    if loading_type == "torsional":
        st.write("Loading Type: Torsional")

    # Input field for cross-section geometry (torsional only)
        cross_section_geometry = col1.selectbox("Select Cross-Section Geometry:", ["solid", "hollow", "rectangle"])
        diameter = col1.number_input("Enter Diameter (for rectangular cross-section) in inches:", min_value=0.0)
    # Input field for thickness (for rectangular cross-section, torsional only)
        if cross_section_geometry == "rectangle":
            thickness = col1.number_input("Enter Thickness (for rectangular cross-section) in inches:", min_value=0.0)
        else:
            thickness = None




st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    
    col1, col2 = st.columns([2, 3])
    kc1 = col1.selectbox("Select load factor ", ["bending", "axial", "torsion"])
    kc=kc_factor(kc1)

    col2.image(i3)
    
st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns([2, 3])
    ke = col1.number_input("Enter Ke reliability factor from image  ", min_value=0.0)
    col2.image(i4)
st.markdown('<hr>', unsafe_allow_html=True)
with st.container():
    col1, col2 = st.columns([2, 3])
    f = col1.number_input("Enter Fatigue strength fraction from image  ", min_value=0.0)
    col2.image(i6)
    col2.image(i5)
# Button to trigger the calculation
if st.button("Calculate"):
    if loading_type == "axial":
        sy_mpa, sy_kpsi, se_mpa, se_kpsi,sut_kpsi, ka,Se= calculate_sy_and_se(sut,material_condition,kc,ke)
        n,ca,cb,sf_kpsi,se_kpsi1=no_of_cycles(f,sy_kpsi,Se,sm)
        st.write(f"No of cycle: {n,ca,cb,sf_kpsi,se_kpsi1}")
        st.write(f"Material Condition: {material_condition ,ka}")
        st.write(f"Ultimate Tensile Strength (SUT): {sut_kpsi} psi")
        st.write(f"Se` Corrected endurance limit: {Se}")
        st.write(f"Yield Strength (sy) in MPa: {sy_mpa} MPa")
        st.write(f"Yield Strength (sy) in kpsi: {sy_kpsi} kpsi")
        st.write(f"Endurance Limit (se) in MPa: {se_mpa} MPa")
        st.write(f"Endurance Limit (se) in kpsi: {se_kpsi} kpsi")
        A=sm/Se
        B=sa/sy_mpa
        B1=sa/sut
        st.write(f" fos considering Soderberg Line {1/(A+B)}")
        st.write(f" fos considering Modified Goodman line {1/(A+B1)}")

    else:
        sy_mpa, sy_kpsi, se_mpa, se_kpsi,sut_kpsi,ka,Se = calculate_sy_and_se_torsional(sut, material_condition, cross_section_geometry, thickness,diameter,kc,ke)
        n,ca,cb,sf_kpsi,se_kpsi1=no_of_cycles(f,sy_kpsi,Se,sm)
        st.write(f"No of cycle: {n,ca,cb,sf_kpsi,se_kpsi1}")
        st.write(f"Material Condition: {material_condition ,ka}")
        st.write(f"Se` Corrected endurance limit: {Se}")
        st.write(f"Ultimate Tensile Strength (SUT): {sut_kpsi} psi")
        st.write(f"Yield Strength (sy) in MPa: {sy_mpa} MPa")
        st.write(f"Yield Strength (sy) in kpsi: {sy_kpsi} kpsi")
        st.write(f"Endurance Limit (se) in MPa: {se_mpa} MPa")
        st.write(f"Endurance Limit (se) in kpsi: {se_kpsi} kpsi")
        A=sm/Se
        B=sa/sy_mpa
        B1=sa/sut
        C=1/(A+B)
        D=1/(A+B1)
        st.write(f" fos considering Soderberg Line {sm,sa}")
        st.write(f" fos considering Modified Goodman line {D}")