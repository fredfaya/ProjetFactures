import os
import sys
import tempfile
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from streamlit_modal import Modal

from Files_preprocessors.result_saver import dict_to_excel
from Pipelines.complete_pipeline import pipeline


# Définir informations_extracted comme une variable globale
if 'informations_extracted' not in st.session_state:
    st.session_state['informations_extracted'] = ""

def display_head_image():
    img = Image.open("UI/facture1_page-0001.jpg")
    st.image(img, width=100)


def space_div():
    components.html(
        """
                    <div style = "height:100px;">
                    </div>
                    """,
        height=20,
    )


def display_info_requested(info_extractred: dict):
    st.markdown(
        """
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css" integrity="sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn" crossorigin="anonymous">

        <div class="shadow bg-primary rounded pt-3 pb-3">
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-2 w-75 rounded-top">
                <div class="form-label" style="font-weight: bold; color:black">Expeditor Name</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 w-75">
                <div class="form-label" style="font-weight: bold; color:black">Expeditor Address</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 w-75">
                <div class="form-label" style="font-weight: bold; color:black">Receiver Name</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 w-75">
                <div class="form-label" style="font-weight: bold; color:black">Receiver Address</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 w-75">
                <div class="form-label" style="font-weight: bold; color:black">Total Amount</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 w-75">
                <div class="form-label" style="font-weight: bold; color:black">Goods Origin</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 pb-2 w-75 rounded-bottom">
                <div class="form-label" style="font-weight: bold; color:black">Reference</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
            <div class="row m-auto d-flex justify-content-between bg-white px-4 pt-1 pb-2 w-75 rounded-bottom">
                <div class="form-label" style="font-weight: bold; color:black">Incoterm</div>
                <div style="color: #3286E6; font-size: 10px; padding-left:50px"> {} </div>
            </div>
        </div>    

        """.format(info_extractred["expeditor_name"], info_extractred["expeditor_address"],
                   info_extractred["receiver_name"], info_extractred["receiver_address"],
                   info_extractred["total_amount"], info_extractred["goods_origin"], info_extractred["reference"],
                   info_extractred["incoterm"])
        ,
        unsafe_allow_html=True
    )


def display_title_bloc():
    components.html(
        """
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
        <div >
            <div class="h1 m-auto pt-4 pb-5 border" style="background-color: #3286E6;color : #fff ;text-align: center;">
                FILE INFORMATIONS EXTRACTOR
            </div>
        </div>

        """,
        height=100,

    )


# les modals pour afficher les messages pop up
error_modal = Modal("Wrong Reference", key="ref")

informations_modal = Modal("", key="pay")

space_div()

uploaded_file = st.file_uploader("Uploader un fichier")

if uploaded_file is not None:
    # Traitez le fichier ici
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(uploaded_file.read())
    temp_file.close()

    space_div()

    columns_button_extract = st.columns((2.25, 1, 2))

    if columns_button_extract[1].button('Extract'):

        st.session_state.informations_extracted = pipeline(temp_file.name)
        # save the information in a csv file
        st.session_state.informations_extracted['File name'] = uploaded_file.name
        dict_to_excel(st.session_state.informations_extracted, r'results.xlsx')

        if st.session_state.informations_extracted == "":
            error_modal.open()
        else:
            space_div()

            columns_infos_title = st.columns((0.65, 2, 0.15))
            columns_infos = st.columns((0.30, 2, 0.25))
            informations_modal.open()

    if error_modal.is_open():
        with error_modal.container():

            html_string = """
            <h1> An error occured while extracting informations </h1>

            <script language="javascript">
              document.querySelector("h1").style.color = "red";
              document.querySelector("h1").style.textAlign = "center";
            </script>
            """
            components.html(html_string)

            columns_button_text = st.columns((2.35, 1, 2))
            columns_button_text[1].write("Please retry :smiley:")
            columns_button_close = st.columns((2.7, 1, 2))
            close_modal1 = columns_button_close[1].button("Close", type='primary')
            if close_modal1:
                error_modal.close()



    elif informations_modal.is_open():
        with st.expander("Informations extracted from file {}".format(uploaded_file.name)):

            columns_header = st.columns((1.56, 4, 0.75))
            columns_header[1].markdown('<p style="font-family:sans-serif; color:black; font-size: 25px;">INFORMATIONS '
                                       'EXTRACTED</p>', unsafe_allow_html=True)

            display_info_requested(st.session_state.informations_extracted)

            space_div()

            columns_button_validate = st.columns((2.2, 1, 2))
            close_informations_modal = columns_button_validate[1].button("Close", type='primary')
            if close_informations_modal:
                informations_modal.close()
