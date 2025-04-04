import streamlit as st
import pandas as pd
import os
from io import BytesIO



# setup our app
st.set_page_config(page_title="data sweeper", layout='wide')
st.title("📁Data sweeper")
st.write("Transform your files between CSV and Excel formats with bulit-in data cleaning and visualization ")

uploade_files = st.file_uploader("upload your files(CSV or Excel):", type=["csv","xlsx"], accept_multiple_files=True)

if uploade_files:
    for file in uploade_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"unsupported file type: (file_ext)")
            continue

# display info about the file
        st.write(f"**file name:** {file.name}")
        st.write(f"**file size:** {file.size/1024}")

        # show 5 rows of our df
        st.write("Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"remove duplicates from {file.name}"):
                     df.drop_duplicates(inplace=True)
                     st.write("duplicates removed!")

            with col2:
                if st.button(f"fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("missing values have been filled!")  


                    # choose specific column to keep or convert
                    st.subheader("select column to convert")
                    columns = st.multiselect(f"choose column for {file.name}", df.columns, default=df.column)
                    df = df[columns]


                    # create some visualizations
                    st.subheader("Data Visualization")
                    if st.checkbox(f"show visualization for {file.name}"):
                        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


                        # convert the file --> CSV to Excel
                        st.subheader("Convertion Options")
                        convertion_type = st.radio(f"covert {file.name} to:",{"CSV","Excel"}, key=file.name)
                        if st.button(f"convert {file.name}"):
                            buffer = BytesIO()
                            if convertion_type == "CSV":
                                df.to_csv(buffer,index=False)
                                file_name = file.name.replace(file_ext, ".csv")
                            
                            elif convertion_type == "Excel":
                                df.to_excel(buffer, index=False)
                                file_name = file.name.repalce(file_ext,".xlsx")
                                mime_type = ""
                            buffer.seek(0)



                            # download button
                            st.download_button(
                                label=f"⬇{file.name} as {convertion_type}",
                                data=buffer,
                                filename=file_name,
                                mime=mime_type
                            )
                            
st.success("🎉All files processed!")
                    

                    