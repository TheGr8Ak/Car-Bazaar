import streamlit as st
import streamlit_authenticator as stauth
import yaml
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container
from yaml.loader import SafeLoader
import time

# Remove sidebar via CSS and adding header image
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)
# Check Login Status
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

authentication_status = st.session_state["authentication_status"]
name = st.session_state["name"]

if (not authentication_status) or (name != "supervisor2"):
    switch_page("Login")

# Logout
colspace, colspace2, column1 = st.columns((8, 10, 2))

with column1:
    if st.session_state["authentication_status"]:
        authenticator.logout(f"{name} Logout", "main", key="unique_key")

# Header image and text
st.columns(3)[1].image("images//header.png", use_column_width="auto")

# Header Text
st.header("Exterior features <2/5>", divider="red")
st.header("")
car = st.session_state["car_under_supervision"]
st.session_state["exterior_features"] = "Not set"
carinfo = st.session_state["carinfo"]

# Content
with stylable_container(
    key="container_with_border",
    css_styles="""
    {
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 1rem;
        padding: calc(1em - 1px)
    }
    """,
):
    carbrand = car.get("Brand").capitalize()
    carmodel = car.get("Model").capitalize()
    carmyear = car.get("Myear")
    carfuel = car.get("Fueltype").capitalize()
    cartransmission = car.get("Transmission").capitalize()
    carvariant = car.get("Variant").capitalize()
    carkms = car.get("Kms")
    carprice = car.get("Priceinlakh")

    col1, col2, col3 = st.columns([3, 5, 3])
    with col1:
        st.image(carinfo["Display image"])
    with col2:
        margin, col = st.columns([0.1, 0.9])
        with col:
            st.header("")
            st.header("")
            st.markdown(f"### {carmyear} {carbrand} {carmodel} {carvariant}")
            st.markdown(
                f"""#### {carfuel} · {cartransmission} · {
                    int(car['Kms'] / 1e3)}k kms"""
            )

    with col3:
        st.subheader("")
        st.write("")
        st.write("")
        st.markdown("#### Inspection date: " + carinfo["Inspection date"])
        st.markdown("#### Inspection time: " + carinfo["Inspection time"])
st.divider()
st.write(" ")

colored_header(label="Inspection Timeline", description="", color_name="red-70")
st.write(" ")
col1, col2, col3, col4, col5 = st.columns([0.21, 0.21, 0.22, 0.21, 0.15])
with col1:
    st.markdown("##### Interior Features")
with col2:
    new_title = '<h5 style="font-family:sans-serif; color:Red;">Exterior Features</h5>'
    st.markdown(new_title, unsafe_allow_html=True)
with col3:
    st.markdown("##### Comfort Features")
with col4:
    st.markdown("##### Safety Features")
with col5:
    st.markdown("##### Confirm Inspection")

inspection_progress_bar = st.progress(0, " ")
for percent_complete in range(28):
    time.sleep(0.0001)
    inspection_progress_bar.progress(percent_complete + 1, text=" ")

st.divider()
with stylable_container(
    key="container_with_border",
    css_styles="""
    {
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 1rem;
        padding: calc(2em - 1px)
    }
    """,
):
    st.subheader("Select the Exterior features available in the car: ")
    exterior_features = [
        "adjustable head lights",
        "fog lights front",
        "fog lights rear",
        "power adjustable exterior rear view mirror",
        "electric folding rear view mirror",
        "rain sensing wiper",
        "rear window wiper",
        "rear window washer",
        "rear window defogger",
        "alloy wheels",
        "integrated antenna",
        "rear spoiler",
        "roof carrier",
        "sun roof",
        "moon roof",
        "outside rear view mirror turn indicators",
        "chrome grille",
        "chrome garnish",
        "automatic driving lights",
        "roof rail",
        "heated wing mirror",
        "dual tone body colour",
        "leddrls",
        "ledheadlights",
        "ledtaillights",
        "ledfog lamps",
        "cornering foglamps",
    ]
    col1, col2, col3 = st.columns(3)
    collist = [col1, col2, col3]
    i = 0
    checkboxes = []
    for i, feat in enumerate(exterior_features):
        with collist[i % 3]:
            key = f"checkbox_{i}"
            checkbox = st.checkbox(label=feat.capitalize(), key=key)
            checkboxes.append(checkbox)
            i = i + 1

selected = []
st.header("")
confirm = st.columns(3)[1].button("Confirm", use_container_width=True, type="primary")
if confirm:
    for box in checkboxes:
        selected.append(box)
    true_vals = [
        feature.capitalize()
        for feature in exterior_features
        if checkboxes[exterior_features.index(feature)] == True
    ]
    st.session_state["exterior_features"] = true_vals
    st.toast("Exterior features recorded successfully")
    time.sleep(1)
    st.toast("Redirecting to Inspect Comfort Features")
    time.sleep(2)
    switch_page("comfortfeatures")
